from flask import Flask, jsonify, request
from flask_cors import CORS
import os, time, json, jwt
from trader import trader as trader_blueprint
from ai_scheduler import start_scheduler, stop_scheduler

SECRET_KEY = os.environ.get('JWT_SECRET', 'change_this_secret_in_prod')
TOKEN_EXP_SECONDS = 3600
app = Flask(__name__)
CORS(app)
USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {'users': []}

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def auth_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'error': 'missing_token'}), 401
        token = auth.split(' ',1)[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if payload.get('exp', 0) < time.time():
                return jsonify({'error': 'token_expired'}), 401
            request.user = payload.get('sub')
        except Exception as e:
            return jsonify({'error': 'invalid_token', 'detail': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username_password_required'}), 400
    users = load_users()
    user = next((u for u in users['users'] if u['username']==username), None)
    if not user:
        return jsonify({'error': 'invalid_credentials'}), 401
    # password verification placeholder (implement bcrypt in deployed env)
    if password != 'demo':
        return jsonify({'error': 'invalid_credentials'}), 401
    payload = {'sub': username, 'iat': int(time.time()), 'exp': int(time.time()) + TOKEN_EXP_SECONDS}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({'access_token': token, 'token_type': 'bearer', 'expires_in': TOKEN_EXP_SECONDS})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok','service':'IQSIGNALS Backend'})

app.register_blueprint(trader_blueprint, url_prefix='/api/trader')

if os.environ.get('AI_AUTO_START','false').lower() in ('1','true','yes'):
    try:
        start_scheduler(interval_seconds=int(os.environ.get('AI_INTERVAL',300)), symbol='BTC/USDT', timeframe='5m', auto_execute=False, user='demo', size_pct=0.001, mode='paper')
        print('AI scheduler auto-started')
    except Exception as e:
        print('Failed to auto-start AI scheduler:', e)

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT',5000)), debug=True)
