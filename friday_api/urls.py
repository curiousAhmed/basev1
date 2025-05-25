from django.urls import include, path

urlpatterns = [
    path("auth/", include("friday_api.api_urls.auth.urls")),
    path("base/", include("friday_api.api_urls.base.urls")),
    path("employee/", include("friday_api.api_urls.employee.urls")),
    path("notifications/", include("friday_api.api_urls.notifications.urls")),
    path("payroll/", include("friday_api.api_urls.payroll.urls")),
    path("attendance/", include("friday_api.api_urls.attendance.urls")),
    path("leave/", include("friday_api.api_urls.leave.urls")),
]
