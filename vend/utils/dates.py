import calendar
from datetime import datetime, timedelta, date


class CalendarPeriod(object):

    @staticmethod
    def from_last_ndays(n):
        start = last_ndays(n, iso_fmt=False, as_date=False)
        end = datetime.now()
        return CalendarPeriod([start, end])

    @staticmethod
    def from_calendar_week(iso_year, iso_week):
        d = iso_to_gregorian(iso_year, iso_week, 1)
        dt = datetime.combine(d, datetime.min.time())

        start = dt.day
        max_day = calendar.monthrange(dt.year, dt.month)[1]
        end = min(start + 7, max_day+1)
        r = end - start
        w = [datetime(dt.year, dt.month, start+d) for d in range(r)]
        if r < 7:
            new_year = dt.year
            new_month = dt.month + 1
            if new_month > 12:
                new_month = 1
                new_year += 1
            r = 7 - r
            w.extend([datetime(new_year, new_month, d+1) for d in range(r)])
        return CalendarPeriod(w)

    def __init__(self, span):
        self.span = span
        return

    def __str__(self):
        return '%s - %s' % (self.starts, self.ends)

    @property
    def start(self):
        return self.span[0]

    @property
    def end(self):
        return self.span[-1]

    @property
    def starts(self):
        return self.start.date().isoformat()

    @property
    def ends(self):
        return self.end.date().isoformat()

    @property
    def timedelta(self):
        return tdiff(self.start, self.end)


def last_ndays(ndays, iso_fmt=True, as_date=True):
    dt = (datetime.now() - timedelta(ndays))
    if as_date:
        dt = dt.date()
    if iso_fmt:
        return dt.isoformat()
    return dt

def last_7days(iso_fmt=True):
    return last_ndays(7, iso_fmt)

def last_14days(iso_fmt=True):
    return last_ndays(14, iso_fmt)

def last_30days(iso_fmt=True):
    return last_ndays(30, iso_fmt)

def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + timedelta(days=iso_day-1, weeks=iso_week-1)

def today(iso_fmt=True):
    dt = datetime.now().date()
    if iso_fmt:
        return dt.isoformat()
    return dt

def to_datetime(datetime_str, fmt="%Y-%m-%d %H:%M:%S"):
    if datetime_str.find(' ') == -1:
        fmt = fmt.split(' ')[0]
    return datetime.strptime(datetime_str, fmt)

def to_date(*args, **kwargs):
    return to_datetime(*args, **kwargs).date()

def tdiff(d1, d2):
    # only takes strings atm but could be made to take date, time or
    # datetime objects as well
    if isinstance(d1, str):
        d1 = to_datetime(d1)
    if isinstance(d2, str):
        d2 = to_datetime(d2)
    return d2 - d1
