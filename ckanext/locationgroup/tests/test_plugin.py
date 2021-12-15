import unittest

from ckan.common import _
from ckan.lib.navl.validators import ignore
from ckanext.locationgroup.plugin import LocationGroupPlugin


class SchemaTest(unittest.TestCase):
    def setUp(self):
        super(SchemaTest, self).setUp()
        self.plugin = LocationGroupPlugin()

    def test_form_to_db_schema_allows_created(self):
        schema = self.plugin.form_to_db_schema()

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_api_create_allows_created(self):
        schema = self.plugin.form_to_db_schema_api_create()

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_api_update_ignores_created(self):
        schema = self.plugin.form_to_db_schema_api_create()

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_options_api_create_allows_created(self):
        options = {'api': 'something',
                   'type': 'create'}

        schema = self.plugin.form_to_db_schema_options(options)

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_options_api_update_ignores_created(self):
        options = {'api': 'something',
                   'type': 'update'}

        schema = self.plugin.form_to_db_schema_options(options)

        self.assertTrue(ignore in schema['created'])

    def test_form_to_db_schema_options_not_api_allows_created(self):
        options = {'api': False}

        schema = self.plugin.form_to_db_schema_options(options)

        self.assertTrue(ignore not in schema['created'])

    def test_form_to_db_schema_options_returns_schema(self):
        my_schema = {'my schema': 'foo'}

        options = {'context': {'schema': my_schema}}

        schema = self.plugin.form_to_db_schema_options(options)

        self.assertEqual(schema, my_schema)


class DatasetFacetsTest(unittest.TestCase):
    def setUp(self):
        super(DatasetFacetsTest, self).setUp()
        self.plugin = LocationGroupPlugin()
        self.default_facet_titles = {
            'organization': _('Organizations'),
            'groups': _('Locations'),
            'tags': _('Tags'),
            'res_format': _('Formats'),
            'license_id': _('Licenses'),
        }

    def test_groups_renamed_locations(self):
        facets_dict = self.plugin.dataset_facets(self.default_facet_titles,
                                            'dataset')

        self.assertEquals(facets_dict['groups'], 'Locations')

    def test_facet_dict_is_left_empty(self):
        facets_dict = self.plugin.dataset_facets({},
                                            'dataset')

        self.assertEquals(facets_dict, {})


class GroupFacetsTest(unittest.TestCase):
    def setUp(self):
        super(GroupFacetsTest, self).setUp()
        self.plugin = LocationGroupPlugin()
        self.default_facet_titles = {'organization': _('Organizations'),
                                     'groups': _('Groups'),
                                     'tags': _('Tags'),
                                     'res_format': _('Formats'),
                                     'license_id': _('Licenses')}

    def test_removes_organization(self):
        facets_dict = self.plugin.group_facets(self.default_facet_titles,
                                          'location',
                                          'dataset')

        self.assertTrue('organization' not in facets_dict)

    def test_removes_tags(self):
        facets_dict = self.plugin.group_facets(self.default_facet_titles,
                                          'location',
                                          'dataset')

        self.assertTrue('tags' not in facets_dict)

    def test_removes_groups(self):
        facets_dict = self.plugin.group_facets(self.default_facet_titles,
                                          'location',
                                          'dataset')

        self.assertTrue('groups' not in facets_dict)

    def test_facet_dict_is_left_empty(self):
        facets_dict = self.plugin.group_facets({},
                                          'location',
                                          'dataset')

        self.assertEquals(facets_dict, {})


class OrganizationFacetsTest(unittest.TestCase):
    def setUp(self):
        super(OrganizationFacetsTest, self).setUp()
        self.plugin = LocationGroupPlugin()
        self.default_facet_titles = {'organization': _('Organizations'),
                                     'groups': _('Groups'),
                                     'tags': _('Tags'),
                                     'res_format': _('Formats'),
                                     'license_id': _('Licenses')}

    def test_groups_renamed_locations(self):
        facets_dict = self.plugin.organization_facets(self.default_facet_titles,
                                                 'organization',
                                                 'dataset')

        self.assertEquals(facets_dict['groups'], 'Locations')

    def test_facet_dict_is_left_empty(self):
        facets_dict = self.plugin.organization_facets({},
                                                 'organization',
                                                 'dataset')

        self.assertEquals(facets_dict, {})
