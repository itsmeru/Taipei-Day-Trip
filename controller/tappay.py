from fastapi import*
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import requests

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

class CheckPrime(BaseModel):
    prime:str
@router.post("/api/orders")
def orders(request:Request,prime:CheckPrime,token: str= Depends(oauth2_scheme)):
    client_ip = request.client.host
    print(f"Request received from IP: {client_ip}")
    order_data={
        "prime": prime.prime,
        "partner_key": "partner_71JD0IlN4Td4dKlAno18sKBDji9PScQ0oM0a0zkj7ZNpNxiSiG3hFzLm",
        "merchant_id": "tppf_itsmeru_GP_POS_3",
        "details":"TapPay Test",
        "amount": 100,
        "cardholder": {
            "phone_number": "+886923456789",
            "name": "王小明",
            "email": "LittleMing@Wang.com",
            "zip_code": "100",
            "address": "台北市天龍區芝麻街1號1樓",
            "national_id": "A123456789"
        },
        "remember": True
    }
    tap_pay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}",
        "x-api-key": "partner_71JD0IlN4Td4dKlAno18sKBDji9PScQ0oM0a0zkj7ZNpNxiSiG3hFzLm",
    }
    
    try:
        response = requests.post(tap_pay_url,json=order_data, headers=headers)
        response.raise_for_status()  # 如果请求不成功，抛出异常
        response_data = response.json()
        print(response_data)
        return response_data
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=response.status_code, detail="TapPay API请求失败")
    
    except Exception as err:
        print(f"Other error occurred: {err}")
        raise HTTPException(status_code=500, detail="服务器内部错误")

