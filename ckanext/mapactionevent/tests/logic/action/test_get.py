from datetime import datetime

import nose.tools

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.mapactionevent.tests.helpers as custom_helpers

assert_equals = nose.tools.assert_equals


class TestEventList(custom_helpers.FunctionalTestBaseClass):
    def setup(self):
        super(TestEventList, self).setup()
        self.user = factories.User()

    def test_event_names_listed_by_created_descending(self):
        albania_2010 = self._get_new_event(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_event(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_event(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        event_names = helpers.call_action(
            'event_list')

        assert_equals(event_names,
                      [cape_verde_2014['name'],
                       albania_2010['name'],
                       benin_2009['name']])

    def test_event_names_listed_by_created_descending_pagination(self):
        albania_2010 = self._get_new_event(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_event(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_event(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        dominica_2015 = self._get_new_event(
            'Dominica - TS Erika, September 2015',
            datetime(2015, 9, 1))

        east_africa_2006 = self._get_new_event(
            'East Africa Seismic Risk, March 2006',
            datetime(2006, 3, 1))

        fiji_2016 = self._get_new_event(
            'Fiji - Cyclone Winston, February 2016 ',
            datetime(2016, 2, 1))

        event_names = helpers.call_action(
            'event_list',
            limit=2,
            offset=0)

        assert_equals(event_names,
                      [fiji_2016['name'],
                       dominica_2015['name']])

        event_names = helpers.call_action(
            'event_list',
            limit=2,
            offset=2)

        assert_equals(event_names,
                      [cape_verde_2014['name'],
                       albania_2010['name']])

        event_names = helpers.call_action(
            'event_list',
            limit=2,
            offset=4)

        assert_equals(event_names,
                      [benin_2009['name'],
                       east_africa_2006['name']])

    def test_events_listed_by_created_descending(self):
        albania_2010 = self._get_new_event(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_event(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_event(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        events = helpers.call_action(
            'event_list',
            all_fields=True)

        event_names = [e['name'] for e in events]

        assert_equals(event_names,
                      [cape_verde_2014['name'],
                       albania_2010['name'],
                       benin_2009['name']])

    def test_event_names_listed_by_name_ascending(self):
        albania_2010 = self._get_new_event(
            'Albania Floods, January 2010',
            datetime(2010, 1, 1))

        benin_2009 = self._get_new_event(
            'Benin Floods, July 2009',
            datetime(2009, 7, 1))

        cape_verde_2014 = self._get_new_event(
            'Cape Verde, December 2014',
            datetime(2014, 12, 1))

        event_names = helpers.call_action(
            'event_list',
            sort='name asc')

        assert_equals(event_names,
                      [albania_2010['name'],
                       benin_2009['name'],
                       cape_verde_2014['name']])

    def _get_new_event(self, title, date):
        return helpers.call_action(
            'event_create',
            context={'user': self.user['name']},
            title=title,
            created=date,
            users=[{'name': self.user, 'capacity': 'admin'}])
