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
        prop_values = await database.fetch_all(query)
        prop_option_ids = [prop_value["prop_value_id"] for prop_value in prop_values]
        prop_options = await database.fetch_all(
            mobile_prop_option.select().where(mobile_prop_option.c.id.in_(prop_option_ids)))
        prop_ids = set([prop_option["prop_id"] for prop_option in prop_options])
        return {"prop_values": prop_values, "prop_count": len(prop_ids)}

    @staticmethod
    async def create_props(prop_data):
        prop_query = mobile_prop.insert(**prop_data)
        prop_id = await database.execute(prop_query)
        is_selectable = prop_data["is_selectable"]
        prop_data_response = prop_data.copy()
        prop_data_response["id"] = prop_id
        if is_selectable:
            options = prop_data["options"]
            option_ids = []
            for option in options:
                option_query = mobile_prop_option.values().insert({"prop_id": prop_id, "value": option})
                option_id = await database.execute(option_query)
                option_ids.append(option_id)
            prop_data_response["options"] = option_ids
        return prop_data_response
