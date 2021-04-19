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
    def _get_utc_now():
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

    def __call__(self, request):
        self.request = request

        logger.info(
            f"Security audit log:\t"
            f"{self._get_utc_now()}\t"
            f"{request.method}\t"
            f"{request.build_absolute_uri()}\t"
            f"{self._get_ip_address()}\t"
            f"{self._get_custom_user_id()}\t"
            f"{request.user.email}\t"
            f"{request.user.first_name}\t"
            f"{request.user.last_name}"
        )

        response = self.get_response(request)
        return response
