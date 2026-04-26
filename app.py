from flask import Flask, request
import redis
import datetime

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def home():
    # Visitor count
    r.incr('visitors')
    visitors = r.get('visitors').decode('utf-8')
    
    # Log visit
    now = datetime.datetime.now().strftime("%H:%M:%S")
    r.lpush('logs', f"{now} - Someone visited")
    r.ltrim('logs', 0, 4)
    logs = r.lrange('logs', 0, 4)
    logs = [l.decode('utf-8') for l in logs]
    
    return f'''
    <html>
    <head><title>WellnessTracker</title></head>
    <body style="font-family:Arial; background:#0f0f1a; color:white; padding:40px; text-align:center">
        <h1>🏥 WellnessTracker</h1>
        <h3>By Neelesh Shukla</h3>
        <hr>
        <h2>📊 Live Stats</h2>
        <p>👥 Total Visitors: {visitors}</p>
        <p>⏰ Server Time: {now}</p>
        <p>✅ Flask: Running</p>
        <p>✅ Redis: Connected</p>
        <hr>
        <h2>📝 Recent Activity</h2>
        {''.join(f"<p>{log}</p>" for log in logs)}
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)