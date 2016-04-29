import nose.tools

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.mapactionevent.tests.helpers as custom_helpers


class TestCreateEvent(custom_helpers.FunctionalTestBaseClass):
    def setup(self):
        super(TestCreateEvent, self).setup()
        self.user = factories.User()

    def test_event_created_with_name(self):
        event = helpers.call_action('event_create',
                                    context={'user': self.user['name']},
                                    users=[
                                        {'name': self.user,
                                         'capacity': 'admin'}],
                                    name='albania-floods-2010')

        nose.tools.assert_equal(event['name'], 'albania-floods-2010')
