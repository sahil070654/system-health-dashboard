import os
from flask import Flask, jsonify

app = Flask(__name__)

<<<<<<< HEAD
APP_VERSION = "1.1.0"
=======
APP_VERSION = "2.0.0"
>>>>>>> feature/version-update-b

@app.route('/health')
def health():
    return jsonify({"status": "UP"}), 200

@app.route('/version')
def version():
    return jsonify({"version": APP_VERSION}), 200

@app.route('/environment')
def environment():
    env = os.environ.get("APP_ENV", "not-set")
    return jsonify({"environment": env}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)