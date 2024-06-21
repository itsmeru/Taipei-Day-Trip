import jwt
import os
jwt_secret = os.environ.get("JWT_SECRET")
algo=os.environ.get("ALGORITHM")
def getUser(token):
    if token is None:
        data = {"data":None}
        return data
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[algo])
        id = payload.get("id")
        name = payload.get("name")
        email = payload.get("email")
        data = {"data":{"id": id, "name": name, "email": email}}
        return data
    except jwt.PyJWTError as e:
        return None
    
    
