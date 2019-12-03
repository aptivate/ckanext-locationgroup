from datetime import datetime
from slugify import slugify

import nose.tools

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.locationgroup.tests.helpers as custom_helpers

assert_equals = nose.tools.assert_equals


class TestLocationList(custom_helpers.FunctionalTestBaseClass):
    def setup(self):
        super(TestLocationList, self).setup()
        self.user = factories.User()

    def test_location_names_listed_by_created_descending(self):
        albania_2010 = self._get_new_location(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_location(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_location(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        location_names = helpers.call_action(
            'location_list')

        assert_equals(location_names,
                      [cape_verde_2014['name'],
                       albania_2010['name'],
                       benin_2009['name']])

    def test_location_names_listed_by_created_descending_pagination(self):
        albania_2010 = self._get_new_location(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_location(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_location(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        dominica_2015 = self._get_new_location(
            'Dominica - TS Erika, September 2015',
            datetime(2015, 9, 1))

        east_africa_2006 = self._get_new_location(
            'East Africa Seismic Risk, March 2006',
            datetime(2006, 3, 1))

        fiji_2016 = self._get_new_location(
            'Fiji - Cyclone Winston, February 2016 ',
            datetime(2016, 2, 1))

        location_names = helpers.call_action(
            'location_list',
            limit=2,
            offset=0)

        assert_equals(location_names,
                      [fiji_2016['name'],
                       dominica_2015['name']])

        location_names = helpers.call_action(
            'location_list',
            limit=2,
            offset=2)

        assert_equals(location_names,
                      [cape_verde_2014['name'],
                       albania_2010['name']])

        location_names = helpers.call_action(
            'location_list',
            limit=2,
            offset=4)

        assert_equals(location_names,
                      [benin_2009['name'],
                       east_africa_2006['name']])

    def test_locations_listed_by_created_descending(self):
        albania_2010 = self._get_new_location(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_location(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_location(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        locations = helpers.call_action(
            'location_list',
            all_fields=True)

        location_names = [e['name'] for e in locations]

        assert_equals(location_names,
                      [cape_verde_2014['name'],
                       albania_2010['name'],
                       benin_2009['name']])

    def test_location_names_listed_by_name_ascending(self):
        albania_2010 = self._get_new_location(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_location(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_location(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        location_names = helpers.call_action(
            'location_list',
            sort='name asc')

        assert_equals(location_names,
                      [albania_2010['name'],
                       benin_2009['name'],
                       cape_verde_2014['name']])

    def _get_new_location(self, title, date):
        return helpers.call_action(
            'location_create',
            context={'user': self.user['name']},
            title=title,
            name=slugify(title),
            created=date,
            users=[{'name': self.user, 'capacity': 'admin'}])
