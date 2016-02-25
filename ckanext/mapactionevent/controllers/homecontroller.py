import ckan.logic as logic
import ckan.lib.maintain as maintain
import ckan.lib.search as search
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit

from ckan.common import _, g, c
from ckan.controllers.home import HomeController

CACHE_PARAMETERS = ['__cache', '__no_cache__']


class HomeController(HomeController):

    def index(self):
        try:
            # package search
            context = {'model': model, 'session': model.Session,
                       'user': c.user, 'auth_user_obj': c.userobj}
            data_dict = {
                'q': '*:*',
                'facet.field': g.facets,
                'rows': 4,
                'start': 0,
                'sort': 'views_recent desc',
                'fq': 'capacity:"public"'
            }
            query = logic.get_action('package_search')(
                context, data_dict)
            c.search_facets = query['search_facets']
            c.package_count = query['count']
            c.datasets = query['results']

            c.facets = query['facets']
            maintain.deprecate_context_item(
                'facets',
                'Use `c.search_facets` instead.')

            c.search_facets = query['search_facets']

            c.facet_titles = {
                'organization': _('Organizations'),
                'groups': _('Groups'),
                'tags': _('Tags'),
                'res_format': _('Formats'),
                'license': _('Licenses'),
            }

            events = logic.get_action('group_list')(
                    context, {'type': 'event', 'all_fields': True})
            c.events = events

        except search.SearchError:
            c.package_count = 0

        if c.userobj and not c.userobj.email:
            url = h.url_for(controller='user', action='edit')
            msg = _('Please <a href="%s">update your profile</a>'
                    ' and add your email address. ') % url + \
                _('%s uses your email address'
                    ' if you need to reset your password.') \
                % g.site_title
            h.flash_notice(msg, allow_html=True)

        return base.render('home/index.html', cache_force=True)
