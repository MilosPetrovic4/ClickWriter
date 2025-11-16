import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import win32gui
from helpers import get_hwnd_by_title, send_click, list_open_windows
from worker import start_worker, stop_worker

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

    for hwnd, title in windows:
        listbox.insert(tk.END, f"{title}")

    def submit_selection():
        selected = listbox.curselection()
        if not selected:
            return

        value = listbox.get(selected[0])

        selected_title.set(value)
        popup.destroy()

    # Submit Button
    submit_btn = ttk.Button(popup, text="Submit", command=submit_selection)
    submit_btn.pack(pady=10)


# ---------------- MAIN UI ---------------- #
root = tk.Tk()
root.title("Bot Setup")
root.geometry("400x700")

# ------------ LABELS ------------ #
selected_title = tk.StringVar(value="No window selected")

label = tk.Label(root, text="Selected Window:")
label.pack(pady=10)

result_label = tk.Label(root, textvariable=selected_title, wraplength=350)
result_label.pack(pady=10)

# ------------ BUTTONS ------------ #
select_button = ttk.Button(root, text="Select Window", command=open_window_selector)
select_button.pack(pady=20)

def start_process():
    start_worker(lambda: code_box.get("1.0", "end"), selected_title.get())

def stop_process():
    stop_worker()

tk.Button(root, text="Start", command=start_process).pack(pady=5)
tk.Button(root, text="Stop", command=stop_process).pack(pady=5)

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
