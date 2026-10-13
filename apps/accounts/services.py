
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import UserAccount


def authenticate_account(username, password):
    try:
        account = UserAccount.objects.select_related("person").get(
            username=username
        )
    except UserAccount.DoesNotExist:
        return None

    if not account.is_active or account.is_locked:
        return None

    if not check_password(password, account.password_hash):
        return None

    UserAccount.objects.filter(pk=account.pk).update(
        last_login_at=timezone.now()
    )

    return account
