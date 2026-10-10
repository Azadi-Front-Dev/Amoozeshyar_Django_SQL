
from django.contrib import admin

from .models import StudentAccount, Invoice, Payment


@admin.register(StudentAccount)
class StudentAccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_id",
        "student",
        "balance",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_display_links = ("account_id", "student")

    search_fields = (
        "student__student_number",
        "student__person__first_name",
        "student__person__last_name",
        "student__person__national_id",
    )

    list_filter = ("is_active",)

    ordering = ("account_id",)

    list_select_related = (
        "student",
        "student__person",
    )

    readonly_fields = (
        "account_id",
        "created_at",
        "updated_at",
    )

    list_per_page = 25


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_id",
        "account",
        "semester",
        "invoice_type",
        "title",
        "amount",
        "due_date",
        "status",
        "created_at",
    )

    list_display_links = ("invoice_id", "title")

    search_fields = (
        "title",
        "account__student__student_number",
        "account__student__person__first_name",
        "account__student__person__last_name",
    )

    list_filter = (
        "invoice_type",
        "status",
        "semester",
        "due_date",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "account",
        "account__student",
        "account__student__person",
        "semester",
    )

    readonly_fields = (
        "invoice_id",
        "created_at",
    )

    list_per_page = 25


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "account",
        "invoice",
        "amount",
        "payment_method",
        "tracking_code",
        "payment_date",
        "status",
    )

    list_display_links = ("payment_id", "account")

    search_fields = (
        "tracking_code",
        "account__student__student_number",
        "account__student__person__first_name",
        "account__student__person__last_name",
        "invoice__title",
    )

    list_filter = (
        "payment_method",
        "status",
        "payment_date",
    )

    ordering = ("-payment_date",)

    list_select_related = (
        "account",
        "account__student",
        "account__student__person",
        "invoice",
    )

    readonly_fields = (
        "payment_id",
        "created_at",
    )

    list_per_page = 25
