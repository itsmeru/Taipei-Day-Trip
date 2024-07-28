from model.hashpwd import verify_password
from sqlalchemy.future import select
import jwt
import os
from datetime import datetime, timedelta
async def getSignIn(db, email, password,Account):
    try:
        stmt = select(Account).filter(Account.email == email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            hash_pwd = existing_user.password
            if verify_password(password, hash_pwd):
                token_payload = {
                    "id": existing_user.id,
                    "name": existing_user.name,
                    "email": existing_user.email,
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(minutes=60)
                }
                header = {
                    "typ": "JWT",
                    "alg": "HS256"
                }
                jwt_secret = os.environ.get("JWT_SECRET")
                algo = os.environ.get("ALGORITHM")
                token = jwt.encode(token_payload, jwt_secret, algorithm=algo, headers=header)
                data = {"token": token, "id": existing_user.id}
                return data
            return "pwdfail"
        return "userfail"

    except Exception as e:
        print(f"signin Unhandled exception: {e}")
        return "error"

       