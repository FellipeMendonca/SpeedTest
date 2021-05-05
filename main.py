from datetime import datetime
from threading import Timer
from model import SpeedTest
from app import SpeedTestService

tests = []
tester = SpeedTestService()


def internet():
    print("start")
    test = SpeedTest(datetime.now(), tester.get_data_down(), tester.get_data_upload())
    print(test)
    tests.append(test)
    print("next")
    Timer(1, internet).start()


internet()
