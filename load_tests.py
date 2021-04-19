import sys
from unittest import TestSuite
from django.test.runner import DiscoverRunner

import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "django_chunk_upload_handlers"))

settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        "default":{
            "ENGINE":"django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=(
        "django_audit_log_middleware",
    ),
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

default_labels = ["django_audit_log_middleware.test", ]

def get_suite(labels=default_labels):
    runner = DiscoverRunner(verbosity=1)
    failures = runner.run_tests(labels)
    if failures:
        sys.exit(failures)

    return TestSuite()

if __name__ == "__main__":
    labels = default_labels
    if len(sys.argv[1:]) > 0:
        labels = sys.argv[1:]

    get_suite(labels)
