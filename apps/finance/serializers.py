
from rest_framework import serializers
from .models import StudentAccount, Invoice, Payment


class InvoiceSerializer(serializers.ModelSerializer):
    # شناسه ترم از روی ForeignKey خوانده می‌شود
    semester_id = serializers.IntegerField(
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Invoice
        fields = [
            "invoice_id",
            "invoice_type",
            "title",
            "amount",
            "due_date",
            "status",
            "semester_id",
            "created_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    invoice_title = serializers.CharField(
        source="invoice.title",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Payment
        fields = [
            "payment_id",
            "invoice_id",
            "invoice_title",
            "amount",
            "payment_method",
            "tracking_code",
            "payment_date",
            "status",
            "description",
        ]


class StudentAccountSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = StudentAccount
        fields = [
            "account_id",
            "balance",
            "is_active",
            "invoices",
            "payments",
        ]
