# -*- coding: utf-8 -*-
import time
import threading
from queue import Queue

class MyThread(threading.Thread):
    def __init__(self, q):
        super(MyThread, self).__init__()
        self._q = q
        self._running = True
        self._input = False
        self._input_passwd = False

    def run(self):
        while self._running:
            if self._input:
                if self._input_passwd:
                    self._input_passwd = False
                    str0 = input("[INPUT] Password: ")
                    str0 = "thenextcontentisthepassword " + str0
                else:
                    str0 = input("[INPUT] Command: ")
                self._input = False
                self._q.put(str0)

    def stop(self):
        self._running = False

    def input_request(self):
        self._input = True
        self._input_passwd = False

    def input_passwd_request(self):
        self._input = True
        self._input_passwd = True
