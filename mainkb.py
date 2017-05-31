#!/usr/bin/env python
import os
import time
import string
from menu import Menu
from oled import Oled
from switch import switch
from serialmicro import SerialMicro

micro = SerialMicro()
oled = Oled()

def close():
    oled.clear()
    oled.refresh()
    micro.disconnect()
    quit()

menu_shutdown = Menu("Shutdown", close)
menu_main = Menu("Main Test Box Menu", menu_shutdown)
menu_rx = Menu("IR Receiver", menu_main)
menu_tx = Menu("IR Transmitter", menu_main)
current_menu = menu_main

def eat():
    oled.startTerminal()
    time.sleep(.5)
    oled.writeln("eating012345678901234567890")
    time.sleep(.5)
    oled.writeln("chewing01234567890")
    time.sleep(.5)
    oled.write("dancing")
    time.sleep(.5)
    oled.write("dancing")
    time.sleep(.5)
    oled.write("dancing")
    time.sleep(4)
    print("eating")
    
def chew():
    print("chewing")

def serial_test():
    micro.flush()
    print("Connected: {}".format(micro.isConnected()))
    print("Sending t")
    micro.send('t')
    print("Recieved: {}".format(micro.read()))
    micro.send('v')
    print("Recieved: {}".format(micro.read()))
    time.sleep(0.5)

def blink_led():
    micro.send('b')
    
def goToMAIN():
    changeMenu(menu_main)
    
def showMenu():
    os.system("clear")
    oled.displayMenu(current_menu)
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
    menu_main.addEntry("IR Transmitter", menu_tx)
    menu_main.addEntry("IR Reciever", menu_rx)
    menu_main.addEntry("Serial Test", serial_test)
    menu_main.addEntry("Blink LED", blink_led)
    menu_tx.addEntry("Test C10 Tx", eat)
    menu_tx.addEntry("Test C16 Tx", eat)
    menu_rx.addEntry("Test C10 Rx", eat)
    menu_rx.addEntry("Test C16 Rx", eat)
    menu_rx.addEntry("Measure Power", eat)
    menu_rx.addEntry("Measure Power", eat)
    menu_rx.addEntry("Measure Power", eat)
    menu_rx.addEntry("Measure Power", eat)
    menu_shutdown.addEntry("Back to Main", menu_main)
    menu_shutdown.addEntry("Shutdown", close)

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
    micro.connect()
    populateMenus()
    oled.splash()
    time.sleep(1)
    gotoMenu(menu_main)
    while(True):
        processInput()
        showMenu()

if __name__ == '__main__':
	main()



	
