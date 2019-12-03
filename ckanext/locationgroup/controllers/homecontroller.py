import ckan.logic as logic
import ckan.lib.base as base
import ckan.model as model

from ckan.common import c
from ckan.controllers.home import HomeController as CkanHomeController


class HomeController(CkanHomeController):
    def index(self):
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'auth_user_obj': c.userobj}
        c.locations = logic.get_action('location_list')(
            context, {'type': 'location', 'all_fields': True})

        return base.render('home/index.html', cache_force=True)
