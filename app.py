from flask import Flask, jsonify
import redis
import os
import socket

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

@app.route("/")
def home():
    try:
        redis_client.incr("hits")
        hits = redis_client.get("hits")
        return jsonify({
            "message": "Flask app is running successfully",
            "redis_status": "connected",
            "hits": hits,
            "pod_name": socket.gethostname()
        })
    except Exception as e:
        return jsonify({
            "message": "Flask app is running but Redis connection failed",
            "redis_status": "failed",
            "error": str(e),
            "pod_name": socket.gethostname()
        }), 500

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200

@app.route("/ready")
def ready():
    try:
        redis_client.ping()
        return jsonify({
            "status": "ready",
            "redis": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "not ready",
            "redis": "failed",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)