import nose.tools

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.locationgroup.tests.helpers as custom_helpers


class TestCreateLocation(custom_helpers.FunctionalTestBaseClass):
    def setup(self):
        super(TestCreateLocation, self).setup()
        self.user = factories.User()

    def test_location_created_with_name(self):
        location = helpers.call_action('location_create',
                                    context={'user': self.user['name']},
                                    users=[
                                        {'name': self.user,
                                         'capacity': 'admin'}],
                                    name='caf')

        nose.tools.assert_equal(location['name'], 'caf')
