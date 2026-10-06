from multiprocessing import *
from time import *

def print_text():
    num = 1
    while True:
        print(f"{num}: Hello.")
        num += 1
        sleep(1)

def main():
    while True:
        current_time = perf_counter()
        time_difference = current_time - timer_start

        if (time_difference>=5):
            print (f"Elapsed Time: {time_difference:0.4f}")
            raise TimeoutError

if __name__=="__main__":
    process1 = Process(target=print_text)
    global timer_start
    timer_start = perf_counter()
    process1.start()

    try:
        main()
    
    except TimeoutError:
        process1.terminate()
        print("Time's up")