from .server.server import server

app = server.app

if __name__ == '__main__':
   app.run()