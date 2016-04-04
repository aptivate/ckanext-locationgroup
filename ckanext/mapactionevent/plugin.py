import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.mapactionevent.logic.action.create


group_type = 'event'


class MapactioneventPlugin(plugins.SingletonPlugin, toolkit.DefaultGroupForm):
    plugins.implements(plugins.IGroupForm, inherit=False)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IRoutes

    def before_map(self, map):
        map.connect('/',
                controller='ckanext.mapactionevent.controllers.homecontroller:HomeController',
                action='index')
        map.connect('/%s/new' % group_type,
                controller='ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController',
                action='new')
        # TODO: IGroupForm register_group_plugins doesn't support delete (in
        # the <group_type>_action mapping). I'm not sure why this is, but we
        # implement it here instead:
        map.connect('%s_delete' % group_type, '/%s/delete/{id}' % group_type,
                controller='ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController',
                action='delete')

        return map

        return map

    # IActions

    def get_actions(self):
        return {
            'event_create': ckanext.mapactionevent.logic.action.create.event_create,
        }

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactionevent')

    # IGroupForm

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

