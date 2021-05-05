import speedtest


class SpeedTestService(object):
    def __init__(self):
        self.app = speedtest.Speedtest()
        self.app.get_servers()
        print(self.app.get_best_server())

    def get_data_down(self):
        speed = self.app.download(threads=None) * (10 ** -6)
        return speed

    def get_data_upload(self):
        speed = self.app.upload(threads=None) * (10 ** -6)
        return speed