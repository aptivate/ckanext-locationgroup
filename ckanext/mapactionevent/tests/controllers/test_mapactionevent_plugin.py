import nose.tools

import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.mapactionimporter.tests.helpers as custom_helpers

assert_equals = nose.tools.assert_equals
assert_true = nose.tools.assert_true
assert_regexp_matches = nose.tools.assert_regexp_matches


import ckan.model as model

assert_in = helpers.assert_in
webtest_submit = helpers.webtest_submit
submit_and_follow = helpers.submit_and_follow

custom_group_type = 'event'


def _get_group_new_page(app, group_type):
    user = factories.User()
    env = {'REMOTE_USER': user['name'].encode('ascii')}
    # See ckan.plugins.register_group_plugins
    response = app.get(
        toolkit.url_for('%s_new' % group_type),
        extra_environ=env,
    )
    return env, response


class TestGroupControllerNew(helpers.FunctionalTestBase):
    @classmethod
    def setup_class(cls):
        super(TestGroupControllerNew, cls).setup_class()
        # Load the plugin under test so that the hooks get inserted
        # eg. the plugins group_types are added.
        plugins.load('mapactionevent')

    @classmethod
    def teardown_class(cls):
        plugins.unload('mapactionevent')
        super(TestGroupControllerNew, cls).teardown_class()

    def test_save(self):
        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = 'test'
        form['description'] = 'description'

        import pdb; pdb.set_trace()
        response = submit_and_follow(app, form, env, 'save')
        # response = submit_and_follow(app, form, env, name='save', value='Create Event')

        # check correct redirect
        assert_equals(response.req.url,
                     'http://localhost/%s/saved' % custom_group_type)

        # check saved ok
        group = model.Group.by_name(u'saved')
        assert_equals(group.title, u'')
        assert_equals(group.type, custom_group_type)
        assert_equals(group.state, 'active')
