from AccessControl import Unauthorized
from plone import api
from plone.dexterity.fti import DexterityFTI
from portal.governo.content.pessoa import Pessoa
from zope.component import createObject

import pytest


CONTENT_TYPE = "Pessoa"


@pytest.fixture
def pessoa_payload() -> dict:
    """Return a payload to create a new secretaria."""
    return {
        "type": "Pessoa",
        "id": "fulano",
        "title": "Fulano da Silva",
        "description": ("Essa é a ágina do fulano," "nascido em ananindeua"),
        "email": "fulano@rs.gov.br",
        "telefone": "(51) 3210.4193",
    }


class TestPessoa:
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
        assert isinstance(obj, Pessoa)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.versioning",
            "plone.constraintypes",
            "plone.leadimage",
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
    def test_create(self, pessoa_payload, role, allowed):
        if allowed:
            with api.env.adopt_roles(role):
                content = api.content.create(container=self.portal, **pessoa_payload)
            assert content.portal_type == CONTENT_TYPE
            assert isinstance(content, Pessoa)
        else:
            with pytest.raises(Unauthorized):
                content = api.content.create(container=self.portal, **pessoa_payload)
