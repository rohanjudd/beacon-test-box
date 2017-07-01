#!/usr/bin/env python3
import os
import time
import string
import constants
from menu import Menu
from hat import Hat
from switch import Switch
from micro import Micro

micro = Micro()
hat = Hat()


def close():
    print("Shutting Down")
    hat.shutdown()
    micro.disconnect()
    quit()

menu_shutdown = Menu("Shutdown", close)
menu_main = Menu("Main Test Box Menu", menu_shutdown)
menu_rx = Menu("IR Receiver", menu_main)
menu_tx = Menu("IR Transmitter", menu_main)
current_menu = menu_main

def start_sleep():
    print("Going to Sleep")
    hat.sleep()

def start_up():
    hat.start_terminal()
    hat.write_line("Beacon Test Box v0.1")
    hat.write_line("Starting")
    delay()
    hat.write_line("Connecting to Interface Board")
    delay()
    micro.connect()
    if micro.is_connected():
        hat.write_line("Serial Port Open")
    else:
        hat.write_line("ERROR: Could not open serial port")
    delay()
    if micro.ping():
        hat.write_line("Connection Sucessful")
    else:
        hat.write_line("No response from Interface Board")
    delay()

def delay():
    time.sleep(constants.STARTUP_DELAY)

def terminal_test():
    hat.start_terminal()
    for x in range(10):
        hat.write("abcdefghijklmnopqrstuvwxyz")
        time.sleep(0.2)


def to_do():
    print("To Do")
    hat.display_notification("To Do")


def tx_test():
    micro.ir_transmit(1 ,1 ,True)
    time.sleep(1)


def micro_test():
    micro.flush()
    print("Connected: {}".format(micro.is_connected()))
    time.sleep(0.5)
    micro.send('b')
    micro.send('t')
    time.sleep(0.2)
    print("Received: {}".format(micro.read()))
    time.sleep(0.5)


def rx_display_test():
    for x in range(0, 32):
        hat.display_rx(x, True, x)
        time.sleep(0.02)
    time.sleep(1)


def hat_test():
    hat.hat_test()


def show_menu():
    os.system("clear")
    hat.display_menu(current_menu)
    print(current_menu.title)
    x = 1
    for l in current_menu.get_lines():
        print("{}: {}".format(x, l))
        x += 1


def go_to_menu(menu):
    global current_menu
    current_menu = menu
    show_menu()


def populate_menus():
    menu_main.add_entry("rxDisplay Test", rx_display_test)
    menu_main.add_entry("IR Transmitter", menu_tx)
    menu_main.add_entry("IR Receiver", menu_rx)
    menu_main.add_entry("Micro Test", micro_test)
    menu_main.add_entry("Terminal Test", terminal_test)
    menu_main.add_entry("Hat Test", hat_test)

    menu_tx.add_entry("Test C10 Tx", tx_test)
    menu_tx.add_entry("Test C16 Tx", to_do)
    menu_rx.add_entry("Test C10 Rx", to_do)
    menu_rx.add_entry("Test C16 Rx", to_do)
    menu_rx.add_entry("Measure Power", to_do)

    menu_shutdown.add_entry("Back to Main", menu_main)
    menu_shutdown.add_entry("Shutdown", close)


def process_button_input():
    sleep_timer = 0
    shutdown_timer = 0
    state = hat.get_button_state()
    while state == constants.NONE and sleep_timer < 500:
        state = hat.get_button_state()
        sleep_timer += 1
        time.sleep(0.05)
    if sleep_timer >= 500:
        start_sleep()
        while state == constants.NONE and shutdown_timer < 500:
            state = hat.get_button_state()
            shutdown_timer += 1
            time.sleep(0.05)
    if shutdown_timer >= 500:
        close()
    if state == constants.UP:
        current_menu.up()
    elif state == constants.DOWN:
        current_menu.down()
    elif state == constants.BACK:
        obj = current_menu.get_parent()
        if type(obj) is Menu:
            go_to_menu(obj)
        else:
            obj()
    elif state == constants.SELECT:
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
    for case in Switch(c):
        if case(*string.ascii_lowercase):
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
                obj = current_menu.get_parent()
                if type(obj) is Menu:
                    go_to_menu(obj)
                else:
                    obj()
            break
        if case(*string.digits):
            i = int(c) - 1
            if current_menu.check_pos(i):
                obj = current_menu.choose(i)
                if type(obj) is Menu:
                    go_to_menu(obj)
                else:
                    obj()
            break
        if case():  # default
            print("Incorrect Key")


def main():
    hat.set_led_states(status=True)
    populate_menus()
    hat.splash()
    start_up()
    go_to_menu(menu_main)
    while True:
        process_button_input()
        show_menu()


if __name__ == '__main__':
    main()
