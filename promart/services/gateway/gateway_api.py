import requests

USER_SERVICE_URL = "http://localhost:8002/api/users/"
PRODUCT_SERVICE_URL = "http://localhost:8001/api/v1/products/"

def create_product_with_user_check(data):
    user_id = data.get("user_id")
    if not user_id:
        return {"detail": "user_id is required", "status": 400}

    try:
        user_resp = requests.get(f"{USER_SERVICE_URL}{user_id}/")
        if user_resp.status_code != 200:
            return {"detail": "User not found", "status": 404}
    except Exception as e:
        return {"detail": f"User service error: {str(e)}", "status": 500}

    try:
        product_resp = requests.post(PRODUCT_SERVICE_URL, json=data)
        return {"data": product_resp.json(), "status": product_resp.status_code}
    except Exception as e:
        return {"detail": f"Product service error: {str(e)}", "status": 500}
