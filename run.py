import os
from app import app
from livereload import Server

if __name__ == "__main__":
    if os.environ.get("ENV") == "DEVELOPMENT":
        server = Server(app)
        server.serve()
    else:
        app.run() #ssl_context="adhoc"# debug=False