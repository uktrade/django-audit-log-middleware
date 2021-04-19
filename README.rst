================================
Django Audit Log Middleware
================================

This package adds simple audit logging to a Django project.

A log is generated at info level each time a request is made. The log includes the following information:

 * A UTC timestamp
 * Request method (HTTP verb)
 * Full URL
 * IP address
 * A value from a custom user field (see below)
 * The requesting user's email address
 * The requesting user's first name
 * The requesting user's last name

Installation
------------

.. code-block:: python

    pip install django-audit-log-middleware

Usage
-----

Using in a Django middleware configuration:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "django_audit_log_middleware",
    ]

    MIDDLEWARE = [
        ...
        "django_audit_log_middleware.AuditLogMiddleware",
    ]

Dependencies
------------

This project is a Django app and depends on the Django package. 

This package uses Django IPware https://github.com/un33k/django-ipware for IP address capture.

Settings
--------

:code:`AUDIT_LOG_USER_FIELD`

Provide to define a field on your user model that should be captured in the audit log. Email, first name and last name are captured by default.

Tests
-----

.. code-block:: console

    $ pip install -r requirements.txt
    $ tox
