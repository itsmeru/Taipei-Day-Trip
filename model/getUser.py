import jwt
def getUser(authorization, jwt_secret, algo):
    if authorization is None:
        data = {"data":None}
        return data
    token = authorization.split(" ")[1]
    id, name, email = verify_token(token, jwt_secret, algo)

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
