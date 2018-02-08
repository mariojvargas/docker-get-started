from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<em>cannot connect to Redis dawg! Counter is disabled</em>"

    html = "<h3>Hello {name}!</h3>" \
           "<p><strong>Hostname:</strong> {hostname}</p>" \
           "<p><strong>Visits:</strong> {visits}</p>"
    
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
