#!venv/Scripts/python
from app import app
if __name__ == "__main__":
    #app.run(host = '0.0.0.0',threaded = True, port=80) #Run on server
    app.run(debug=True) #Development on local machine: runs at http://localhost:5000
