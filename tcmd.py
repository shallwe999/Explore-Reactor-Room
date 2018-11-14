import time
import threading
from queue import Queue

class MyThread(threading.Thread):
    def __init__(self, q):
        super(MyThread, self).__init__()
        self.q = q
        self.running = True
        self.input = False

    def run(self):
        while self.running:
            if self.input:
                str0 = input("Command: ")
                self.input = False
                self.q.put(str0)

    def stop(self):
        self.running = False

    def input_request(self):
        self.input = True


