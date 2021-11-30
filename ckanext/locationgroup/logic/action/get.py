import ckan.plugins.toolkit as toolkit


def location_list(context, data_dict):
    sort = data_dict.get('sort')

    data_dict['type'] = 'location'

    if sort != 'created desc':
        data_dict['all_fields'] = False
        return toolkit.get_action('group_list')(
            context,
            data_dict=data_dict)

    return _list_by_created_desc(context, data_dict)


def _list_by_created_desc(context, data_dict):
    all_fields = toolkit.asbool(data_dict.get('all_fields', None))
    offset = data_dict.get('offset', None)
    limit = data_dict.get('limit', None)
    if limit:
        end = offset+limit
    else:
        end = None

    data_dict.update(sort='name',
                     all_fields=True,
                     limit=0,
                     offset=0)

    groups = toolkit.get_action('group_list')(
        context,
        data_dict=data_dict)

    sorted_groups = sorted(groups, key=lambda group: group['created'],
                           reverse=True)[offset:end]

    if all_fields:
        return sorted_groups

    return [g['name'] for g in sorted_groups]
