import jwt
import datetime
from config import config

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None