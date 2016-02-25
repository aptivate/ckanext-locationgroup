import nose.tools

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.mapactionevent.tests.helpers as custom_helpers
import ckan.plugins.toolkit as toolkit


class TestCreateEvent(custom_helpers.FunctionalTestBaseClass):
    def setup(self):
        super(TestCreateEvent, self).setup()
        self.user = factories.User()

    def test_initial_event_id_created_is_one(self):
        existing_events = helpers.call_action('group_list',
                type='event')

        nose.tools.assert_equal(len(existing_events), 0)

        event = helpers.call_action('event_create',
                context={'user': self.user['name']},
                users=[{'name': self.user, 'capacity': 'admin'}])

        nose.tools.assert_equal(event['name'], '001')

    def test_event_id_created_after_last(self):
        event = helpers.call_action('event_create',
                context={'user': self.user['name']},
                users=[{'name': self.user, 'capacity': 'admin'}])

        nose.tools.assert_equal(event['name'], '001')

        event = helpers.call_action('event_create',
                context={'user': self.user['name']},
                users=[{'name': self.user, 'capacity': 'admin'}])

        nose.tools.assert_equal(event['name'], '002')
