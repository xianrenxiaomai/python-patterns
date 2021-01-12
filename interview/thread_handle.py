import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List

"""
1、python起3个线程，循环切换线程打印0-9
"""

# pool
LOCK = threading.Lock()


def task(flag: int, queue: List[int], count: int, mod: int):
    while True:
        with LOCK:
            if count == len(queue):
                return
            if not queue:
                if flag == 0:
                    queue.append(0)
                    print(f"task-{flag} number:{0}")
            elif queue and (
                    (flag == 0 and queue[-1] % mod + 1 == mod)
                    or (flag != 0 and queue[-1] % mod + 1 == flag)
            ):
                temp_value = queue[-1] + 1
                print(f"task-{flag} number:{temp_value}")
                queue.append(temp_value)


def main():
    task_number = 3
    count = 10
    queue = list()
    pool = ThreadPoolExecutor(max_workers=task_number)
    for i in range(task_number):
        pool.submit(task, i, queue, count, task_number)

    pool.shutdown(wait=True)


main()

# event


event1 = threading.Event()
event2 = threading.Event()
event3 = threading.Event()
i = 0


def f1():
    global i
    while True:
        event1.wait()
        print("t1", i)
        i += 1
        event2.set()
        event1.clear()


def f2():
    global i
    while True:
        event2.wait()
        print("t2", i)
        i += 1
        event3.set()
        event2.clear()


def f3():
    global i
    while True:
        event3.wait()
        print("t3", i)
        i += 1
        event1.set()
        event3.clear()


if __name__ == '__main__':
    t1 = Thread(target=f1)
    t1.start()
    t2 = Thread(target=f2)
    t2.start()
    t3 = Thread(target=f3)
    t3.start()
    event1.set()
    t1.join()
    t2.join()
    t3.join()
