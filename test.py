import pythoncom, pyWinhook

def OnKeyboardEvent(event):
    key = chr(event.KeyID)
    print(key)
    return True

hm = pyWinhook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
