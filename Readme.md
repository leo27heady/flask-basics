set FLASK_APP=src\flask-server\server.py
flask run --host 127.0.0.1 --port 5000

set FLASK_APP=src\flask-client\client.py
flask run --host 127.0.0.1 --port 5001
