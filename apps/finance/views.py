
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import StudentAccount
from .serializers import StudentAccountSerializer

# مسیر import مجوز IsStudent را مطابق فایل views.py
# در اپ accounts پروژه خودت تنظیم کن.
from apps.accounts.permissions import IsStudent


class StudentFinanceView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        person = request.user.person

        account = get_object_or_404(
            StudentAccount.objects.prefetch_related(
                "invoices",
                "payments",
            ),
            student__person=person,
            is_active=True,
        )

        serializer = StudentAccountSerializer(account)

        return Response(serializer.data)
