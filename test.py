import win32gui
import win32con
import time
import threading as th
import os
import time
time.sleep(2)

def print_GetForegroundWindow():
    hwnd_active = win32gui.GetForegroundWindow()
    print('hwnd_active hwnd:',hwnd_active)
    print('hwnd_active text:',win32gui.GetWindowText(hwnd_active))
    print('hwnd_active class:',win32gui.GetClassName(hwnd_active))

name = 'AntYecai'
hwnd = win32gui.FindWindow(None, name)
win32gui.BringWindowToTop(hwnd)
win32gui.SetForegroundWindow(hwnd)
win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
# win32gui.SetForegroundWindow(win32gui.FindWindow("UnityWndClass","AntYecai"))
# print_GetForegroundWindow()
# win32gui.ShowWindow(win32gui.FindWindow("UnityWndClass","AntYecai"), win32con.SW_SHOW)
# if hwnd == 0:
#     os.startfile('D:\\daily data\\AntYecaibuluo\\AntYecai.exe')

