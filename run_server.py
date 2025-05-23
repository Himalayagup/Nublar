# run_server.py
from core.main import CoreHTTPServer
import app

if __name__ == "__main__":
    server = CoreHTTPServer(host='127.0.0.1', port=4000)
    server.start()
