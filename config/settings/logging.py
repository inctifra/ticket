LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "tenant_context": {"()": "django_tenants.log.TenantContextFilter"},
    },
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            ),
        },
        "tenant_context": {
            "format": (
                "[%(schema_name)s:%(domain_url)s] "
                "%(levelname)-7s %(asctime)s %(message)s"
            ),
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "tenant_context",  # <-- FIXED
            "filters": ["tenant_context"],
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "django": {  # MAIN DJANGO LOGS
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "tenant": {  # DJANGO TENANTS LOGS
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry_sdk": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
