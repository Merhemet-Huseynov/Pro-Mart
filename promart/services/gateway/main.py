from fastapi import FastAPI, Request, Header, HTTPException
import requests
import os

app = FastAPI()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:8002/api/v1//users/")

@app.get("/verify-user/")
def verify_user(Authorization: str = Header(...)):
    headers = {"Authorization": Authorization}
    try:
        res = requests.get(USER_SERVICE_URL + "me/", headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="User not found")

        user = res.json()
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gateway error: {str(e)}")