import re

import ckan.lib.base as base
import ckan.controllers.group as group
import ckan.model as model
import ckan.logic as logic

from ckan.common import c, _

abort = base.abort

NotAuthorized = logic.NotAuthorized
NotFound = logic.NotFound

class EventGroupController(group.GroupController):

    group_types = ['event']

    def _action(self, action_name):
        ''' select the correct group/org action '''
        if action_name == 'group_create':
            action_name = 'event_create'
        elif action_name == 'group_list':
            action_name = 'event_list'

        return super(EventGroupController, self)._action(action_name)

    def _render_template(self, template_name, group_type):
        ''' render the correct group/org template '''
        import sys; print >>sys.stderr, template_name, group_type
        return super(EventGroupController, self)._render_template(template_name, group_type)

    # TODO: overridden as no hook for changing template in base controller.
    def members(self, id):
        group_type = self._ensure_controller_matches_group_type(id)

        context = {'model': model, 'session': model.Session,
                   'user': c.user}

        try:
            c.members = self._action('member_list')(
                context, {'id': id, 'object_type': 'user'}
            )
            data_dict = {'id': id}
            data_dict['include_datasets'] = False
            c.group_dict = self._action('group_show')(context, data_dict)
        except NotAuthorized:
            abort(401, _('Unauthorized to delete group %s') % '')
        except NotFound:
            abort(404, _('Group not found'))
        return self._render_template('mapactionevent/members.html', group_type)
