import os

from flask import Flask, render_template, send_from_directory, request, jsonify
import sys

from pip._vendor import urllib3

from utils import *

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("homepage.html", clusterinfo=getclusterinfo)


@app.route('/executecmd')
def get_prediction():
  cmd = request.args.get('cmd')
  return jsonify({'html':customcommand(cmd)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
