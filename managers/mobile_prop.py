from db import database
from managers import BrandManager
from models import mobile_prop, mobile_prop_option, mobile_prop_selectable_value


class MobilePropManager:
    @staticmethod
    async def get_props_by_mobile(mobile_id):
        query = mobile_prop_selectable_value.select().where(
            mobile_prop_selectable_value.c.mobile_id == mobile_id)
        mobile_prop_selectable_values = await database.fetch_all(query)
        props = {}
        for mpsv in mobile_prop_selectable_values:
            prop_value_query = mobile_prop_option.select().where(mobile_prop_option.c.id == mpsv["prop_value_id"])
            prop_value = await database.fetch_one(prop_value_query)
            prop_query = mobile_prop.select().where(mobile_prop.c.id == prop_value["prop_id"])
            prop_key = await database.fetch_one(prop_query)
            props[prop_key["prop"]] = prop_value["value"]
        return props

    @staticmethod
    async def get_props():
        query = mobile_prop.select()
        prop_keys = await database.fetch_all(query)
        props = {"brand": await BrandManager.list_brand_for_filter()}
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

    @staticmethod
    async def get_props_by_ids(prop_ids):
        query = mobile_prop_selectable_value.select().where(mobile_prop_selectable_value.c.prop_value_id.in_(prop_ids))
        return await database.fetch_all(query)
