from django.apps import AppConfig


class BackupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "friday_backup"

    def ready(self):
        from django.urls import include, path

        from friday.urls import urlpatterns

        urlpatterns.append(
            path("backup/", include("friday_backup.urls")),
        )
        super().ready()
