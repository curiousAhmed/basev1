"""
friday_audit/settings.py

This module is used to write settings contents related to payroll app
"""

from friday.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "friday_audit.context_processors.history_form",
)
