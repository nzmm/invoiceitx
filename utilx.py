from datetime import datetime
from dateutil import tz

UTC_ZONE = tz.tzutc()
LC_ZONE = tz.tzlocal()


def toLocalTime(t, fmt='%Y-%m-%d %H:%M:%S'):
    utc = datetime.strptime(t, fmt)
    utc = utc.replace(tzinfo=UTC_ZONE)
    return utc.astimezone(LC_ZONE)

