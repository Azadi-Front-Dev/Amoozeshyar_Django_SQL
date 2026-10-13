
from django.db import models

from apps.users.models import Person


class Role(models.Model):
    role_id = models.IntegerField(
        db_column="RoleId",
        primary_key=True,
    )
    name = models.CharField(
        db_column="Name",
        max_length=50,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    display_name = models.CharField(
        db_column="DisplayName",
        max_length=100,
        db_collation="Arabic_CI_AS",
    )
    description = models.CharField(
        db_column="Description",
        max_length=300,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[auth].[Role]"
        verbose_name = "نقش"
        verbose_name_plural = "نقش‌ ها"

    def __str__(self):
        return self.display_name


class UserAccount(models.Model):
    user_id = models.AutoField(
        db_column="UserId",
        primary_key=True,
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.DO_NOTHING,
        db_column="PersonId",
        related_name="account",
    )
    username = models.CharField(
        db_column="Username",
        max_length=50,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    password_hash = models.CharField(
        db_column="PasswordHash",
        max_length=255,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")
    is_locked = models.BooleanField(db_column="IsLocked")
    last_login_at = models.DateTimeField(
        db_column="LastLoginAt",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(db_column="CreatedAt")
    updated_at = models.DateTimeField(
        db_column="UpdatedAt",
        blank=True,
        null=True,
    )

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    class Meta:
        managed = False
        db_table = "[auth].[UserAccount]"
        verbose_name = "حساب کاربری"
        verbose_name_plural = "حساب‌های کاربری"

    def __str__(self):
        return self.username



class UserRole(models.Model):
    pk = models.CompositePrimaryKey("user_id", "role_id")

    user = models.ForeignKey(
        UserAccount,
        on_delete=models.DO_NOTHING,
        db_column="UserId",
        related_name="user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.DO_NOTHING,
        db_column="RoleId",
        related_name="user_roles",
    )
    assigned_at = models.DateTimeField(db_column="AssignedAt")

    class Meta:
        managed = False
        db_table = "[auth].[UserRole]"

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"