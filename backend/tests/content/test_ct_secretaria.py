from AccessControl import Unauthorized
from plone import api
from plone.dexterity.fti import DexterityFTI
from portal.governo.content.secretaria import Secretaria
from zope.component import createObject

import pytest


CONTENT_TYPE = "Secretaria"


@pytest.fixture
def secretaria_payload() -> dict:
    """Return a payload to create a new secretaria."""
    return {
        "type": "Secretaria",
        "id": "casacivil",
        "title": "Casa Civil",
        "description": (
            "A Casa Civil do Governo do Estado foi criada em janeiro de 1954,"
            "pelo então governador Ernesto Dornelles"
        ),
        "email": "gabinete@casacivil.rs.gov.br",
        "telefone": "(51) 3210.4193",
    }


class TestSecretaria:
    @pytest.fixture(autouse=True)
    def _setup(self, get_fti, portal):
        self.fti = get_fti(CONTENT_TYPE)
        self.portal = portal

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Secretaria)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.versioning",
            "volto.blocks",
            "plone.constraintypes",
            "plone.navigationroot",
            "volto.preview_image",
            "portal.governo.behavior.contato",
            "portal.governo.behavior.endereco",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "role, allowed",
        [
            ["Manager", True],
            ["Site Administrator", True],
            ["Member", False],
            ["Editor", False],
        ],
    )
    def test_create(self, secretaria_payload, role, allowed):
        if allowed:
            with api.env.adopt_roles(role):
                content = api.content.create(
                    container=self.portal, **secretaria_payload
                )
            assert content.portal_type == CONTENT_TYPE
            assert isinstance(content, Secretaria)
        else:
            with pytest.raises(Unauthorized):
                content = api.content.create(
                    container=self.portal, **secretaria_payload
                )

    @pytest.mark.parametrize(
        "role",
        [
            ["Manager"],
            ["Site Administrator"],
            ["Member"],
            ["Editor"],
        ],
    )
    def test_cant_create(self, secretaria_payload, role):
        usr = api.user.get_current()
        with api.env.adopt_roles("Manager"):
            content = api.content.create(container=self.portal, **secretaria_payload)
        with api.env.adopt_roles(role):
            assert (
                api.user.has_permission(
                    "portal.governo: Add Secretaria", user=usr, obj=content
                )
                is False
            )
