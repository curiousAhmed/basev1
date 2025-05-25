from django.apps import AppConfig


class fridayApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "friday_api"

    def ready(self):
        from django.urls import include, path

        from friday.urls import urlpatterns

        urlpatterns.append(
            path("api/", include("friday_api.urls")),
        )
        super().ready()
