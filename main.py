#!/usr/bin/env python
import os
import time
import string
from menu import Menu
from oled import Oled
from hat import Hat
from switch import switch
from beacon import Beacon
from serialmicro import SerialMicro

micro = SerialMicro()
hat = Hat()

def close():
    print("Shutting Down")
    hat.shutdown()
    micro.disconnect()
    quit()

def goToSleep():
    print("Going to Sleep")
    hat.sleep()

menu_shutdown = Menu("Shutdown", close)
menu_main = Menu("Main Test Box Menu", menu_shutdown)
menu_rx = Menu("IR Receiver", menu_main)
menu_tx = Menu("IR Transmitter", menu_main)
current_menu = menu_main

def terminal_test():
    hat.newTerminal()
    for x in range(10):
        hat.write("abcdefghijklmnopqrstuvwxyz")
        time.sleep(0.2)
    
def toDo():
    print("To Do")
    hat.displayNotification("To Do")

def micro_test():
    micro.flush()
    print("Connected: {}".format(micro.isConnected()))
    print("Sending t")
    micro.send('t')
    print("Recieved: {}".format(micro.read()))
    micro.send('v')
    print("Recieved: {}".format(micro.read()))
    time.sleep(0.5)
    micro.send('b')

def rxdisplay_test():
    codes_done = 0
    for x in range(0,32):
        hat.oled.displayRx(x, True, x)
        time.sleep(0.5)
    time.sleep(1)

def hat_test():
    hat.testHat()
    
def goToMAIN():
    changeMenu(menu_main)
    
def showMenu():
    os.system("clear")
    hat.displayMenu(current_menu)
    print(current_menu.getTitle())
    x = 1
    for l in current_menu.getLines():
        print("{}: {}".format(x,l))
        x+=1
        
def gotoMenu(menu):
    global current_menu
    current_menu = menu
    showMenu()
    
def select():
    print("SELECT")
    
def incorrectInput():
    print("Incorrect Key")

def populateMenus():
    menu_main.addEntry("rxDisplay Test", rxdisplay_test)
    menu_main.addEntry("IR Transmitter", menu_tx)
    menu_main.addEntry("IR Reciever", menu_rx)
    menu_main.addEntry("Micro Test", micro_test)
    menu_main.addEntry("Terminal Test", terminal_test)
    menu_main.addEntry("Hat Test", hat_test)

    menu_tx.addEntry("Test C10 Tx", toDo)
    menu_tx.addEntry("Test C16 Tx", toDo)
    menu_rx.addEntry("Test C10 Rx", toDo)
    menu_rx.addEntry("Test C16 Rx", toDo)
    menu_rx.addEntry("Measure Power", toDo)
    menu_rx.addEntry("Measure Power", toDo)
    menu_rx.addEntry("Measure Power", toDo)
    menu_rx.addEntry("Measure Power", toDo)
    menu_shutdown.addEntry("Back to Main", menu_main)
    menu_shutdown.addEntry("Shutdown", close)

def processButtonInput():
    sleepTimer = 0
    shutdownTimer = 0
    state = hat.getButtonState()
    while  state == hat.NONE and sleepTimer < 500:
        state = hat.getButtonState()
        sleepTimer += 1
        time.sleep(0.05)
    if sleepTimer >= 500:
        goToSleep()
        while state == hat.NONE and shutdownTimer < 500:
            state = hat.getButtonState()
            shutdownTimer += 1
            time.sleep(0.05)
    if shutdownTimer >= 500:
        close()
    if state == hat.UP:
        current_menu.up()
    elif state == hat.DOWN:
        current_menu.down()
    elif state == hat.BACK:
        obj = current_menu.getParent()
        if (type(obj) is Menu):
            gotoMenu(obj)
        else:
            obj()
    elif state == hat.SELECT:
        obj = current_menu.select()
        if (type(obj) is Menu):
            gotoMenu(obj)
        else:
            obj()
    
def processInput():
    inp = input()
    if len(inp) > 0:
        c = inp[0]
    else:
        c = ' '
    for case in switch(c):
        if case(*string.ascii_lowercase): # note the * for unpacking as arguments
            if c == 'x':
                close()
                break
            if c == 'w':
                current_menu.up()
                break
            if c == 's':
                current_menu.down()
                break
            if c == 'd':
                obj = current_menu.select()
                if (type(obj) is Menu):
                    gotoMenu(obj)
                else:
                    obj()
            if c == 'a':
                obj = current_menu.getParent()
                if (type(obj) is Menu):
                    gotoMenu(obj)
                else:
                    obj()
            break
        if case(*string.digits):
            i = int(c) - 1
            if current_menu.checkPos(i):
                obj = current_menu.choose(i)
            if (type(obj) is Menu):
                gotoMenu(obj)
            else:
                obj()
            break
        if case(): # default
            print("Incorrect Key") 
            
def main():
    hat.setStatusLED(True)
    micro.connect()
    populateMenus()
    hat.splash()
    time.sleep(4)

    rxdisplay_test()
    
    gotoMenu(menu_main)
    while(True):
        #processInput()
        processButtonInput()
        showMenu()

if __name__ == '__main__':
	main()



	
