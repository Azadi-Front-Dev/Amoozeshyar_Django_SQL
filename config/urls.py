from django.urls import include, path
from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

admin.site.site_header = "مدیریت سامانه آموزشیار"
admin.site.site_title = "پنل مدیریت آموزشیار"
admin.site.index_title = "مدیریت اطلاعات دانشگاه"
urlpatterns = [
    path("admin/", admin.site.urls),

    # API Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/academic/",
        include("apps.academic.urls"),
    ),
    path(
        "api/accounts/",
        include("apps.accounts.urls"),
    ),
]
