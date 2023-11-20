from pymongo import ReturnDocument
import requests
from flask import render_template, flash
from ..extensions.database import mongo

MAX_REPOS = 5

def get_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      if len(data) == 0:
        return []
      repos = []
      for i in range(0, MAX_REPOS):
        repos.append({
                'name': get_value(data[i]['name']),
                'html_url': get_value(data[i]['html_url']),
                'description': get_value(data[i]['description']),
                'language': get_value(data[i]['language']),
            })
      return {
        'username': username,
        'avatar_url': data[0]['owner']['avatar_url'],
        'repositories': repos,
      }
    else:
      return None
    
def get_value(string):
    return string if string is not None else ''

def get_user(username):
  userCollection = mongo.db.users
  repos = get_repos(username)
  if repos is None:
    flash('Failed to fetch data, try again later')
    return render_template('index.html')
  if len(repos) > 0:
    userExists = userCollection.find_one({"username": username})
    result = userCollection.find_one_and_update(
      {"username": username},
      {
          "$set": {
              "repositories": repos['repositories'],
              "avatar_url": repos['avatar_url'],
          },
          "$setOnInsert": {
              "username": username,
          }
      },
      upsert=True,
      return_document=ReturnDocument.AFTER
    )
    userRepositories = {
      'username': result['username'],
      'avatar_url': result['avatar_url'],
      'repositories': result['repositories'],
      'status': 'new' if userExists is None else 'updated'
    }
    return userRepositories
  else:
    flash('User does not exist or has no repositories')
    return render_template('index.html')

def update_users():
    userCollection = mongo.db.users
    users = userCollection.find({})
    for user in list(users):
      print(f'Updating {user["username"]} repositories')
      repos = get_repos(user["username"])
      if repos is not None and len(repos) > 0:
        userCollection.find_one_and_update(
          {"username": user["username"]},
          {
              "$set": {
                  "repositories": repos['repositories'],
                  "avatar_url": repos['avatar_url'],
              },
          },
        )
      else:
        print(f'Failed to update {user["username"]} repositories')