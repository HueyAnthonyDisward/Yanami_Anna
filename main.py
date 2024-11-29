import multiprocessing
from init import assist
from engine.support import hotword

# To run VA
def startVA():
    # Code for process 1
    print("Process 1 is running...")
    assist()

# To run hotword
def startHotword():
    # Code for process 2
    print("Process 2 is running...")
    hotword()

# Start both processes
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startVA)
    p2 = multiprocessing.Process(target=startHotword)

    p1.start()
    p2.start()

    p1.join()
    if p2.is_alive():
        p2.terminate()
        p2.join()
    
    print("System stop!")
