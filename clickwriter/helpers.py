import psutil
import win32gui
import win32con
import win32api
import win32process
import time
import random

# ------------------------------------------
# Get PID of a process by name
#
# process_name - name of the process executable
# ------------------------------------------
def get_pid(process_name):
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] and proc.info["name"].lower() == process_name.lower():
            return proc.info["pid"]
    return None

# ------------------------------------------
# Get main window handle from PID
#
# pid - process ID
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
#
# hwnd      - window handle
# rel_x/y   - relative coordinates within the window
# ------------------------------------------
def send_click(hwnd, rel_x, rel_y):
    lparam = win32api.MAKELONG(rel_x, rel_y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    time.sleep(0.05)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)

# ------------------------------------------
# Send hold to window via HWND
#
# hwnd      - window handle
# rel_x/y   - relative coordinates within the window
# hold_time - duration to hold the click (in seconds)
# ------------------------------------------
def send_hold(hwnd, rel_x, rel_y, hold_time):
    lparam = win32api.MAKELONG(rel_x, rel_y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    time.sleep(hold_time)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)


# ------------------------------------------
# Humanize Click
# Simulates a more human-like click by adding random variance
# to the click coordinates.
#
# hwnd        - window handle
# rel_x/y     - relative coordinates within the window
# variance    - maximum pixels to vary the click location
# ------------------------------------------
def human_click(hwnd, rel_x, rel_y, variance=3):
    var_x = random.randint(-variance, variance)
    var_y = random.randint(-variance, variance)

    final_x = rel_x + var_x
    final_y = rel_y + var_y

    print("Human Click at:", final_x, final_y)

    send_click(hwnd, final_x, final_y)


# ------------------------------------------
# Hold down and drag
# Simulates click-and-hold inside a window, then drags to a new location,
# without moving the real mouse.
# 
# hwnd        - window handle
# start_x/y   - starting relative coordinates
# end_x/y     - ending relative coordinates
# duration    - how long the drag should take
# steps       - how many increments to break the movement into
# ------------------------------------------
def hold_and_drag(hwnd, start_x, start_y, end_x, end_y, duration=0.5, steps=20):
    start_lparam = win32api.MAKELONG(start_x, start_y)

    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, start_lparam)
    
    time.sleep(0.5)

    step_delay = duration / steps
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps

    for i in range(1, steps + 1):
        new_x = int(start_x + dx * i)
        new_y = int(start_y + dy * i)
        move_lparam = win32api.MAKELONG(new_x, new_y)

        win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE,
                             win32con.MK_LBUTTON, move_lparam)

        time.sleep(step_delay)

    end_lparam = win32api.MAKELONG(end_x, end_y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, end_lparam)
    

# ------------------------------------------
# Random Point in Polygon
# Checks if a point is inside a polygon using the ray casting algorithm.
#
# x, y   - point coordinates
# poly   - list of (x, y) tuples defining the polygon vertices
# ------------------------------------------
def point_in_polygon(x, y, poly):
    num = len(poly)
    j = num - 1
    inside = False

    for i in range(num):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i

    return inside

# ------------------------------------------
# Random Point in Quadrilateral
# Generates a random point inside a quadrilateral defined by 4 points.
#
# p1, p2, p3, p4 - tuples defining the quadrilateral vertices
# ------------------------------------------
def random_point_in_quad(p1, p2, p3, p4):
    poly = [p1, p2, p3, p4]

    # Compute bounding box
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Random sampling until a valid point is found
    while True:
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        if point_in_polygon(x, y, poly):
            return x, y


# ------------------------------------------
# Click Random in Quadrilateral
# Clicks at a random point inside the quadrilateral defined by 4 points.
#
# hwnd          - window handle
# p1, p2, p3, p4 - tuples defining the quadrilateral vertices
# ------------------------------------------
def click_random_in_quad(hwnd, p1, p2, p3, p4):
    """
    Clicks at a random point inside the quadrilateral created by 4 points.
    
    Points must be tuples: (x, y)
    """

    x, y = random_point_in_quad(p1, p2, p3, p4)

    lparam = win32api.MAKELONG(x, y)

    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, lparam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)

    return (x, y)  # return clicked point if needed



# ------------------------------------------
# Get the Window HWND by Window Title
#
# title - exact window title
# ------------------------------------------
def get_hwnd_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    return hwnd if hwnd != 0 else None


# ------------------------------------------
# Get all Window Titles on the system
# ------------------------------------------
def list_open_windows():
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.strip():
                windows.append((hwnd, title))
        return True

    win32gui.EnumWindows(callback, None)
    return windows



