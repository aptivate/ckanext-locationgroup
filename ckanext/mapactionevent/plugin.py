import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.mapactionevent.logic.action.create


group_type = 'event'


class MapactioneventPlugin(plugins.SingletonPlugin, toolkit.DefaultGroupForm):
    plugins.implements(plugins.IGroupForm, inherit=False)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IRoutes, inherit=True)
    # plugins.implements(plugins.IGroupController, inherit=True)


    # IRoutes

    def before_map(self, map):
        map.connect('/%s/new' % group_type, controller='ckanext.mapactionevent.controllers.event_groupcontroller:EventGroupController', action='new')
        #map.connect('/group/{id}', controller='ckanext.datacatalogs.controller:DataCatalogsGroupController', action='read')
        return map


    # IGroupController

    def create(self, entity):
        # import pdb; pdb.set_trace()
        print entity
        pass

    def after_create(self, context, pkg_dict):
        '''
            Extensions will receive the validated data dict after the package
            has been created (Note that the create method will return a package
            domain object, which may not include all fields). Also the newly
            created package id will be added to the dict.
        '''
        # import pdb; pdb.set_trace()
        print context, pkg_dict
        pass


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

    def group_types(self):
        return (group_type,)

    def is_fallback(self):
        False

    def group_form(self):
        return 'mapactionevent/group_form.html'
