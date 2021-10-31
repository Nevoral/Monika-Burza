#from web import create_app
from flask import Flask
app =  Flask(__name__)
@app.route('/')
def home():
    return 'Hello World!'
if __name__ == '__main__':
    #app = create_app()
    app.run()