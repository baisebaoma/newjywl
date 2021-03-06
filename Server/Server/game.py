import random
import threading
import time
import json

# self
from Event.Event import Event
from Event.EventListener import *
from Event.EventDealer import EventDealer

from Game.Champion import Champion
from Game.Card import Card


class Player:
    def __init__(self, ID):
        self.ID = ID
        self.gold = 0
        self.shown_cards = list()
        self.hidden_cards = list()
        self.buff = {}
        self.killed = False
        self.champion = None

    def turn(self):
        '''
        # 回合开始（亮英雄）
        ED.event_queue.push(Event.Turn.Start(source=self))
        # 获取阶段（有的英雄可以在这里使用技能）
        ED.event_queue.push(Event.Turn.Get(source=self))
        i = self.ask()
        if i == "GetCard":
            ED.event_queue.push(Event.GetCard(player=self, amount=2))  # 简化，直接摸两张牌，不需要选择
        elif i == "GetGold":
            ED.event_queue.push(Event.GetGold(player=self, amount=2))

        # 出牌阶段（使用技能）
        ED.event_queue.push(Event.Turn.Main(source=self))
        i = self.ask()

        # 回合结束（此时进行判定）
        ED.event_queue.push(Event.Turn.End(source=self))
        '''
        pass


class GameLogic:
    # cdl = card list, 牌堆
    end = False

    def __init__(self):
        self.cdl = list()
        self.players = list()
        self.champion_pool = [Champion.Assassin(), Champion.Thief(), Champion.Magician(), Champion.Emperor(),
                              Champion.Bishop(), Champion.Businessman(), Champion.Architect(), Champion.Warlord()]

        self.ED = None

    def __round(self):
        self.ED.event_queue.push(Event.Round.Start)
        self.ED.event_queue.push(Event.Round.ChooseCham)
        self.ED.event_queue.push(Event.Round.End)

    def __turn(self, player=None):
        self.ED.event_queue.push(Event.Turn.Start(player=player))
        self.ED.event_queue.push(Event.Turn.ShowChamp(player=player))
        self.ED.event_queue.push(Event.Turn.Choose(player=player))
        self.ED.event_queue.push(Event.Turn.Main(player=player))
        self.ED.event_queue.push(Event.Turn.End(player=player))

    def start(self):
        print("游戏逻辑开始了！")
        self.cdl = [Card.GoldMaker()] * 100
        # init
        random.shuffle(self.champion_pool)

        for player in self.players:
            self.ED.event_queue.push(Event.GetChampion(player=player, champion=self.champion_pool.pop(0)))
            self.ED.event_queue.push(Event.GetCard(player=player, amount=4))
            self.ED.event_queue.push(Event.GetGold(player=player, amount=5))

        time.sleep(6)

        while True:
            # shuffle players by champion
            players_in_order = [None] * 8
            for player in self.players:
                players_in_order[player.champion.order] = player
            for _ in range(players_in_order.count(None)):
                players_in_order.remove(None)

            for player in players_in_order:
                self.__turn(player)

            # end
            for player in self.players:
                if len(player.shown_cards) >= 3:
                    self.end = True
                    break
            if self.end:
                break

            self.champion_pool = [Champion.Assassin(), Champion.Thief(), Champion.Magician(), Champion.Emperor(),
                                  Champion.Bishop(), Champion.Businessman(), Champion.Architect(), Champion.Warlord()]
            self.ED.event_queue.push(Event.Round.Start())
            for player in self.players:
                self.ED.event_queue.push(Event.Round.ChooseCham(player=player, champion_pool_left=self.champion_pool))


class Game:
    def __init__(self):
        self.GL = GameLogic()
        # self.NW = Network()
        self.ED = EventDealer(game_logic=self.GL, network="NW")
        self.GL.ED = self.ED

    def start(self):
        self.ED.start()
        self.GL.start()


if __name__ == "__main__":
    g = Game()

    xjb = Player("xjb")
    xjb.shown_cards.append(Card.GoldMaker())
    pzk = Player("pzk")
    zxx = Player("zxx")

    g.GL.players.append(xjb)
    g.GL.players.append(pzk)
    g.GL.players.append(zxx)

    g.start()
