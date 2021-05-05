from utils import DateTimeUtils


class SpeedTest(object):
    def __init__(self, time=None, speed_down=None, speed_up=None):
        self.time = time
        self.speed_down = speed_down
        self.speed_up = speed_up

    def __str__(self):
        return (
            "Date: "
            + DateTimeUtils.convert_datetime_str(
                self.time, DateTimeUtils.pattern_brazil_full
            )
            + " - Down: "
            + str(self.speed_down)
            + " - Up: "
            + str(self.speed_up)
        )
