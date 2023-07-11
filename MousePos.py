import os, win32api, ctypes
from PIL import ImageGrab

ctypes.windll.shcore.SetProcessDpiAwareness(2)

handle = open("pos.txt", "w", encoding="utf-8")

os.system("cls")

input("Draw area start")
x, y = win32api.GetCursorPos()
print(f"X:{x}, Y:{y}")
handle.write(f"{x},{y}\n")

input("Draw area end")
x, y = win32api.GetCursorPos()
print(f"X:{x}, Y:{y}")
handle.write(f"{x},{y}")

cc = int(input("Count color:\n"))
i = 0
while i < cc:
    i = i + 1
    input(f"Color {i}/{cc}")
    x, y = win32api.GetCursorPos()
    scr = ImageGrab.grab().convert("RGB").load()
    c = scr[x, y]
    print(f"X: {x}, Y: {y} - RED: {c[0]}, GREEN: {c[1]}, BLUE: {c[2]}")
    handle.write(f"\n{c[0]},{c[1]},{c[2]},{x},{y}")

handle.close()