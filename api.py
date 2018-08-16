from flask import Flask

app = Flask(__name__)


if _name__ == '__main__':
    app.run(debug==True)