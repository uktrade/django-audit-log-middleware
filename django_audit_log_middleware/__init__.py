from datetime import datetime
import logging

from ipware import get_client_ip

from django.conf import settings


logger = logging.getLogger(__name__)


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _get_ip_address(self):
        client_ip, is_routable = get_client_ip(self.request)
        return client_ip or "Unknown"

    # Defined so it we can mock it
    def _get_utc_now(self):
        return datetime.utcnow()

    #  Check for custom user id in request.user
    def _get_custom_user_id(self):
        if getattr(
            settings, "AUDIT_LOG_USER_FIELD", None
        ) is not None:
            if hasattr(
                self.request.user,
                settings.AUDIT_LOG_USER_FIELD,
            ):
                return getattr(
                    self.request.user,
                    settings.AUDIT_LOG_USER_FIELD,
                )

        return ""

    def _get_email(self):
        if self.request.user.is_authenticated:
            return self.request.user.email

        return "anonymous"

    def _get_first_name(self):
        if self.request.user.is_authenticated:
            return self.request.user.first_name

        return ""

    def _get_last_name(self):
        if self.request.user.is_authenticated:
            return self.request.user.last_name

        return ""

    def __call__(self, request):
        self.request = request

        logger.info(
            f"Security audit log:\t"
            f"{self._get_utc_now()}\t"
            f"{request.method}\t"
            f"{request.build_absolute_uri()}\t"
            f"{self._get_ip_address()}\t"
            f"{self._get_custom_user_id()}\t"
            f"{self._get_email()}\t"
            f"{self._get_first_name()}\t"
            f"{self._get_last_name()}"
        )

        response = self.get_response(request)
        return response
