import re
from flask import render_template, request, flash
from ..services.userService import get_user

def validate(username):
  if username == '':
    flash('Please enter a username')
    return False
  regex = re.compile(r"^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$")
  result = bool(regex.match(username.lower().strip()))
  if result == False:
    flash('Please enter a valid username')
  return result


def get():
  username = request.form['username']
  isValid = validate(username)
  if not isValid:
    return render_template('index.html')
  userRepositories = get_user(username)
  return render_template('users.html', userRepositories=userRepositories)