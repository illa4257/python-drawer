# config

pencil = 3
# dot(defualt), lines, fast, fast2
mode = "fast2"
operations = 60
# win32api(default), pyautogui
mouseLib = "win32api"

# end

if mouseLib == "pyautogui":
    import pyautogui
else:
    import win32api, win32con

import math, time, keyboard, ctypes, datetime
from PIL import Image

ctypes.windll.shcore.SetProcessDpiAwareness(2)

t = 1 / operations

imgP = input("Image:\n")
img = Image.open(imgP).convert("RGBA")

area_start, area_end = [0, 0], [0, 0]
picker = []

def rArg(line):
    if "," in line:
        r = line[:line.index(",")]
        line = line[line.index(",") + 1:]
        return line, int(r)
    else:
        r = "0"
        if "\n" in line:
            r = line[:line.index("\n")]
        else:
            r = line
        return "", int(r)

with open("pos.txt", "r", encoding="utf-8") as h:
    lines = h.readlines()
    i = 0
    for line in lines:
        if i == 0:
            line = lines[i]
            line, area_start[0] = rArg(line)
            line, area_start[1] = rArg(line)
        elif i == 1:
            line = lines[i]
            line, area_end[0] = rArg(line)
            line, area_end[1] = rArg(line)
        else:
            line = lines[i]
            p = {}
            p["color"] = {}
            line, p["color"]["red"] = rArg(line)
            line, p["color"]["green"] = rArg(line)
            line, p["color"]["blue"] = rArg(line)
            line, p["x"] = rArg(line)
            line, p["y"] = rArg(line)
            picker.append(p)
        i = i + 1

def click(x,y):
    if mouseLib == "pyautogui":
        pyautogui.click(x, y)
    else:
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        time.sleep(t)

def move(x1,y1,x2,y2):
    if mouseLib == "pyautogui":
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2)
    else:
        win32api.SetCursorPos((x1,y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
        win32api.SetCursorPos((x2,y2))
        time.sleep(t)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y2,0,0)

width = area_end[0] - area_start[0]
height = area_end[1] - area_start[1]

w = math.floor(width / pencil) + 1
h = math.floor(height / pencil) + 1

pw = 1 / w
ph = 1 / h

def best(c):
    bc = None
    bs = 9999999
    for p in picker:
        d = math.sqrt(math.pow(p["color"]["red"] - c[0], 2) + math.pow(p["color"]["green"] - c[1], 2) + math.pow(p["color"]["blue"] - c[2], 2))
        if bc == None or bs > d:
            bc = p
            bs = d
    return bc

def setColor(p):
    click(p["x"], p["y"])

def convX(x):
    return area_start[0] + x * pencil

def convY(y):
    return area_start[1] + y * pencil

if mode == "fast":
    print("Preparing ...")
    colors = []
    for y in range(img.height):
        for x in range(img.width):
            col = best(img.getpixel((x, y)))
            if not col in colors:
                colors.append(col)
    input("Press enter, to continue ...")
    print("Painting ...")
    terminate = False
    for color in colors:
        if terminate:
            break
        setColor(color)
        for y in range(h):
            if terminate:
                break
            drawing = False
            sx = 0
            by = math.floor(y * ph * img.height)
            for x in range(w):
                if keyboard.is_pressed('c'):
                    terminate = True
                    break
                col = img.getpixel((math.floor(x * pw * img.width), by))
                if col[3] > 0 and best(col) == color:
                    if not drawing:
                        sx = x
                        drawing = True
                elif drawing:
                    if x - sx == 1:
                        click(convX(sx), convY(y))
                    else:
                        move(convX(sx), convY(y), convX(x - 1), convY(y))
                    drawing = False
            if drawing:
                if w - sx == 1:
                    click(convX(sx), convY(y))
                else:
                    move(convX(sx), convY(y), convX(w - 1), convY(y))
elif mode == "fast2":
    print("Preparing ...")
    terminate = False
    colors = []
    queue = []
    cc = None
    for y in range(h):
        if terminate:
            break
        drawing = False
        sx = 0
        by = math.floor(y * ph * img.height)
        for x in range(w):
            col = img.getpixel((math.floor(x * pw * img.width), by))
            if col[3] > 0:
                c = best(col)
                if not c in colors:
                    colors.append(c)
                    queue.append([])
                if cc != c:
                    if drawing:
                        queue[colors.index(cc)].append([sx, x, y])
                    cc = c
                    sx = x
                if not drawing:
                    sx = x
                    drawing = True
            elif drawing:
                queue[colors.index(cc)].append([sx, x, y])
                drawing = False
            if keyboard.is_pressed('c'):
                terminate = True
                break
        if drawing:
            queue[colors.index(cc)].append([sx, w, y])
    if terminate:
        exit
    input("Press enter, to continue ...")
    print("Painting ...")
    terminate = False
    for color in colors:
        if terminate:
            break
        pl = queue[colors.index(color)]
        print(f"Color: {colors.index(color) + 1}/{len(colors)}, actions: 0/{len(pl)}")
        setColor(color)
        a = 1
        l = datetime.datetime.now()
        for points in pl:
            if keyboard.is_pressed('c'):
                terminate = True
                break
            sx = points[0]
            x = points[1]
            y = points[2]
            if x - sx == 1:
                click(convX(sx), convY(y))
            else:
                move(convX(sx), convY(y), convX(x - 1), convY(y))
            a = a + 1
            n = datetime.datetime.now()
            if (n - l).seconds >= 1:
                print(f"Color: {colors.index(color) + 1}/{len(colors)}, actions: {a}/{len(pl)}")
                l = n
else:
    terminate = False
    cc = None
    for y in range(h):
        if terminate:
            break
        drawing = False
        sx = 0
        by = math.floor(y * ph * img.height)
        for x in range(w):
            col = img.getpixel((math.floor(x * pw * img.width), by))
            if mode == "dot":
                if col[3] > 0:
                    c = best(col)
                    if cc != c:
                        cc = c
                        setColor(c)
                    click(convX(x), convY(y))
            elif mode == "lines":
                if col[3] > 0:
                    c = best(col)
                    if cc != c:
                        if drawing:
                            if x - sx == 1:
                                click(convX(sx), convY(y))
                            else:
                                move(convX(sx), convY(y), convX(x - 1), convY(y))
                        cc = c
                        setColor(c)
                        sx = x
                    if not drawing:
                        sx = x
                        drawing = True
                elif drawing:
                    if x - sx == 1:
                        click(convX(sx), convY(y))
                    else:
                        move(convX(sx), convY(y), convX(x - 1), convY(y))
                    drawing = False
            if keyboard.is_pressed('c'):
                terminate = True
                break
        if mode == "lines" and drawing:
            if w - sx == 1:
                click(convX(sx), convY(y))
            else:
                move(convX(sx), convY(y), convX(w - 1), convY(y))