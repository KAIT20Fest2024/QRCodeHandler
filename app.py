from flask import Flask, request

app = Flask(__name__)

@app.get('/')
def root():
    return request.cookies.get('Authorization')


if __name__=="__main__":
    app.run()
