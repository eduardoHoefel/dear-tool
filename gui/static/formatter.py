from datetime import timedelta

class Formatter():

    def timedelta_to_string(time):
        return str(timedelta(seconds=int(time)))

