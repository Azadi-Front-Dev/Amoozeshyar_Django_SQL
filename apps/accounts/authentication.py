
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings

from .models import UserAccount


class AccountJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get(api_settings.USER_ID_CLAIM)

        if user_id is None:
            raise AuthenticationFailed("Invalid token.")

        try:
            account = UserAccount.objects.select_related("person").get(
                **{api_settings.USER_ID_FIELD: user_id}
            )
        except UserAccount.DoesNotExist:
            raise AuthenticationFailed("User not found.")

        if not account.is_active or account.is_locked:
            raise AuthenticationFailed("Account is inactive or locked.")

        return account
