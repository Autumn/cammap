from werkzeug.serving import run_with_reloader

from backend import app
import backend.serv

PORT = 5000

if __name__ == '__main__':
    app.run()
    run_server()
