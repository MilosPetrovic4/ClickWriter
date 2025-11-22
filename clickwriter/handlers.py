from helpers import send_click, human_click, hold_and_drag, send_hold, click_random_in_quad
import time, random


# ------------------------------------------------------------
# handle click command
#
# hwnd - window handle
# parts - list of command parts
# ------------------------------------------------------------
def handle_click(hwnd, parts):
    if len(parts) != 3:
        print("Invalid click command:", parts)
        return
    try:
        x = int(parts[1])
        y = int(parts[2])
    except ValueError:
        print("Click command contains non-integer values:", parts)
        return

    send_click(hwnd, x, y)


# ------------------------------------------------------------
# handle waiting command
#
# parts - list of command parts
# ------------------------------------------------------------
def handle_wait(_, parts):
    if len(parts) != 3:
        print("Invalid wait command: ", parts)
        return
    try:
        t_min = float(parts[1])
        t_max = float(parts[2])
    except ValueError:
        print("Wait command contains non-float values: ", parts)
        return

    time.sleep(random.uniform(t_min, t_max))


# ------------------------------------------------------------
# handle random point on line command
#
# hwnd - window handle
# parts - list of command parts
# ------------------------------------------------------------
def handle_random_point_on_line(hwnd, parts):
    if len(parts) != 5:
        print("Invalid hold command: ", parts)
        return
    try:
        x1 = int(parts[1])
        y1 = int(parts[2])
        x2 = int(parts[3])
        y2 = int(parts[4])
    except ValueError:
        print("Hold command contains invalid values: ", parts)
        return

    t = random.random()
    x = int(x1 + t * (x2 - x1))
    y = int(y1 + t * (y2 - y1))

    send_click(hwnd, x, y)

# ------------------------------------------------------------
# handle hold command
#
# hwnd - window handle
# parts - list of command parts
# ------------------------------------------------------------
def handle_hold(hwnd, parts):
    if len(parts) != 4:
        print("Invalid hold command: ", parts)
        return
    try:
        x = int(parts[1])
        y = int(parts[2])
        t = float(parts[3])
    except ValueError:
        print("Hold command contains invalid values: ", parts)
        return

    send_hold(hwnd, x, y, t)


# ------------------------------------------------------------
# handle harea command
#
# hwnd - window handle
# parts - list of command parts
# ------------------------------------------------------------
def handle_harea(hwnd, parts):
    """
    Expected format:
    harea x1 y1 x2 y2 x3 y3 x4 y4
    """
    if len(parts) != 9:
        print("Invalid harea command:", parts)
        return

    try:
        coords = list(map(int, parts[1:]))
    except ValueError:
        print("harea command invalid numeric values:", parts)
        return

    p1 = (coords[0], coords[1])
    p2 = (coords[2], coords[3])
    p3 = (coords[4], coords[5])
    p4 = (coords[6], coords[7])

    click_random_in_quad(hwnd, p1, p2, p3, p4)


# ------------------------------------------------------------
# handle humanized click command
#
# hwnd - window handle
# parts - list of command parts
# ------------------------------------------------------------
def handle_hclick(hwnd, parts):
    if len(parts) != 4:
        print("Invalid hclick command:", parts)
        return
    try:
        x = int(parts[1])
        y = int(parts[2])
        variance = int(parts[3])
    except ValueError:
        print("hclick command invalid values:", parts)
        return

    human_click(hwnd, x, y, variance)


# ------------------------------------------------------------
# handle drag command
#
# hwnd - window handle
# parts - list of command parts
# ------------------------------------------------------------
def handle_drag(hwnd, parts):
    if len(parts) != 6:
        print("Invalid drag command:", parts)
        return

    try:
        sx = int(parts[1])
        sy = int(parts[2])
        ex = int(parts[3])
        ey = int(parts[4])
        duration = float(parts[5])
    except ValueError:
        print("Drag command invalid values:", parts)
        return

    hold_and_drag(hwnd, sx, sy, ex, ey, duration)