import ckan.model as model
import ckan.controllers.group as group
import ckan.plugins.toolkit as toolkit


class EventGroupController(group.GroupController):

    def _action(self, action_name):
        ''' select the correct group/org action '''
        if action_name == 'group_create':
            action_name = 'event_create'
        return super(EventGroupController, self)._action(action_name)
