from flask import Flask, Response, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/stream')
def stream():
    def generate():
        with open('audio.mp3', 'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(generate(), mimetype='audio/mpeg')

@app.route('/order', methods=['POST'])
def order():
    item = request.form['item']
    quantity = request.form['quantity']
    return f'注文が受け付けられました。商品: {item}, 数量: {quantity}'

@app.route('/')
def index():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Delivery App</title>
</head>
<body>
    <h1>配信アプリへようこそ</h1>
    <form action="/order" method="post">
        <label for="item">商品:</label>
        <input type="text" id="item" name="item" required><br><br>
        <label for="quantity">数量:</label>
        <input type="number" id="quantity" name="quantity" min="1" required><br><br>
        <input type="submit" value="注文する">
    </form>
</body>
</html>"""

if __name__ == '__main__':
    socketio.run(app, port=5000)