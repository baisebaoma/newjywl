import threading
import time

# self
from Event.Event import Event
from Event.Queue import Queue
from Game.Card import Card
from Game.Champion import Champion


class EventListener:
    pass


class GoldMakerListener(EventListener):
    interest = ((Event.GetGold, Event.GetCard),
                (Event.Turn.Start, Event.LostShownCard))

    __count = {

    }

    def activate_before(self, event):
        for card in event.player.shown_cards:
            if type(card) == Card.GoldMaker:
                if type(event) == Event.GetGold:
                    print(f'{event.player.ID} 拥有 金币制造厂，加钱翻倍！')
                    if event.player.ID in self.__count:
                        self.__count[event.player.ID] += event.amount
                    else:
                        self.__count[event.player.ID] = event.amount
                    event.amount *= 2
                elif type(event) == Event.GetCard:
                    print(f'{event.player.ID} 拥有 金币制造厂，不能获得牌！')
                    event.cancel()
        return event
        # event.cancel()

    def activate_after(self, event):
        if type(event) == Event.Turn.Start:
            if type(event.player.champion) == Champion.Businessman:
                # 调试用 if event.player.ID == "xjb":
                # print("Nice!")
                for card in event.player.shown_cards:
                    if type(card) == Card.GoldMaker:
                        event.player.gold += 1
                        print(f"{event.player.ID} 是 商人 并且拥有 金币制造厂，加 1 金")
                        if event.player.ID in self.__count:
                            self.__count[event.player.ID] += 1
                        else:
                            self.__count[event.player.ID] = 1
                        return event

        elif type(event) == Event.LostShownCard:
            if type(event.card) == Card.GoldMaker:
                event.player.gold -= self.__count[event.player.ID]
                print(f"{event.player.ID} 的 金币制造厂 被拆了！他将为此损失 {self.__count[event.player.ID]} 金！")
                return event


class KilledListener(EventListener):
    interest = (Event.Turn.Start, )

    def activate(self, event):
        if event.player.killed:
            print(f'{event.player.ID} 已经被杀，无法进行下一个回合！')
            event.cancel()
        return event
            # event.cancel()

