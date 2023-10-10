from flask import request, abort
from functools import wraps
import datetime
import pexicdb
from pexicdb.fields import UUIDField, StringField
from .config import API_LIMIT_COUNT_FOR_1_MINUTE


requests_model = {
    "_id": UUIDField("_id"),
    "ipaddress": StringField("ipaddress"),
    "endpoint": StringField("endpoint"),
    "datetime": StringField("datetime")
}

db = pexicdb.connect("local_container", list(requests_model.values()),)


def get_ip_address():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    return request.environ['HTTP_X_FORWARDED_FOR']


def api_limiter(f):
    @wraps(f)
    def fun(*a, **kw):
        datetime_sub_60s = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
        current_user_ip_address = get_ip_address()

        requests_count = db.count(
            db.get([
                requests_model["datetime"].greater_than(datetime_sub_60s.isoformat()),
                requests_model["ipaddress"].equals(current_user_ip_address)
            ])
        )

        if requests_count >= API_LIMIT_COUNT_FOR_1_MINUTE:
            abort(429)

        db.insert({
            "ipaddress": current_user_ip_address,
            "endpoint": request.endpoint,
            "datetime": datetime.datetime.utcnow().isoformat()
        })

        return f(*a, **kw)

    return fun