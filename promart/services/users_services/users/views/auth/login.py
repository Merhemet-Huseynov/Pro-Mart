import logging
from rest_framework.views import APIView, Response, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import LoginSerializer

__all__ = ["LoginView"]

logger = logging.getLogger(__name__)


class LoginView(APIView):
    """
    View to handle user login requests.

    Allows users to authenticate using their credentials.
    Returns validated user data on success, or error messages on failure.
    """

    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description="Authenticate a user using email/username and password.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful. Returns user info or token.",
                examples={
                    "application/json": {
                        "token": "abc123xyz456",
                        "username": "johndoe",
                        "email": "john@example.com"
                    }
                }
            ),
            400: openapi.Response(
                description="Login failed due to invalid credentials or missing data.",
                examples={
                    "application/json": {
                        "non_field_errors": [
                            "Unable to log in with provided credentials."
                        ]
                    }
                }
            ),
        }
    )
    def post(self, request) -> Response:
        """
        Handles the POST request to log in a user.

        Args:
            request: The HTTP request containing user credentials.

        Returns:
            Response: A Response object with login result.
        """
        logger.info("Login request received")

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            logger.info("Login successful")
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        logger.warning("Login failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
