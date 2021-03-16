"""
Example: Multiprocessing
"""

import time
import signal
from multiprocessing import Process, Event


stop_evt = Event()


class ServiceExit(Exception):
    """
    Exit Service
    """


def handle_signal(signum, frame):
    """
    Handling terminate signal
    """
    raise ServiceExit


def process():
    """
    Child process
    """
    print("Start child process")
    while not stop_evt.is_set():
        try:
            time.sleep(.01)
        except ServiceExit:
            break

    print("Stop child process")


if __name__ == '__main__':
    print("Start main process")

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    p = Process(target=process)
    p.start()

    while True:
        try:
            time.sleep(.01)
        except ServiceExit:
            print("Stop main process")
            stop_evt.set()
            break

    p.join()

    print("Exit successfully")
