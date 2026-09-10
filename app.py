import os
import logging
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

# Structured logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Prometheus metrics — exposes /metrics endpoint automatically
metrics = PrometheusMetrics(app)

APP_VERSION = "1.1.0"

@app.route('/health')
def health():
    logger.info("Health check endpoint called")
    return jsonify({"status": "UP"}), 200

@app.route('/version')
def version():
    logger.info("Version endpoint called")
    return jsonify({"version": APP_VERSION}), 200

@app.route('/environment')
def environment():
    env = os.environ.get("APP_ENV", "not-set")
    logger.info(f"Environment endpoint called - returning {env}")
    return jsonify({"environment": env}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)