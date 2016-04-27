from bs4 import BeautifulSoup
from datetime import datetime

import nose.tools

import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

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


def _get_group_index_page(app, group_type):
    user = factories.User()
    env = {'REMOTE_USER': user['name'].encode('ascii')}
    # See ckan.plugins.register_group_plugins
    response = app.get(
        toolkit.url_for('%s_index' % group_type),
        extra_environ=env,
    )
    return env, response


class TestEventGroupController(helpers.FunctionalTestBase):
    @classmethod
    def setup_class(cls):
        super(TestEventGroupController, cls).setup_class()
        # Load the plugin under test so that the hooks get inserted
        # eg. the plugins group_types are added.
        plugins.load('mapactionevent')

    @classmethod
    def teardown_class(cls):
        plugins.unload('mapactionevent')
        super(TestEventGroupController, cls).teardown_class()

    def test_save_creates_event(self):
        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = 'test'
        form['description'] = 'description'

        # TODO: Doesn't seem to work without this
        form.fields['save'][0].force_value('Create Event')
        response = submit_and_follow(app, form, env, name='save')

        # check correct redirect
        assert_equals(response.req.url,
                      'http://localhost/%s/test' % custom_group_type)

        # check saved ok
        group = model.Group.by_name(u'test')
        assert_equals(group.title, 'title')
        assert_equals(group.type, custom_group_type)
        assert_equals(group.state, 'active')

    def test_event_name_required(self):
        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = ''
        form['description'] = 'description'

        # TODO: Doesn't seem to work without this
        form.fields['save'][0].force_value('Create Event')
        response = webtest_submit(form, name='save', extra_environ=env)

        # check correct redirect
        assert_equals(response.req.url,
                      'http://localhost/%s/new' % custom_group_type)

        assert_true('Name: Missing value' in response)

    def test_cannot_have_two_identical_event_names(self):
        user = factories.User()

        helpers.call_action(
            'event_create',
            context={'user': user['name']},
            title='Albania Floods, January 2010',
            name='albania-floods-2010',
            created=datetime(2010, 1, 1),
            users=[{'name': user, 'capacity': 'admin'}])

        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = 'albania-floods-2010'
        form['description'] = 'description'

        # TODO: Doesn't seem to work without this
        form.fields['save'][0].force_value('Create Event')
        response = webtest_submit(form, name='save', extra_environ=env)

        # check correct redirect
        assert_equals(response.req.url,
                      'http://localhost/%s/new' % custom_group_type)

        assert_true('The form contains invalid entries' in response)
        assert_true('Name: Group name already exists in database' in response)

    def test_index_lists_events_in_order_of_date(self):
        user = factories.User()
        event_2010 = helpers.call_action(
            'event_create',
            context={'user': user['name']},
            title='Albania Floods, January 2010',
            name='albania-floods-2010',
            created=datetime(2010, 1, 1),
            users=[{'name': user, 'capacity': 'admin'}])

        event_2009 = helpers.call_action(
            'event_create',
            context={'user': user['name']},
            title='Benin Floods, July 2009',
            name='benin-floods-2009',
            created=datetime(2009, 7, 1),
            users=[{'name': user, 'capacity': 'admin'}])

        event_2014 = helpers.call_action(
            'event_create',
            context={'user': user['name']},
            title='Cape Verde, December 2014',
            name='cape-verde-2014',
            created=datetime(2014, 12, 1),
            users=[{'name': user, 'capacity': 'admin'}])

        app = self._get_test_app()
        env, response = _get_group_index_page(app, custom_group_type)

        html = BeautifulSoup(response.body)

        titles = [u.string.strip() for u in html.select('.simple-event-list li a')]

        assert_equals(titles, [event_2014['title'],
                               event_2010['title'],
                               event_2009['title']])
