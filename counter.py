#!/bin/python3

import tkinter as tk

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
    
    def setText(self,text):
        self.text = text

def close():
    root.destroy()
    listener.stop()

def onClick(event):
    global lastClick
    lastClick = [ event.x, event.y ]

def onDrag(event):
    global lastClick
    delta = [ event.x - lastClick[0], event.y - lastClick[1] ]
    root.geometry(f'+{root.winfo_x()+delta[0]}+{root.winfo_y()+delta[1]}')

def onUnClick(event):
    global lastClick
    lastClick = None
    save()

count = 0
quantity = 5
scentKey = None
setKey = 0
last = [0] * 50
undoPoint = 0
modifier = False
altMod = False
shiftMod = False
superMod = False
pause = False

def plusOne():
    inc(1)
def minusOne():
    dec(1)
def plusQuant():
    inc(quantity)
def minusQuant():
    dec(quantity)
def undo():
    global count, last, undoPoint, undoButton
    count += last[undoPoint]
    undoPoint -= 1
    if undoPoint < 0:
        undoPoint = 0
        last[undoPoint] = 0
    if undoPoint == 0 and last[undoPoint] == 0:
        undoButton["state"] = "disabled"
    save()
def togglePause():
    global pause, plusButton, minusButton, undoButton, configButton, resetButton
    pause = not pause
    if pause:
        print('\nInput is being paused! Press Alt+Esc to resume!')
        label.config(text='PAUSED')
        labeltip.setText('Input is being paused!\nPress Alt+Esc to resume!')
        plusButton["state"] = "disabled"
        minusButton["state"] = "disabled"
        undoButton["state"] = "disabled"
        configButton["state"] = "disabled"
        resetButton["state"] = "disabled"
        root.configure(bg='red')
        label.configure(bg='red')
        plusButton.configure(bg='red')
        minusButton.configure(bg='red')
        configButton.configure(bg='red')
        resetButton.configure(bg='red')
        pauseButton.configure(bg='red')
        undoButton.configure(bg='red')
        exitButton.configure(bg='red')
    else:
        print('\nInput is now resumed!')
        if count < 10:
            label.config(text='{:,} '.format(count))
        else:
            label.config(text='{:,}'.format(count))
        labeltip.setText(f'Horde quantity: {quantity}\nSweet Scent Key: {scentKey}')
        plusButton["state"] = "normal"
        minusButton["state"] = "normal"
        configButton["state"] = "normal"
        resetButton["state"] = "normal"
        if undoPoint > 0 or last[undoPoint] != 0:
            undoButton["state"] = "normal"
        root.configure(bg='grey')
        label.configure(bg='grey')
        plusButton.configure(bg='grey')
        minusButton.configure(bg='grey')
        configButton.configure(bg='grey')
        resetButton.configure(bg='grey')
        pauseButton.configure(bg='grey')
        undoButton.configure(bg='grey')
        exitButton.configure(bg='grey')
    root.update()
def configure():
    global setKey
    print('\nPlease press your Sweet Scent key!')
    label.config(text='Press your Sweet Scent keybind!')
    labeltip.setText('Press the key you have bound to activate Sweet Scent.')
    root.update_idletasks()
    root.geometry(f'{label.winfo_reqwidth()+30}x{root.winfo_height()}')
    root.update_idletasks()
    exitButton.place(x=root.winfo_width()-exitButton.winfo_reqwidth(),y=0)
    root.update()
    setKey = 1
def reset():
    dec(count)

root = tk.Tk()
root.attributes('-topmost', True)
root.overrideredirect(True)
root.title('enCounter')
root.resizable(False, False)
#root.attributes('-alpha', 0.5)
root.configure(bg='grey')
root.bind('<ButtonPress-1>', onClick)
root.bind('<ButtonRelease-1>', onUnClick)
root.bind('<B1-Motion>', onDrag)
pixelVirtual = tk.PhotoImage(width=1, height=1)

exitButton = tk.Button(text='×', image=pixelVirtual, width=1, height=7, compound='c', command=close, bg='grey', fg='white', activebackground='black', activeforeground='white')
#exitButton.pack(side='top', anchor='ne')
#exitButton.grid(row=0, column=2, sticky='e', ipadx=0)
exitTip = CreateToolTip(exitButton,'Exit')

tk.Label(text='').grid(row=0, column=0)

label = tk.Label(text='{:,}'.format(count), bg='grey', fg='white')
label.place(x=1,y=0)
#label.grid(row=0, column=0, columnspan=2, sticky='w', ipadx=0)
labeltip = CreateToolTip(label,f'Horde quantity: {quantity}\nSweet Scent Key: {scentKey}')
print(f'{label.winfo_reqwidth()}')
pauseButton = tk.Button(text='⏸︎', image=pixelVirtual, width=1, height=7, compound='c', command=togglePause, bg='grey', fg='white', activebackground='black', activeforeground='white')
#pauseButton.pack(side='left')
pauseButton.grid(row=2, column=1, sticky='w', ipadx=0)
CreateToolTip(pauseButton,'Pause\nAlt+Esc')
plusButton = tk.Button(text='+', image=pixelVirtual, width=1, height=7, compound='c', command=plusOne, bg='grey', fg='white', activebackground='black', activeforeground='white')
#plusButton.pack(side='left')
plusButton.grid(row=1, column=0, sticky='w', ipadx=0)
CreateToolTip(plusButton,"Increase count\nCtrl+'+' or Ctrl+'='\nTo increase count by horde count press\nCtrl+'*' or Ctrl+8")
minusButton = tk.Button(text='-', image=pixelVirtual, width=1, height=7, compound='c', command=minusOne, bg='grey', fg='white', activebackground='black', activeforeground='white')
#minusButton.pack(side='left')
minusButton.grid(row=1, column=1, sticky='w', ipadx=0)
CreateToolTip(minusButton,"Decrease count\nCtrl+'-'\nTo decrease count by horde count press\nCtrl+'/'")
#plusQButton = tk.Button(text='+H', image=pixelVirtual, width=1, height=7, compound='c', command=plusQuant)
#plusQButton.pack(side='left')
#minusQButton = tk.Button(text='-H', image=pixelVirtual, width=1, height=7, compound='c', command=minusQuant)
#minusQButton.pack(side='left')
undoButton = tk.Button(text='Undo', image=pixelVirtual, width=15, height=7, compound='c', command=undo, bg='grey', fg='white', activebackground='black', activeforeground='white')
#undoButton.pack(side='left')
undoButton.grid(row=1, column=2, sticky='w', ipadx=0)
CreateToolTip(undoButton,'Ctrl+Z')
configButton = tk.Button(text='⚙', image=pixelVirtual, width=1, height=7, compound='c', command=configure, bg='grey', fg='white', activebackground='black', activeforeground='white')
#configButton.pack(side='left')
configButton.grid(row=2, column=0, sticky='w', ipadx=0)
CreateToolTip(configButton,'Configure\nCtrl+Esc')
resetButton = tk.Button(text='Reset', image=pixelVirtual, width=15, height=7, compound='c', command=reset, bg='grey', fg='white', activebackground='black', activeforeground='white')
resetButton.grid(row=2, column=2, sticky='w', ipadx=0)
CreateToolTip(resetButton,'Click this to reset your count to 0.\nOnly do this when you encounter a shiny!\nCan be undone ;p')

undoButton["state"] = "disabled"

root.update_idletasks()
winWidth = root.winfo_width()
exitCoord = winWidth-exitButton.winfo_reqwidth()
exitButton.place(x=exitCoord,y=0)

try:
    from encounters import *
except Exception as e:
    from pynput import keyboard
    setKey = 1
    wingeo = '+10+20'
    print('No config file found . . .\nPlease press your Sweet Scent key!')
    label.config(text='Press your Sweet Scent keybind!')
    labeltip.setText('Press the key you have bound to activate Sweet Scent.')
    root.update_idletasks()
    root.geometry(f'{label.winfo_reqwidth()+30}x{root.winfo_height()}')
    root.update_idletasks()
    exitButton.place(x=root.winfo_width()-exitButton.winfo_reqwidth(),y=0)

if isinstance(scentKey,str):
    scentKey = keyboard.KeyCode(char=scentKey)

root.geometry(wingeo)

if setKey == 0:
    print(f'enCounter started . . .\nCurrent horde quantity: {quantity}\nCurrent encounter count: {count}\n')
    #label.config(text=f'{count}')
    if count < 10:
        label.config(text='{:,} '.format(count))
    else:
        label.config(text='{:,}'.format(count))
    labeltip.setText(f'Horde quantity: {quantity}\nSweet Scent Key: {scentKey}')
    root.update_idletasks()
    root.geometry(f'{winWidth}x{root.winfo_height()}')
    root.update_idletasks()
    exitButton.place(x=exitCoord,y=0)
    #plusQButton.config(text=f'+{quantity}')
    #minusQButton.config(text=f'-{quantity}')

def save():
    if setKey == 0:
        file = open('encounters.py', 'w')
        try:
            file.write(f'#!/bin/python3\nfrom pynput import keyboard\nquantity = {quantity}\ncount = {count}\nscentKey = \'{scentKey.char}\'\nwingeo = "+{root.winfo_x()}+{root.winfo_y()}"')
        except AttributeError:
            file.write(f'#!/bin/python3\nfrom pynput import keyboard\nquantity = {quantity}\ncount = {count}\nscentKey = keyboard.{scentKey}\nwingeo = "+{root.winfo_x()}+{root.winfo_y()}"')
        file.close()
        print(f'Count: {count}')
        if not pause:
            if count < 10:
                label.config(text='{:,} '.format(count))
            else:
                label.config(text='{:,}'.format(count))
            labeltip.setText(f'Horde quantity: {quantity}\nSweet Scent Key: {scentKey}')
        root.update()

def inc(n):
    global count, last, undoPoint, undoButton
    count += n
    undoPoint += 1
    if undoPoint > 49:
        last.pop(0)
        last.append(n*-1)
        undoPoint = 49
    else:
        last[undoPoint] = n*-1
    if undoButton["state"] == "disabled":
        undoButton["state"] = "normal"
    save()

def dec(n):
    global count, last, undoPoint, undoButton
    count -= n
    undoPoint += 1
    if undoPoint > 49:
        last.pop(0)
        last.append(n*-1)
        undoPoint = 49
    else:
        last[undoPoint] = n
    if undoButton["state"] == "disabled":
        undoButton["state"] = "normal"
    save()

def on_press(key):
    global modifier, scentKey, setKey, altMod, shiftMod, superMod, undoButton
    if pause == False and modifier == True and altMod == False and shiftMod == False and superMod == False:
        if key == keyboard.KeyCode(char='+') or key == keyboard.KeyCode(char='='):
            inc(1)
        elif key == keyboard.KeyCode(char='*') or key == keyboard.KeyCode(char='8'):
            inc(quantity)
        elif key == keyboard.KeyCode(char='-'):
            dec(quantity)
        elif key == keyboard.KeyCode(char='/'):
            dec(1)
        elif key == keyboard.KeyCode(char='z'):
            if undoPoint == 0 and last[undoPoint] == 0:
                print('Nothing to undo!')
                undoButton["state"] = "disabled"
            else:
                undo()
        elif key == keyboard.Key.esc:
            configure()
        elif key == keyboard.KeyCode(char='h'):
            print('\nPlease press the single digit number corresponding to the horde count you are shunting!')
            label.config(text='Enter the number of encounters per horde!')
            labeltip.setText('Press a single digit number corresponding to the horde count you are shunting.')
            root.update_idletasks()
            root.geometry(f'{label.winfo_reqwidth()+30}x{root.winfo_height()}')
            root.update_idletasks()
            exitButton.place(x=root.winfo_width()-exitButton.winfo_reqwidth(),y=0)
            root.update()
            setKey = 2
    elif modifier == False and altMod == True and shiftMod == False and superMod == False:
        if key == keyboard.Key.esc:
            togglePause()
    if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        modifier = True
    elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr:
        altMod = True
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
        shiftMod = True
    elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
        superMod = True

def on_release(key):
    global modifier, scentKey, setKey, quantity, altMod, shiftMod, superMod
    if pause == False and modifier == False and altMod == False and shiftMod == False and superMod == False:
        if setKey == 1:
            scentKey = key
            print('\nPlease press the single digit number corresponding to the horde count you are shunting!')
            label.config(text='Enter the number of encounters per horde!')
            labeltip.setText('Press a single digit number corresponding to the horde count you are shunting.')
            root.update_idletasks()
            root.geometry(f'{label.winfo_reqwidth()+30}x{root.winfo_height()}')
            root.update_idletasks()
            exitButton.place(x=root.winfo_width()-exitButton.winfo_reqwidth(),y=0)
            root.update()
            setKey = 2
        elif setKey == 2:
            try:
                keyChar = key.char
            except AttributeError:
                keyChar = 'n'
            if keyChar.isdigit():
                quantity = int(keyChar)
                print(f'\nenCounter started . . .\nCurrent horde quantity: {quantity}\nCurrent encounter count: {count}\n')
                if count < 10:
                    label.config(text='{:,} '.format(count))
                else:
                    label.config(text='{:,}'.format(count))
                labeltip.setText(f'Horde quantity: {quantity}\nSweet Scent Key: {scentKey}')
                root.update_idletasks()
                root.geometry(f'{winWidth}x{root.winfo_height()}')
                exitButton.place(x=exitCoord,y=0)
                #plusQButton.config(text=f'+{quantity}')
                #minusQButton.config(text=f'-{quantity}')
                root.update()
                setKey = 0
            else:
                print('\nPlease enter a valid number!')
                label.config(text='Enter the number of encounters per horde! Please enter a valid number!')
                labeltip.setText('Press a single digit number corresponding to the horde count you are shunting.')
                root.update_idletasks()
                root.geometry(f'{label.winfo_reqwidth()+30}x{root.winfo_height()}')
                root.update_idletasks()
                exitButton.place(x=root.winfo_width()-exitButton.winfo_reqwidth(),y=0)
                root.update()
        elif key == scentKey:
            inc(quantity)
    if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        modifier = False
    elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr:
        altMod = False
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
        shiftMod = False
    elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
        superMod = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    root.mainloop()
    listener.join()
