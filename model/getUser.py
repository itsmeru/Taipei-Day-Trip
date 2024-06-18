import jwt
def getUser(authorization, jwt_secret, algo):
    if not authorization or not authorization.startswith("Bearer "):
        return "provided"
        
    token = authorization.split(" ")[1]
    id,name,email = verify_token(token, jwt_secret, algo)

    if any(x is None for x in [id, name, email]):
        return None
    else:
        data = {"data":{"id": id, "name": name, "email": email}}
        return data
def verify_token(token, jwt_secret, algo):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[algo])
        id = payload.get("id")
        name = payload.get("name")
        email = payload.get("email")
        return id,name,email
    except jwt.PyJWTError as e:
        return None
