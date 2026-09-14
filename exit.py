# Password Manager exit
# Author: Yingyi Liao
# For private use only

import threading

finish = False


def exit_delay_2_second():
    global finish
    finish = True
    timer = threading.Timer(2, print)
    print('Thank you for using Password Manager')
    timer.start()
