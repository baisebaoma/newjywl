import threading
import time

from Event.EventListener import *
from Event.Queue import Queue


class EventDealer:

    event_listeners = (
        GoldMakerListener(),
        KilledListener(),

    )

    def __init__(self, game, network=""):
        self.game = game  # 将？？传进来
        self.network = network
        self.event_queue = Queue()

    def ask_before(self, event):
        for event_listener in self.event_listeners:
            if event.__class__ in event_listener.interest:
                event = event_listener.activate_before(event)
            return event

    def ask_after(self, event):
        for event_listener in self.event_listeners:
            if event.__class__ in event_listener.interest:
                event = event_listener.activate_after(event)
            return event

    def deal(self):
        event = self.event_queue.pop()
        if event is not False:  # 因为 event 可能是 Event 也可能是 Bool，所以不能写 if not event
            # print(f'正在处理事件 {event.send()}')
            event = self.ask_before(event)
            event.do()
            event = self.ask_after(event)
            # self.game.broadcast(event.send())  # 暂时是这样
            # print(event.send())
        else:
            print("没有事件")
            time.sleep(1)
            # time.sleep(60)

    def start(self):
        # start listening
        thread = threading.Thread(target=self.__thread, args=(), daemon=False)
        thread.start()

    def __thread(self):
        while not self.game.end:
            self.deal()
            time.sleep(0.05)


        # append event listeners
        self.event_listeners.append(GoldMakerListener())
