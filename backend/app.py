from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from models import db, User
from config import Config
from oauthlib.oauth2 import WebApplicationClient
import requests
import bcrypt

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

client = WebApplicationClient(app.config["GITHUB_CLIENT_ID"])

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(email=email, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/login/github')
def login_github():
    authorization_url = client.prepare_request_uri(
        app.config['GITHUB_AUTHORIZATION_URL'],
        redirect_uri=request.base_url + "/callback",
        scope=None
    )
    return redirect(authorization_url)

@app.route('/login/github/callback')
def callback():
    code = request.args.get('code')

    token_url, headers, body = client.prepare_token_request(
        app.config['GITHUB_TOKEN_URL'],
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config["GITHUB_CLIENT_ID"], app.config["GITHUB_CLIENT_SECRET"]),
    )

    client.parse_request_body_response(token_response.text)

    # Use the GitHub API to fetch the user profile
    uri, headers, body = client.add_token(app.config['GITHUB_USER_API_URL'])
    userinfo_response = requests.get(uri, headers=headers, data=body)

    user_info = userinfo_response.json()
    github_id = user_info["id"]
    email = user_info["email"]

    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        user = User(github_id=github_id, email=email)
        db.session.add(user)
        db.session.commit()

    return jsonify({'message': 'GitHub login successful', 'user': user.email}), 200

if __name__ == '__main__':
    app.run(debug=True)
