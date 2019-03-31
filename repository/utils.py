from datetime import datetime


def datetime_to_epoch(datetime_: datetime) -> int:
    pass


def current_datetime_epoch() -> (datetime, int):
    datetime_ = datetime.now()
    return datetime_, int(datetime_.timestamp())
