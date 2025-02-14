import jwt
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")