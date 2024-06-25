from model.hashpwd import verify_password
import jwt
import os
from datetime import datetime, timedelta
def getSignIn(db_pool, email, password):
    try:
        with db_pool.get_connection() as con:
            with con.cursor(dictionary = True) as cursor:
                cursor.execute("select * from account where email = %s",(email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    hash_pwd = existing_user["password"]
                    if verify_password(password,hash_pwd):
                        token_payload = {
                            "id": existing_user["id"],
                            "name": existing_user["name"],
                            "email": existing_user["email"],
                            "iat": datetime.utcnow(),
                            "exp": datetime.utcnow() + timedelta(minutes=30)  
                        }
                        header = {
                            "typ": "JWT",
                            "alg": "HS256"
                        }
                        jwt_secret = os.environ.get("JWT_SECRET")
                        algo = os.environ.get("ALGORITHM")
                        token = jwt.encode(token_payload, jwt_secret, algorithm=algo,headers=header)
                        data = {"token": token}
                        return data
                    return "pwdfail"
                return "userfail"

    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"
       