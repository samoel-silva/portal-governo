"""Portal settings tests."""
from plone import api

import pytest


class TestPortalSettings:
    """Test that Portal configuration is correctly done."""

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["plone.site_title", "Novo Portal de Novo Governo"],
            ["plone.email_from_name", "Novo Portal de Novo Governo"],
            ["plone.smtp_host", "procergs.mail"],
            ["plone.smtp_port", 25],
        ],
    )
    def test_setting(self, portal, key: str, expected: str):
        """Test portal title."""
        value = api.portal.get_registry_record(key)
        assert value == expected
