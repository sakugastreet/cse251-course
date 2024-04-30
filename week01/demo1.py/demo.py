from cse251 import *
import threading
print("hello world")

t1 = 1
t2 = dict()
t2["mykey"] = 12343
print(t2)
t3 = [1,23,45, 5, 6, 789]

def do_useful(param1=1, param2=2, param3=3):
    print(param1,param2, param3)

t4 = threading.Thread(target=do_useful, args=(1,))
t4.start()
t4.join()
t5 = threading.Thread(target=do_useful, args=(1,))
t5.start()
t5.join()
