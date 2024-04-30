import logging
import threading
import time

def thread_function(name, sleep_time):
    """This is the function the thread will run"""
    print(f"Thread {name}: starting")
    time.sleep(sleep_time)
    print(f"Thread {name}: finishing")


if __name__ == "__main__":
    print("Main     : before creating thread")


    t = threading.Thread(target=thread_function, args=("Sleep Function", 2))

    print("Main     : before running thread")



    t.start()
    
    print("Main    : wait for thread to finish")


    t.join()



    print("Main    : all done")