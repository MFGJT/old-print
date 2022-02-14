from flask import Flask, request, send_file
import oldprint as op
import random
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return send_file('./index.html')

@app.route('/index.js', methods=['GET'])
def public():
    return send_file('./index.js')

@app.route('/generate-photo', methods=['POST'])
def get_photo():
    data = request.get_json().values()
    img = op.get_text_img(*data, ROTATION=(random.random() - 1) * 0.5)
    return send_file(io.BytesIO(img), mimetype='image/jpg')

print('log: starting server')
app.run(host='0.0.0.0', port=8080)
