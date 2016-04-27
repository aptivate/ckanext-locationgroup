import ckan.logic as logic
import ckan.plugins.toolkit as toolkit


def event_create(context, data_dict):
    """ Creates an 'event' type group """

    data_dict.update({
        'type': 'event'
    })

    try:
        event = toolkit.get_action('group_create')(
            context,
            data_dict=data_dict)
    except (logic.NotFound) as e:
        raise toolkit.ValidationError("event %s" % e)

    return event
