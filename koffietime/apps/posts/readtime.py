import re

# Average number of words a person can read in a minute.
WORDS_PER_MINUTE = 250


class ReadTime:
    """
    Calculate the time it takes to read a post.
    """

    def __init__(self, body):
        self.body = body

    def calculate_read_time(self):
        minutes_per_hour = 60
        hours_per_day = 24
        number_of_words = len(re.findall(r'\w+', self.body))
        time = round(number_of_words / WORDS_PER_MINUTE)
        if time < 1:
            return 'less than a minute read'
        if time == 1:
            return '1 minute read'
        if time >= minutes_per_hour:
            hours = round(time / minutes_per_hour)
            if hours >= hours_per_day:
                days = round(hours / hours_per_day)
                return '{} days read'.format(days)
            return '{} hours read'.format(hours)
        return '{} minutes read'.format(time)
