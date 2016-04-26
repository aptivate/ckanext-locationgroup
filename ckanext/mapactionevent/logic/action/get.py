import ckan.plugins.toolkit as toolkit


def event_list(context, data_dict):
    sort = data_dict.get('sort') or 'created desc'

    all_fields = toolkit.asbool(data_dict.get('all_fields', None))

    if sort == 'created desc':
        data_dict.update(sort='name',
                         all_fields=True)

    data_dict['type'] = 'event'

    groups = toolkit.get_action('group_list')(
        context,
        data_dict=data_dict)

    if sort != 'created desc':
        return groups

    sorted_groups = sorted(groups, key=lambda group: group['created'],
                           reverse=True)

    if all_fields:
        return sorted_groups

    return [g['name'] for g in sorted_groups]
