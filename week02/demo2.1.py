import time
import threading

class WorkerThread(threading.Thread):
    def __init__(self, id,guard_duty:threading.Lock):
        super().__init__()
        self.identifier = id
        self.guard_duty = guard_duty
    
    def run(self):
        print(f"im starting {self.identifier}")
        self.guard_duty.acquire()
        print(f"guarding {self.identifier}")
        time.sleep(2)
        self.guard_duty.release()
        print(f"I'm done executing {self.identifier}")


def main():
    print("Main thread start")
    guard_duty = threading.Lock()
    t1 = WorkerThread(1, guard_duty)
    t2 = WorkerThread(2, guard_duty)
    print(t1.identifier)
    print(t2.identifier)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
