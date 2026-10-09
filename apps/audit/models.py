
from django.db import models

from apps.accounts.models import UserAccount


class AuditLog(models.Model):
    audit_log_id = models.BigIntegerField(
        db_column="AuditLogId",
        primary_key=True,
    )
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.DO_NOTHING,
        db_column="UserId",
        related_name="audit_logs",
        blank=True,
        null=True,
    )
    action = models.CharField(
        db_column="Action",
        max_length=30,
        db_collation="Arabic_CI_AS",
    )
    entity_name = models.CharField(
        db_column="EntityName",
        max_length=100,
        db_collation="Arabic_CI_AS",
    )
    entity_id = models.CharField(
        db_column="EntityId",
        max_length=100,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    old_values = models.TextField(
        db_column="OldValues",
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    new_values = models.TextField(
        db_column="NewValues",
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    ip_address = models.CharField(
        db_column="IpAddress",
        max_length=45,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    user_agent = models.CharField(
        db_column="UserAgent",
        max_length=500,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )

    class Meta:
        managed = False
        db_table = "[system].[AuditLog]"

    def __str__(self):
        return f"{self.action} - {self.entity_name}"

