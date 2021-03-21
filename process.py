import multiprocessing
import time
import os


def test():
    a = 1 / 0
    return 1111


class LocalProcess(multiprocessing.Process):
    def __init__(self, fun_name, args=None, name=None, queue=None):
        super().__init__()
        self.fun_name = fun_name
        self.args = args
        self.daemon = True
        self.name = name
        self.queue = queue

    def run(self):
        try:
            res = self.fun_name() if self.args is None else self.fun_name(*self.args)
            code = 0
        except Exception as e:
            res = e
            code = 1
        if self.queue is not None:
            self.queue.put({"code": code, "name": self.name, "result": res})


if __name__ == '__main__':
    q = multiprocessing.Queue()
    p = LocalProcess(test, name="2",  queue=q)
    p.start()
    p.join()
    while q.qsize():
        print(q.get(False))
