"""Setup tests for this package."""

from collective.js.underscore.testing import INTEGRATION_TESTING
from plone.base.interfaces import IBundleRegistry
from plone.base.utils import get_installer
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.resources.browser.resource import ScriptsView
from zope.component import getUtility

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.js.underscore is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.installer = get_installer(self.portal, self.request)
        self.registry = getUtility(IRegistry)
        self.bundles = self.registry.collectionOfInterface(
            IBundleRegistry, prefix="plone.bundles"
        )

    def test_install(self):
        self.assertTrue(self.installer.is_product_installed("collective.js.underscore"))
        self.assertIn("underscore", self.bundles)
        scripts = ScriptsView(self.layer["portal"], self.layer["request"], None)
        scripts.update()
        results = scripts.render()
        self.assertIn("++resource++collective.js.underscore/underscore.min.js", results)

    def test_uninstall(self):
        self.installer.uninstall_product("collective.js.underscore")
        self.assertFalse(
            self.installer.is_product_installed("collective.js.underscore")
        )
        self.assertNotIn("underscore", self.bundles)
        scripts = ScriptsView(self.layer["portal"], self.layer["request"], None)
        scripts.update()
        results = scripts.render()
        self.assertNotIn(
            "++resource++collective.js.underscore/underscore.min.js", results
        )
