from distutils.core import setup

import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="django_audit_log_middleware",
    version="0.0.1",
    packages=setuptools.find_packages(),
    author="Ross Miller",
    author_email="ross.miller@digita.trade.gov.uk",
    url="https://github.com/uktrade/django-audit-log-middleware",
    description="Simple audit logging for Django requests",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
        "django~=3.1.6",
        "django-ipware~=3.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
