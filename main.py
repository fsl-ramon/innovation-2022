from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        print(request.get_json())
        return 'OK', 200