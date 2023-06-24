from flask import Flask
# экземпляр класса Flask
app = Flask(__name__)
# задать маршрут во Flask
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()





