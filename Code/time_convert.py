from datetime import datetime
from dateutil import tz, parser

class TimeConvert:

    def __init__(self):
        # tup_months_full = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
        #  "November", "December")

        self.tup_months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


    def to_local_raw(self, date_time_git):
        # Auto-detect zones:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        date_git = str(date_time_git[0:10])
        time_git = str(date_time_git[11:19])
        date_time_utc = date_git + " " + time_git

        utc = datetime.strptime(date_time_utc, '%Y-%m-%d %H:%M:%S')

        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        time_here = str(utc.astimezone(to_zone))
        time_here = parser.parse(time_here)

        return str(time_here.year)[0:4] + "-" + str(time_here.month).zfill(2) + "-" + str(time_here.day).zfill(2) + " " \
               + str(time_here.hour).zfill(2) + ":" + str(time_here.minute).zfill(2) + ":" + str(time_here.second).zfill(2)
    pass


    def to_local(self, date_time_git):
        # Auto-detect zones:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        date_git = str(date_time_git[0:10])
        time_git = str(date_time_git[11:19])
        date_time_utc = date_git + " " + time_git

        utc = datetime.strptime(date_time_utc, '%Y-%m-%d %H:%M:%S')

        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        time_here = str(utc.astimezone(to_zone))
        time_here = parser.parse(time_here)

        return self.tup_months[time_here.month - 1] + " " + str(time_here.day).zfill(2) + "/" + str(time_here.year)[1:4] + " "\
               + str(time_here.hour).zfill(2) + ":" + str(time_here.minute).zfill(2) + ":" + str(time_here.second).zfill(2)
    pass

    def compare_time(self, commit_date):
        today = datetime.today()
        commit_date = datetime(int(commit_date[0:4]), int(commit_date[5:7]), int(commit_date[8:10]),
                                        int(commit_date[11:13]), int(commit_date[14:16]), int(commit_date[17:19]));
        time_delta = today - commit_date
        return time_delta.days
    pass

    def get_days_back_from_today(self, UNIX_Timestamp):
        datetime_now = datetime.now()
        date_time_back = datetime.fromtimestamp(int(UNIX_Timestamp))
        diff_days = (datetime_now - date_time_back).days
        return diff_days

    def time_stamp_to_human(self, UNIX_Timestamp):
        dateNtime = datetime.fromtimestamp(UNIX_Timestamp)
        return (str(dateNtime.date()) + "T" + str(dateNtime.time()))