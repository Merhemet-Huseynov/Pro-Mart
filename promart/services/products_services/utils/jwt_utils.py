from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

__all__ = [
    "get_user_from_token",
]

def get_user_from_token(request):
    auth = JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(
            auth.get_raw_token(request.headers.get("Authorization").split()[1])
        )
        return {
            "id": validated_token.get("user_id"),
            "user_type": validated_token.get("user_type"),
        }
    except Exception:
        raise AuthenticationFailed("Invalid token or user not found")
