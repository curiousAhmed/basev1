from friday.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "friday_crumbs.context_processors.breadcrumbs",
)
