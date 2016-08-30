from flask import Flask, jsonify, render_template, request
import flask.json

from messages import LogViewer
from models import MessagesEncoder


app = Flask(__name__)
#app.json_encoder = MessagesEncoder

@app.route('/')
def index():
    return render_template('index.html')

# /messages/<channel>/tail/100
# /messages/<channel>/tail/100/before/123098120312.234
@app.route('/messages/')
def channel():
    before_message = request.args.get('before_message')
    return flask.jsonify([m.to_json() for m in LogViewer().tail('random', 100, before_message)])


if __name__ == '__main__':
    app.run()
