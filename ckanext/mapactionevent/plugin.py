from ckan import logic

from ckan.lib.navl.validators import ignore_missing

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.mapactionevent.logic.action.create
import ckanext.mapactionevent.logic.action.get


group_type = 'event'


class MapactioneventPlugin(plugins.SingletonPlugin, toolkit.DefaultGroupForm):
    plugins.implements(plugins.IGroupForm, inherit=False)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IFacets, inherit=True)

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        if 'groups' in facets_dict:
            facets_dict['groups'] = plugins.toolkit._('Events')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        facets_dict.pop('organization', False)
        facets_dict.pop('tags', False)
        facets_dict.pop('groups', False)

        return facets_dict

    def organization_facets(self, facets_dict, group_type, package_type):
        if 'groups' in facets_dict:
            facets_dict['groups'] = plugins.toolkit._('Events')

        return facets_dict

    # IRoutes
    def before_map(self, map):
        map.connect(
            '/',
            controller='ckanext.mapactionevent.controllers.homecontroller:HomeController',
            action='index')
        map.connect(
            '/%s/new' % group_type,
            controller='ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController',
            action='new')
        # TODO: IGroupForm register_group_plugins doesn't support delete (in
        # the <group_type>_action mapping). I'm not sure why this is, but we
        # implement it here instead:
        map.connect(
            '%s_delete' % group_type, '/%s/delete/{id}' % group_type,
            controller='ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController',
            action='delete')

        map.connect(
            '%s_about' % group_type, '/%s/about/{id}' % group_type,
            controller='ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController',
            action='about')

        map.redirect('/group', '/event')
        map.redirect('/group/{url:.*}', '/event/{url}')

        return map

    # IActions

    def get_actions(self):
        return {
            'event_create': ckanext.mapactionevent.logic.action.create.event_create,
            'event_list': ckanext.mapactionevent.logic.action.get.event_list,
        }

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactionevent')

    # IGroupForm
    def form_to_db_schema_options(self, options):
        ''' This allows us to select different schemas for different
        purpose eg via the web interface or via the api or creation vs
        updating. It is optional and if not available form_to_db_schema
        should be used.
        If a context is provided, and it contains a schema, it will be
        returned.
        '''
        schema = options.get('context', {}).get('schema', None)
        if schema:
            return schema

        if options.get('api'):
            if options.get('type') == 'create':
                return self.form_to_db_schema_api_create()
            else:
                return logic.schema.default_update_group_schema()
        else:
            return self.form_to_db_schema()

    def form_to_db_schema_api_create(self):
        schema = logic.schema.default_group_schema()

        # Allow created date to be set explicitly on events
        schema['created'] = [ignore_missing]

        return schema

    def form_to_db_schema(self):
        schema = logic.schema.group_form_schema()

        # Allow created date to be set explicitly on events
        schema['created'] = [ignore_missing]

        return schema

    def group_controller(self):
        return "ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController"

    def group_types(self):
        return (group_type,)

    def is_fallback(self):
        False

    def group_form(self):
        return 'mapactionevent/group_form.html'

    def new_template(self):
        return 'mapactionevent/new.html'

    def index_template(self):
        return 'mapactionevent/index.html'

    def edit_template(self):
        return 'mapactionevent/edit.html'

    def read_template(self):
        return 'mapactionevent/read.html'

    def about_template(self):
        return 'mapactionevent/about.html'
