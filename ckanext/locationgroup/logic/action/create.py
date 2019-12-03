import ckan.logic as logic
import ckan.plugins.toolkit as toolkit


def location_create(context, data_dict):
    """ Creates an 'location' type group """

    data_dict.update({
        'type': 'location'
    })

    try:
        location = toolkit.get_action('group_create')(
            context,
            data_dict=data_dict)
    except (logic.NotFound) as e:
        raise toolkit.ValidationError("location %s" % e)

    return location
