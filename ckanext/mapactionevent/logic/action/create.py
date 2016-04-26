import ckan.logic as logic
import ckan.plugins.toolkit as toolkit


def event_create(context, data_dict):
    """ Creates a 'event' type group with a custom unique identifier for the
    event """

    if data_dict.get('name'):
        name = data_dict.get('name')
    else:
        # Generate a new operation ID
        existing_events = toolkit.get_action('group_list')(
            context,
            {'type': 'event', 'sort': 'name desc'})

        # default value, if there are no existing
        # numerically named events
        event_code = 1

        for event in existing_events:
            if event.isdigit():
                event_code = int(event) + 1
                break

        name = str(event_code).zfill(5)

    data_dict.update({
        'name': name,
        'type': 'event'
    })

    try:
        event = toolkit.get_action('group_create')(
            context,
            data_dict=data_dict)
    except (logic.NotFound) as e:
        raise toolkit.ValidationError("event %s" % e)

    return event
