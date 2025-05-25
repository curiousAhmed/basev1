from django.contrib import admin

from friday_automations.models import MailAutomation

# Register your models here.


admin.site.register(
    [
        MailAutomation,
    ]
)
