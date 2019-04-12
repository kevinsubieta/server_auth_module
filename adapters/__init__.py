from datetime import date, datetime
from typing import List


def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def create_obj(class_, values: dict, keys: List[str]):
    obj = class_()
    for key in values:
        if key in keys:
            setattr(obj, key, values[key])
    return obj