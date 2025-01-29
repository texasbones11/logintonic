from dotenv import load_dotenv
import os

load_dotenv()

class Config:
   SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
   SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
   GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
   GITHUB_AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
   GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
   GITHUB_USER_API_URL = 'https://api.github.com/user'
