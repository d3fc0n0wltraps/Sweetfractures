import os, time, pygame
from tkinter import *
from datetime import datetime
try:
    import RPi.GPIO as GPIO
except ImportError:pass

fasterText = "Decrease strobe rate"
slowerText = "Increase strobe rate"
intChangeBy = 1000
intOldRate = 100000
intNewRate = 0
startTime = datetime.now()
deltaT = 0


class dev_DashBoard:
    def __init__(self, master):
        fm = Frame(master)
        btnFasterStrobe = Button(fm, text=fasterText, command = self.increaseStrobe)
        btnFasterStrobe.pack(side=TOP, anchor=W, fill=X, expand=YES)
        self.lblStrobeRate = Label(fm, text=f'Strobe Rate: {intOldRate}')
        self.lblStrobeRate.pack(side=TOP, anchor=W, fill=X, expand=YES)
        btnSlowerStrobe = Button(fm, text=slowerText, command = self.decreaseStrobe)
        btnSlowerStrobe.pack(side=TOP, anchor=W, fill=X, expand=YES)
        btnButton = Button(fm, text='Left', command = self.controlStrobe)
        btnButton.pack(side=LEFT)
        self.lblMS = Label(fm, text=f'Off')
        self.lblMS.pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)
        fm.pack(fill=BOTH, expand=YES)

    def increaseStrobe(self):
        global intOldRate
        global intNewRate
        global intChangeBy
        intNewRate = intOldRate+intChangeBy
        print(f'strobe increased from {intOldRate} to {intNewRate}')
        intOldRate = intNewRate
        self.lblStrobeRate.config(text=f'Strobe Rate: {intNewRate}')

    def decreaseStrobe(self):
        global intOldRate
        global intNewRate
        global intChangeBy
        if intOldRate > 0:
            intNewRate = intOldRate-intChangeBy
            print(f'strobe decreased from {intOldRate} to {intNewRate}')
            intOldRate = intNewRate
            self.lblStrobeRate.configure(text=f'Strobe Rate: {intNewRate}')
        else:
            print('Strobe cannot be decreased beyond zero')

    def controlStrobe(self):
        global startTime
        currentTime = datetime.now()
        deltaT = currentTime - startTime
        ms = deltaT.microseconds
        self.lblMS.configure(text=f'{ms} MS')


root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Strobe Dashboard")
root.geometry("250x140")
display = dev_DashBoard(root)

def my_mainloop():
    global startTime
    currentTime = datetime.now()
    deltaT = currentTime - startTime
    ms = deltaT.microseconds
    if ms > intOldRate:
        display.lblMS["text"] = f'On'
    if ms > (intOldRate*2):
        display.lblMS["text"] = f'Off'
        startTime = datetime.now()

    root.after(1, my_mainloop)

root.after(1, my_mainloop)

root.mainloop()
