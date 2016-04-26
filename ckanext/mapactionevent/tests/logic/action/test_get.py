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

        self.albania_2010 = helpers.call_action(
            'event_create',
            context={'user': self.user['name']},
            title='Albania Floods, January 2010',
            created=datetime(2010, 1, 1),
            users=[{'name': self.user, 'capacity': 'admin'}])

        self.benin_2009 = helpers.call_action(
            'event_create',
            context={'user': self.user['name']},
            title='Benin Floods, July 2009',
            created=datetime(2009, 7, 1),
            users=[{'name': self.user, 'capacity': 'admin'}])

        self.cape_verde_2014 = helpers.call_action(
            'event_create',
            context={'user': self.user['name']},
            title='Cape Verde, December 2014',
            created=datetime(2014, 12, 1),
            users=[{'name': self.user, 'capacity': 'admin'}])

    def test_event_names_listed_by_created_descending(self):
        event_names = helpers.call_action(
            'event_list')

        assert_equals(event_names,
                      [self.cape_verde_2014['name'],
                       self.albania_2010['name'],
                       self.benin_2009['name']])

    def test_events_listed_by_created_descending(self):
        events = helpers.call_action(
            'event_list',
            all_fields=True)

        event_names = [e['name'] for e in events]

        assert_equals(event_names,
                      [self.cape_verde_2014['name'],
                       self.albania_2010['name'],
                       self.benin_2009['name']])

    def test_event_names_listed_by_name_ascending(self):
        event_names = helpers.call_action(
            'event_list',
            sort='name asc')

        assert_equals(event_names,
                      [self.albania_2010['name'],
                       self.benin_2009['name'],
                       self.cape_verde_2014['name']])
