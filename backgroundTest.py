import win32api
import win32con
import win32gui
import cv
hwnd = win32gui.FindWindow(None, 'MuMu模拟器12')

# 获取窗口位置
rect = win32gui.GetWindowRect(hwnd)
print(rect)

for x in range(rect[0], rect[2]):
    for y in range(rect[1], rect[3]):
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, y << 16 | x)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, y << 16 | x)
        print("点击",x,":",y)
