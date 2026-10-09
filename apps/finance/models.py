
from django.db import models

from apps.education.models import Semester
from apps.users.models import Student


class StudentAccount(models.Model):
    account_id = models.IntegerField(
        db_column="AccountId",
        primary_key=True,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        db_column="StudentId",
        related_name="financial_accounts",
    )
    balance = models.DecimalField(
        db_column="Balance",
        max_digits=18,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        db_column="IsActive",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )
    updated_at = models.DateTimeField(
        db_column="UpdatedAt",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "[finance].[StudentAccount]"

    def __str__(self):
        return f"Account {self.account_id}"


class Invoice(models.Model):
    invoice_id = models.BigIntegerField(
        db_column="InvoiceId",
        primary_key=True,
    )
    account = models.ForeignKey(
        StudentAccount,
        on_delete=models.DO_NOTHING,
        db_column="AccountId",
        related_name="invoices",
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.DO_NOTHING,
        db_column="SemesterId",
        related_name="invoices",
        blank=True,
        null=True,
    )
    invoice_type = models.CharField(
        db_column="InvoiceType",
        max_length=30,
        db_collation="Arabic_CI_AS",
    )
    title = models.CharField(
        db_column="Title",
        max_length=200,
        db_collation="Arabic_CI_AS",
    )
    amount = models.DecimalField(
        db_column="Amount",
        max_digits=18,
        decimal_places=2,
    )
    due_date = models.DateField(
        db_column="DueDate",
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )

    class Meta:
        managed = False
        db_table = "[finance].[Invoice]"

    def __str__(self):
        return f"Invoice {self.invoice_id}"


class Payment(models.Model):
    payment_id = models.BigIntegerField(
        db_column="PaymentId",
        primary_key=True,
    )
    account = models.ForeignKey(
        StudentAccount,
        on_delete=models.DO_NOTHING,
        db_column="AccountId",
        related_name="payments",
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.DO_NOTHING,
        db_column="InvoiceId",
        related_name="payments",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        db_column="Amount",
        max_digits=18,
        decimal_places=2,
    )
    payment_method = models.CharField(
        db_column="PaymentMethod",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    tracking_code = models.CharField(
        db_column="TrackingCode",
        max_length=100,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    payment_date = models.DateTimeField(
        db_column="PaymentDate",
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    description = models.CharField(
        db_column="Description",
        max_length=300,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )

    class Meta:
        managed = False
        db_table = "[finance].[Payment]"

    def __str__(self):
        return f"Payment {self.payment_id}"

