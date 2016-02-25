import ckan.logic as logic
import ckan.plugins.toolkit as toolkit


def event_create(context, data_dict):
    """ Creates a 'event' type group with a custom unique identifier for the
    event """

    existing_events = toolkit.get_action('group_list')(
            context,
            {'type': 'event', 'sort': 'name desc'})

    if len(existing_events) == 0:
        event_code = 1
    else:
        event_code = int(existing_events[0]) + 1

    data_dict.update({
        'name': str(event_code).zfill(5),  # Zero pad required for validation
        'type':'event'
        })

    try:
        foo = toolkit.get_action('group_create')(
            context,
            data_dict=data_dict)
    except (logic.NotFound) as e:
        raise toolkit.ValidationError("foo %s" % e)

    return foo
