import time
import threading
import random
from helpers import get_hwnd_by_title, send_click, send_hold

running = False
thread_obj = None


# ------------------------------------------------------------
# Instruction runner, runs in a background thread
# ------------------------------------------------------------
def click_loop(get_code_callback, window_title):
    global running
    raw_code = get_code_callback()
    
    lines = [
        line.strip().lower()
        for line in raw_code.split("\n")
        if line.strip()
    ]

    hwnd = get_hwnd_by_title(window_title)

    print("hwnd: ", hwnd)

    while running:
        for line in lines:
            if line.startswith("click"):
                parts = line.split()

                if len(parts) != 3:
                    print("Invalid click command:", line)
                    continue
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    print("Click command contains non-integer values:", line)
                    continue

                send_click(hwnd, x, y)
            
            elif line.startswith("wait"):
                parts = line.split()

                if len(parts) != 3:
                    print("Invalid wait command:", line)
                    continue
                try:
                    wait_time_min = float(parts[1])
                    wait_time_max = float(parts[2])
                except ValueError:
                    print("Wait command contains non-float values:", line)
                    continue
                
                wait_time = random.uniform(wait_time_min, wait_time_max)
                time.sleep(wait_time)

            elif line.startswith("hold"):
                parts = line.split()

                if len(parts) != 4:
                    print("Invalid hold command:", line)
                    continue
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                    hold_time = float(parts[3])
                except ValueError:
                    print("Hold command contains non-integer/float values:", line)
                    continue

                send_hold(hwnd, x, y, hold_time)

            time.sleep(1)


# ------------------------------------------------------------
# Start worker loop in new thread
# ------------------------------------------------------------
def start_worker(get_code_callback, window_title):
    global running, thread_obj
    if running:
        print("Worker already running.")
        return

    running = True
    thread_obj = threading.Thread(
        target=click_loop,
        args=(get_code_callback, window_title,),
        daemon=True
    )
    thread_obj.start()


# ------------------------------------------------------------
# Stop worker thread loop
# ------------------------------------------------------------
def stop_worker():
    global running
    running = False