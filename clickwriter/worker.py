import threading
from helpers import get_hwnd_by_title
from handlers import handle_click, handle_wait, handle_hold, handle_hclick, handle_drag, handle_harea, handle_random_point_on_line

running = False
thread_obj = None

COMMANDS = {
    "click": handle_click,
    "wait": handle_wait,
    "hold": handle_hold,
    "hclick": handle_hclick,
    "drag": handle_drag,
    "harea": handle_harea,
    "rline": handle_random_point_on_line,
}

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
    print("hwnd:", hwnd)

    while running:
        for line in lines:
            if line.startswith("#"):
                continue

            parts = line.split()
            cmd = parts[0]

            handler = COMMANDS.get(cmd)
            if handler is None:
                print("Unknown command:", line)
                continue

            handler(hwnd, parts)


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