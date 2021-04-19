from unittest.mock import patch, MagicMock, Mock

from django_audit_log_middleware import AuditLogMiddleware
from django.test import override_settings, TestCase


class AuditLogTests(TestCase):
    def setUp(self):
        self.middleware = AuditLogMiddleware(
            get_response=MagicMock()
        )
        self.request = Mock()
        self.ip = "1.1.1.1"
        self.request.META = { 
            "REMOTE_ADDR": self.ip,
        }
        self.request.method = "GET"
        self.request.build_absolute_uri = Mock(return_value="http://www.test.com?test=1")

        self.request.user = Mock(
            first_name="Jane",
            last_name="Test",
            email="jane@test.com",
        )

    @patch('django_audit_log_middleware.AuditLogMiddleware._get_utc_now')
    def test_log_output_on_request(self, utcnow):
        utcnow.return_value = "Test"

        with self.assertLogs('django_audit_log_middleware', level='INFO') as test_logger:
            response = self.middleware(self.request)

            expected = (
                "INFO:django_audit_log_middleware:"
                f"Security audit log:\t"
                f"{utcnow.return_value}\t"
                f"{self.request.method}\t"
                f"{self.request.build_absolute_uri()}\t"
                f"{self.ip}\t"
                f"\t"
                f"{self.request.user.email}\t"
                f"{self.request.user.first_name}\t"
                f"{self.request.user.last_name}"
            )

            self.assertEqual(expected, test_logger.output[0])

    @override_settings(AUDIT_LOG_USER_FIELD="username")
    @patch('django_audit_log_middleware.AuditLogMiddleware._get_utc_now')
    def test_log_output_with_custom_user_id(self, utcnow):
        utcnow.return_value = "Test"

        self.request.user = Mock(
            username="custom id test",
            first_name="Jane",
            last_name="Test",
            email="jane@test.com",
        )

        with self.assertLogs('django_audit_log_middleware', level='INFO') as test_logger:
            response = self.middleware(self.request)

            expected = (
                "INFO:django_audit_log_middleware:"
                f"Security audit log:\t"
                f"{utcnow.return_value}\t"
                f"{self.request.method}\t"
                f"{self.request.build_absolute_uri()}\t"
                f"{self.ip}\t"
                f"{self.request.user.username}\t"
                f"{self.request.user.email}\t"
                f"{self.request.user.first_name}\t"
                f"{self.request.user.last_name}"
            )

            self.assertEqual(expected, test_logger.output[0])
