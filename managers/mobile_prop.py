from db import database
from models import mobile_prop, mobile_prop_option


class MobilePropManager:
    @staticmethod
    async def get_props():
        query = mobile_prop.select()
        prop_keys = await database.fetch_all(query)
        props = {}
        for prop_key in prop_keys:
            mobile_prop_options_query = mobile_prop_option.select().where(
                mobile_prop_option.c.prop_id == prop_key["id"])
            mobile_prop_option_instances = await database.fetch_all(mobile_prop_options_query)
            options = []
            for mobile_prop_option_instance in mobile_prop_option_instances:
                option = {
                    "id": mobile_prop_option_instance["id"],
                    "option": mobile_prop_option_instance["value"]
                }
                options.append(option)
            props[prop_key["prop"]] = options
        return props
