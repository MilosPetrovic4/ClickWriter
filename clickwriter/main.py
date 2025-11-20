import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from helpers import get_hwnd_by_title, send_click, list_open_windows
from worker import start_worker, stop_worker
from tkinter import filedialog
import win32api, win32gui

# ------------------------------------------------------------
# Creates a popup allowing the user to select a window
# ------------------------------------------------------------
def open_window_selector():
    popup = tk.Toplevel(root)
    popup.title("Select a Window")
    popup.geometry("400x300")

    windows = list_open_windows()

    # Listbox to show windows
    listbox = tk.Listbox(popup, width=50)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for _, title in windows:
        listbox.insert(tk.END, f"{title}")

    def submit_selection():
        selected = listbox.curselection()
        if not selected:
            return

        value = listbox.get(selected[0])

        selected_title.set(value)
        print(selected_title.get())
        popup.destroy()

    # Submit Button
    submit_btn = ttk.Button(popup, text="Submit", command=submit_selection)
    submit_btn.pack(pady=10)


# ---------------- MAIN UI ---------------- #
root = tk.Tk()
root.title("Bot Setup")
root.geometry("400x700")

# ----- MENU BAR -----
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

def import_file():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        code_box.delete("1.0", "end")
        code_box.insert("1.0", content)

    except Exception as e:
        print("Error", f"Failed to open file:\n{e}")

def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save File As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        content = code_box.get("1.0", "end")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print("Error", f"Failed to save file:\n{e}")

file_menu.add_command(label="Import File", command=import_file)
file_menu.add_command(label="Save File", command=save_file)

# ------------ LABELS ------------ #
selected_title = tk.StringVar(value="No window selected")

result_label = tk.Label(root, textvariable=selected_title, wraplength=350)
result_label.pack(pady=10)

# ------------ BUTTONS ------------ #
select_button = ttk.Button(root, text="Select Window", command=open_window_selector)
select_button.pack(pady=20)

def start_process():
    start_worker(lambda: code_box.get("1.0", "end"), selected_title.get())

def stop_process():
    stop_worker()

def test_click():
    try:
        x = int(test_x_entry.get())
        y = int(test_y_entry.get())
    except ValueError:
        print("Invalid Input", "X and Y must be integers.")
        return

    hwnd = get_hwnd_by_title(selected_title.get())
    if not hwnd:
        print("No Window Selected", "Please select a window first.")
        return

    send_click(hwnd, x, y)  
    left, top, _, _ = win32gui.GetWindowRect(hwnd)
    win32api.SetCursorPos((left + x, top + y))
    print("Success", f"Clicked at ({x}, {y})")

tk.Button(root, text="Start", command=start_process).pack(pady=5)
tk.Button(root, text="Stop", command=stop_process).pack(pady=5)

# ------------ TEST CLICK SECTION ------------ #
test_frame = tk.LabelFrame(root, text="Test Click", padx=10, pady=10)
test_frame.pack(pady=15, fill="x")

tk.Label(test_frame, text="X:").grid(row=0, column=0, padx=5, pady=5)
test_x_entry = tk.Entry(test_frame, width=10)
test_x_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(test_frame, text="Y:").grid(row=0, column=2, padx=5, pady=5)
test_y_entry = tk.Entry(test_frame, width=10)
test_y_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Button(test_frame, text="Test Click", command=test_click).grid(
    row=0, column=5, columnspan=4, pady=10
)

# ------------ CODE EDITOR WITH LINE NUMBERS ------------ #
editor_frame = tk.Frame(root)
editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

code_font = tkfont.Font(family="Consolas", size=11)

line_numbers = tk.Text(editor_frame, width=4, padx=5, takefocus=0, 
                       border=0, background="#f0f0f0", state="disabled",
                       font=code_font)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(editor_frame, width=25)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

code_box = tk.Text(editor_frame, wrap="none", font=code_font,
                   yscrollcommand=scrollbar.set)
code_box.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=code_box.yview)

# Update line numbers when text changes
def update_line_numbers(event=None):
    code_box.update_idletasks()

    line_count = int(code_box.index('end-1c').split('.')[0])
    lines = "\n".join(str(i) for i in range(1, line_count + 1))

    line_numbers.config(state="normal")
    line_numbers.delete("1.0", tk.END)
    line_numbers.insert("1.0", lines)
    line_numbers.config(state="disabled")


code_box.bind("<KeyRelease>", update_line_numbers)

# Initialize line numbers
update_line_numbers()

# ------------ TK MAINLOOP ------------ #
root.mainloop()
