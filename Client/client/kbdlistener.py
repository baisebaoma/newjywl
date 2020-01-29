import client.UI
import client.game
import threading
import msvcrt
import time


def listen_thread():
    while True:
        e = ord(msvcrt.getch())
        if e == 224:
            e2 = ord(msvcrt.getch())
            if e2 == 72:
                client.UI.UIController.search().键盘监听 = 'up'
            elif e2 == 80:
                client.UI.UIController.search().键盘监听 = 'down'
            elif e2 == 75:
                client.UI.UIController.search().键盘监听 = 'left'
            elif e2 == 77:
                client.UI.UIController.search().键盘监听 = 'right'
            client.UI.UIController.search().refresh()
        elif e == 13:
            client.UI.UIController.search().键盘监听 = 'enter'
            client.UI.UIController.search().refresh()
        else:
            pass
        time.sleep(0.1)


def 键盘监听():
    线程 = threading.Thread(target=listen_thread)
    线程.setDaemon(True)
    线程.start()
