import threading
from typing import List

"""
1、python起3个线程，循环切换线程打印0-9
"""
# 给线程起名

LOCK = threading.Lock()


def task(thread_name: int, queue: List[int], count: int = 10):
    while True:
        with LOCK:
            # current_thread = threading.current_thread()
            if count == len(queue):
                return
            if not queue:
                if thread_name == 0:
                    queue.append(0)
                    print(f"task-{thread_name} number:{0}")
            elif queue and (
                    #  根据队列最后一个数来判断整除
                    (thread_name == 0 and queue[-1] % 3 + 1 == 3)
                    #
                    or (thread_name != 0 and queue[-1] % 3 + 1 == thread_name)
            ):
                temp_value = queue[-1] + 1
                print(f"task-{thread_name} number:{temp_value}")
                queue.append(temp_value)


if __name__ == '__main__':
    task_number = 3
    count = 10
    queue = list()
    t1 = threading.Thread(target=task, args=(0, queue))
    t2 = threading.Thread(target=task, args=(1, queue))
    t3 = threading.Thread(target=task, args=(2, queue))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

# pool
# LOCK = threading.Lock()
#
#
# def task(thread_name: int, queue: List[int], count: int, mod: int):
#     while True:
#         with LOCK:
#             if count == len(queue):
#                 return
#             if not queue:
#                 if thread_name == 0:
#                     queue.append(0)
#                     print(f"task-{thread_name} number:{0}")
#             elif queue and (
#                     (thread_name == 0 and queue[-1] % mod + 1 == mod)
#                     or (thread_name != 0 and queue[-1] % mod + 1 == thread_name)
#             ):
#                 temp_value = queue[-1] + 1
#                 print(f"task-{thread_name} number:{temp_value}")
#                 queue.append(temp_value)
#
#
# def main():
#     task_number = 3
#     count = 10
#     queue = list()
#     pool = ThreadPoolExecutor(max_workers=task_number)
#     for i in range(task_number):
#         pool.submit(task, i, queue, count, task_number)
#
#     pool.shutdown(wait=True)
#
#
# main()

# event


# event1 = threading.Event()
# event2 = threading.Event()
# event3 = threading.Event()
# i = 0
#
#
# def f1():
#     global i
#     while True:
#         event1.wait()
#         print("t1", i)
#         i += 1
#         event2.set()
#         event1.clear()
#
#
# def f2():
#     global i
#     while True:
#         event2.wait()
#         print("t2", i)
#         i += 1
#         event3.set()
#         event2.clear()
#
#
# def f3():
#     global i
#     while True:
#         event3.wait()
#         print("t3", i)
#         i += 1
#         event1.set()
#         event3.clear()
#
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=f1)
#     t1.start()
#     t2 = threading.Thread(target=f2)
#     t2.start()
#     t3 = threading.Thread(target=f3)
#     t3.start()
#     event1.set()
#     t1.join()
#     t2.join()
#     t3.join()
