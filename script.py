import psutil
import win32gui
import win32con
import win32api
import win32process
import time
import random

CLASH_PROCESS_NAME = "Clash of Clans - ShortKestrel35935"

# ------------------------------------------
# Get PID of a process by name
# ------------------------------------------
def get_pid(process_name):
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] and proc.info["name"].lower() == process_name.lower():
            return proc.info["pid"]
    return None

# ------------------------------------------
# Get main window handle from PID
# ------------------------------------------
def get_hwnd_from_pid(pid):
    hwnd_list = []

    def callback(hwnd, _):
        # Only consider visible windows with a title
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnd_list.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return hwnd_list[0] if hwnd_list else None

# ------------------------------------------
# Send click to window via HWND
# ------------------------------------------
def send_click(hwnd, x, y):
    lparam = win32api.MAKELONG(x, y)

    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    time.sleep(0.05)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)

# ------------------------------------------
# Get the Window HWND by Window Title
# ------------------------------------------
def get_hwnd_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    return hwnd if hwnd != 0 else None

# ------------------------------------------
# Example usage
# ------------------------------------------
if __name__ == "__main__":
    process_title = "Clash of Clans - ShortKestrel35935"
    hwnd = get_hwnd_by_title(process_title)

    while(True):
        window = win32gui.GetWindowRect(hwnd)

        left_bar_x = window[0]
        top_bar_y = window[1]
        right_bar_x = window[2]
        bottom_bar_y = window[3]

        # Click Attack button
        send_click(hwnd, left_bar_x + 20, bottom_bar_y - 150)

        time.sleep(random.uniform(2, 4))

        # Click Find a Match button
        send_click(hwnd, left_bar_x + 100, bottom_bar_y - 300)

        time.sleep(random.uniform(5, 7))
    



