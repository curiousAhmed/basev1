"""
friday_apps

This module is used to register friday addons
"""

from friday import settings
from friday.settings import INSTALLED_APPS

INSTALLED_APPS.append("accessibility")
INSTALLED_APPS.append("friday_audit")
INSTALLED_APPS.append("friday_widgets")
INSTALLED_APPS.append("friday_crumbs")
INSTALLED_APPS.append("friday_documents")
INSTALLED_APPS.append("haystack")
INSTALLED_APPS.append("friday_views")
INSTALLED_APPS.append("friday_automations")
INSTALLED_APPS.append("auditlog")
INSTALLED_APPS.append("biometric")
INSTALLED_APPS.append("helpdesk")
INSTALLED_APPS.append("friday_backup")
if settings.env("AWS_ACCESS_KEY_ID", default=None) and "storages" not in INSTALLED_APPS:
    INSTALLED_APPS.append("storages")


AUDITLOG_INCLUDE_ALL_MODELS = True

AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    # "<app_name>",
    # "<app_name>.<model>"
)

setattr(settings, "AUDITLOG_INCLUDE_ALL_MODELS", AUDITLOG_INCLUDE_ALL_MODELS)
setattr(settings, "AUDITLOG_EXCLUDE_TRACKING_MODELS", AUDITLOG_EXCLUDE_TRACKING_MODELS)

settings.MIDDLEWARE.append(
    "auditlog.middleware.AuditlogMiddleware",
)

SETTINGS_EMAIL_BACKEND = getattr(settings, "EMAIL_BACKEND", False)
setattr(settings, "EMAIL_BACKEND", "base.backends.ConfiguredEmailBackend")
if SETTINGS_EMAIL_BACKEND:
    setattr(settings, "EMAIL_BACKEND", SETTINGS_EMAIL_BACKEND)


SIDEBARS = [
    "onboarding",
    "employee",
    "attendance",
    "leave",
    "payroll",
    "helpdesk",
]

WHITE_LABELLING = False
NESTED_SUBORDINATE_VISIBILITY = False
