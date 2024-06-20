import jwt
def getUser(authorization, jwt_secret, algo):
    token = authorization.split(" ")[1]
    result = verify_token(token, jwt_secret, algo)
    if result is None:
        data = {"data":None}
        return data
    data = {"data":{"id": result[0], "name": result[1], "email": result[2]}}
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
