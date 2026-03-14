# import threading
# import time
#
# thread_storage = threading.local()
#
# class MyClass:
#     def set_thread_variable(self, value, value1):
#         """Sets a variable unique to the current thread."""
#         thread_storage.my_variable = value
#         thread_storage.my_variable1 = value1
#         print(f"Thread {threading.current_thread().name} set my_variable to: {value}")
#
#     def get_thread_variable(self):
#         """Retrieves the variable for the current thread."""
#         # Access the variable, if it exists for this thread
#         value = thread_storage.my_variable + 1
#         value1 = thread_storage.my_variable1 + 1
#         print(hasattr(thread_storage, 'my_variable'))
#         print(f"Thread {threading.current_thread().name} retrieved my_variable: {value}")
#         print(f"Thread {threading.current_thread().name} retrieved my_variable: {value1}")
#         return value
#
# obj = MyClass()
# obj.set_thread_variable(1,2)
# obj.get_thread_variable()
#
# obj = MyClass()
# obj.get_thread_variable()
#
# import numpy as np
# arr = np.append(np.array([[1,2,3,4]]), np.empty((0,4)), axis=0)
# print(np.append(np.array([[4,3,2,1]]), arr, axis=0))
# print(np.hstack((np.array([1,2,3]), np.array([4]), np.array([5]))))

from multiprocessing import Process, Value
import threading

def nic(shared_bal):
    thread_storage = threading.local()
    thread_storage.bal1 = 0
    for i in range(100):
        thread_storage.bal1 += shared_bal
    print(thread_storage.bal1)

def seb(shared_bal):
    thread_storage = threading.local()
    thread_storage.bal2 = 100
    for i in range(100):
        thread_storage.bal2 += shared_bal
    print(thread_storage.bal2)

if __name__ == '__main__':
    p1 = Process(target=nic, args=(1,))
    p2 = Process(target=seb, args=(1,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # print(shared_bal.value)