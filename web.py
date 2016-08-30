from flask import Flask, jsonify, render_template, request
import flask.json

from messages import LogViewer


app = Flask(__name__)
#app.json_encoder = MessagesEncoder


@app.route('/messages/<channel>')
def channel(channel):
    before_message = request.args.get('before_message')
    return flask.jsonify([m.to_json() for m in LogViewer().tail(channel, 100, before_message)])


@app.route('/', defaults={'path':''})
@app.route('/channel/<path>')
def index(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
