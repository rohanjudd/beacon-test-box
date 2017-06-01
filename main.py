#!/usr/bin/env python
import os
import time
import string
from menu import Menu
from hat import Hat
from switch import switch
from serialmicro import SerialMicro

micro = SerialMicro()
hat = Hat()


def close():
    print("Shutting Down")
    hat.shutdown()
    micro.disconnect()
    quit()


def start_sleep():
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


def to_do():
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


def rx_display_test():
    for x in range(0, 32):
        hat.oled.displayRx(x, True, x)
        time.sleep(0.5)
    time.sleep(1)


def hat_test():
    hat.testHat()


def show_menu():
    os.system("clear")
    hat.displayMenu(current_menu)
    print(current_menu.getTitle())
    x = 1
    for l in current_menu.getLines():
        print("{}: {}".format(x, l))
        x += 1


def go_to_menu(menu):
    global current_menu
    current_menu = menu
    show_menu()


def select():
    print("SELECT")


def populate_menus():
    menu_main.addEntry("rxDisplay Test", rx_display_test)
    menu_main.addEntry("IR Transmitter", menu_tx)
    menu_main.addEntry("IR Receiver", menu_rx)
    menu_main.addEntry("Micro Test", micro_test)
    menu_main.addEntry("Terminal Test", terminal_test)
    menu_main.addEntry("Hat Test", hat_test)

    menu_tx.addEntry("Test C10 Tx", to_do)
    menu_tx.addEntry("Test C16 Tx", to_do)
    menu_rx.addEntry("Test C10 Rx", to_do)
    menu_rx.addEntry("Test C16 Rx", to_do)
    menu_rx.addEntry("Measure Power", to_do)
    menu_rx.addEntry("Measure Power", to_do)
    menu_rx.addEntry("Measure Power", to_do)
    menu_rx.addEntry("Measure Power", to_do)
    menu_shutdown.addEntry("Back to Main", menu_main)
    menu_shutdown.addEntry("Shutdown", close)


def process_button_input():
    sleep_timer = 0
    shutdown_timer = 0
    state = hat.getButtonState()
    while state == hat.NONE and sleep_timer < 500:
        state = hat.getButtonState()
        sleep_timer += 1
        time.sleep(0.05)
    if sleep_timer >= 500:
        start_sleep()
        while state == hat.NONE and shutdown_timer < 500:
            state = hat.getButtonState()
            shutdown_timer += 1
            time.sleep(0.05)
    if shutdown_timer >= 500:
        close()
    if state == hat.UP:
        current_menu.up()
    elif state == hat.DOWN:
        current_menu.down()
    elif state == hat.BACK:
        obj = current_menu.getParent()
        if type(obj) is Menu:
            go_to_menu(obj)
        else:
            obj()
    elif state == hat.SELECT:
        obj = current_menu.select()
        if type(obj) is Menu:
            go_to_menu(obj)
        else:
            obj()


def process_input():
    inp = input()
    if len(inp) > 0:
        c = inp[0]
    else:
        c = ' '
    for case in switch(c):
        if case(*string.ascii_lowercase):  # note the * for unpacking as arguments
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
                if type(obj) is Menu:
                    go_to_menu(obj)
                else:
                    obj()
            if c == 'a':
                obj = current_menu.getParent()
                if type(obj) is Menu:
                    go_to_menu(obj)
                else:
                    obj()
            break
        if case(*string.digits):
            i = int(c) - 1
            if current_menu.checkPos(i):
                obj = current_menu.choose(i)
                if type(obj) is Menu:
                    go_to_menu(obj)
                else:
                    obj()
            break
        if case():  # default
            print("Incorrect Key")


def main():
    hat.setStatusLED(True)
    micro.connect()
    populate_menus()
    hat.splash()
    time.sleep(4)

    rx_display_test()

    go_to_menu(menu_main)
    while True:
        # processInput()
        process_button_input()
        show_menu()


if __name__ == '__main__':
    main()
