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

custom_group_type = 'location'


def _get_home_index_page(app):
    user = factories.User()
    env = {'REMOTE_USER': user['name'].encode('ascii')}

    response = app.get(
        toolkit.url_for('/'),
        extra_environ=env,
    )

    return env, response


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


def _get_new_location(user, **kwargs):
    return helpers.call_action(
        'location_create',
        context={'user': user['name']},
        users=[{'name': user, 'capacity': 'admin'}],
        **kwargs
    )


class ControllerTestBase(helpers.FunctionalTestBase):
    @classmethod
    def setup_class(cls):
        super(ControllerTestBase, cls).setup_class()
        # Load the plugin under test so that the hooks get inserted
        # eg. the plugins group_types are added.
        plugins.load('locationgroup')

    @classmethod
    def teardown_class(cls):
        plugins.unload('locationgroup')
        super(ControllerTestBase, cls).teardown_class()


class TestLocationGroupController(ControllerTestBase):
    def test_save_creates_location(self):
        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = 'test'
        form['description'] = 'description'

        # TODO: Doesn't seem to work without this
        form.fields['save'][0].force_value('Create Location')
        response = submit_and_follow(app, form, env, name='save')

        # check correct redirect
        assert_equals(response.req.url,
                      'http://localhost/%s/test' % custom_group_type)

        # check saved ok
        group = model.Group.by_name(u'test')
        assert_equals(group.title, 'title')
        assert_equals(group.type, custom_group_type)
        assert_equals(group.state, 'active')

    def test_location_name_required(self):
        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = ''
        form['description'] = 'description'

        # TODO: Doesn't seem to work without this
        form.fields['save'][0].force_value('Create Location')
        response = webtest_submit(form, name='save', extra_environ=env)

        # check correct redirect
        assert_equals(response.req.url,
                      'http://localhost/%s/new' % custom_group_type)

        assert_true('Name: Missing value' in response)

    def test_cannot_have_two_identical_location_names(self):
        user = factories.User()

        _get_new_location(
            user,
            title='Albania Floods, January 2010',
            created=datetime(2010, 1, 1),
            name='albania-floods-2010')

        app = self._get_test_app()
        env, response = _get_group_new_page(app, custom_group_type)

        form = response.forms['group-edit']
        form['title'] = 'title'
        form['name'] = 'albania-floods-2010'
        form['description'] = 'description'

        # TODO: Doesn't seem to work without this
        form.fields['save'][0].force_value('Create Location')
        response = webtest_submit(form, name='save', extra_environ=env)

        # check correct redirect
        assert_equals(response.req.url,
                      'http://localhost/%s/new' % custom_group_type)

        assert_true('The form contains invalid entries' in response)
        assert_true('Name: Group name already exists in database' in response)

    def test_index_lists_locations_in_order_of_date(self):
        user = factories.User()
        location_2010 = _get_new_location(
            user,
            title='Albania Floods, January 2010',
            created=datetime(2010, 1, 1),
            name='albania-floods-2010')

        location_2009 = _get_new_location(
            user,
            title='Benin Floods, July 2009',
            created=datetime(2009, 7, 1),
            name='benin-floods-2009')

        location_2014 = _get_new_location(
            user,
            title='Cape Verde, December 2014',
            created=datetime(2014, 12, 1),
            name='cape-verde-2014')

        app = self._get_test_app()
        env, response = _get_group_index_page(app, custom_group_type)

        html = BeautifulSoup(response.body)

        titles = [u.string.strip()
                  for u in html.select('.simple-location-list li > a')]

        assert_equals(titles, [location_2014['title'],
                               location_2010['title'],
                               location_2009['title']])


class TestHomeController(ControllerTestBase):
    def test_index_lists_locations_in_order_of_date(self):
        user = factories.User()
        location_2010 = _get_new_location(
            user,
            title='Albania Floods, January 2010',
            created=datetime(2010, 1, 1),
            name='albania-floods-2010')

        location_2009 = _get_new_location(
            user,
            title='Benin Floods, July 2009',
            created=datetime(2009, 7, 1),
            name='benin-floods-2009')

        location_2014 = _get_new_location(
            user,
            title='Cape Verde, December 2014',
            created=datetime(2014, 12, 1),
            name='cape-verde-2014')

        app = self._get_test_app()
        env, response = _get_home_index_page(app)

        html = BeautifulSoup(response.body)

        titles = [u.string.strip()
                  for u in html.select('.simple-location-list li > a')]

        assert_equals(titles, [location_2014['title'],
                               location_2010['title'],
                               location_2009['title']])
