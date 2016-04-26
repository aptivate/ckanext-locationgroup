import unittest

from ckan.lib.navl.validators import ignore
from ckanext.mapactionevent.plugin import MapactioneventPlugin


class SchemaTest(unittest.TestCase):

    def test_form_to_db_schema_allows_created(self):
        plugin = MapactioneventPlugin()
        schema = plugin.form_to_db_schema()

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_api_create_allows_created(self):
        plugin = MapactioneventPlugin()
        schema = plugin.form_to_db_schema_api_create()

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_api_update_ignores_created(self):
        plugin = MapactioneventPlugin()
        schema = plugin.form_to_db_schema_api_create()

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_options_api_create_allows_created(self):
        plugin = MapactioneventPlugin()

        options = {'api': 'something',
                   'type': 'create'}

        schema = plugin.form_to_db_schema_options(options)

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_options_api_update_ignores_created(self):
        plugin = MapactioneventPlugin()

        options = {'api': 'something',
                   'type': 'update'}

        schema = plugin.form_to_db_schema_options(options)

        self.assertTrue(ignore in schema['created'])

    def test_form_to_db_schema_options_not_api_allows_created(self):
        plugin = MapactioneventPlugin()

        options = {'api': False}

        schema = plugin.form_to_db_schema_options(options)

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_options_returns_schema(self):
        plugin = MapactioneventPlugin()

        my_schema = {'my schema': 'foo'}

        options = {'context': {'schema': my_schema}}

        schema = plugin.form_to_db_schema_options(options)

        self.assertEqual(schema, my_schema)
