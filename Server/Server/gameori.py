import random
import threading
import time
import json


class Queue:
    """
    提供一堆函数:
    is_empty: 若是空 返回 alse 否则返回 True
    print: 打印当前队列
    push: 向末尾添加项
    push_insert: 在a项之后、b项之前添加项
    pop: 从最前提取一个项，如果空则返回 False
    """
    def __init__(self):
        self.__queue = list()

    def is_empty(self):
        if self.__queue:
            return False
        else:
            return True

    def print(self):
        print(self.__queue)

    def push(self, T):
        self.__queue.append(T)

    def pop(self):
        if self.is_empty():
            return False
        else:
            return self.__queue.pop(0)


class Player:
    def __init__(self, player_network):
        self.ID = player_network.ID
        self.gold = 0
        self.shown_cards = list()
        self.hidden_cards = list()
        self.buff = {}

    def turn(self):
        # 回合开始（亮英雄）
        ED.event_queue.push(Event.Turn.Start(source=self))
        # 获取阶段（有的英雄可以在这里使用技能）
        ED.event_queue.push(Event.Turn.Get(source=self))
        # 出牌阶段（使用技能）
        ED.event_queue.push(Event.Turn.Main(source=self))
        # 回合结束（此时进行判定）
        ED.event_queue.push(Event.Turn.End(source=self))


class Event:

    class GetCard:
        card_got = None

        def __init__(self, player, amount):
            # 输入：玩家 要拿取的卡牌数量
            self.player = player
            self.amount = amount

        def do(self):
            self.card_got = self.player.get_card(self.amount)  # ???????? 这个绝对实现不了 以后再改
            # tuple

        def send(self, target="broadcast"):
            if target == "broadcast":
                return {
                    "event": "GetCard",
                    "source": self.player.ID,
                    "card": None,
                    "amount": self.amount,
                    "target": None
                }
            # 最好在发送的时候也包装一下？
            elif target == "private":
                return {
                    "event": "GetCard",
                    "source": self.player.ID,
                    "card": self.card_got,
                    "amount": self.amount,
                    "target": None
                }

    class TransferHiddenCard:
        def __init__(self, player1, player2, card):
            # 输入：玩家1 玩家2 卡牌
            self.player1 = player1
            self.player2 = player2
            self.card = card

        def do(self):
            self.player1.hidden_cards.remove(self.card)
            self.player2.hidden_cards.append(self.card)

        def send(self, target="broadcast"):
            if target == "broadcast":
                return {
                    "event": "TransferHiddenCard",
                    "source": self.player1.ID,
                    "card": None,
                    "amount": 1,
                    "target": self.player2.ID
                }
            elif target == "private":
                return {
                    "event": "TransferHiddenCard",
                    "source": self.player1.ID,
                    "card": self.card.name,
                    "amount": 1,
                    "target": self.player2.ID
                }

    class LostHiddenCard:
        def __init__(self, player, card):
            # is card tuple?
            # 输入：玩家 卡牌
            self.player = player
            self.card = card

        def do(self):
            self.player.lost_card(self.card)

        def send(self, target="broadcast"):
            # 虽然 target 没有用 但是还是放在这里防止报错
            # 不用区分
            return {
                "event": "LostHiddenCard",
                "source": self.player.ID,
                "card": self.card.name,
                "amount": None,
                "target": None
            }

    class TransferShownCard:
        def __init__(self, player1, player2, card):
            # is card tuple?
            # no because 1 card 1 time
            # 输入：玩家1 玩家2 卡牌
            self.player1 = player1
            self.player2 = player2
            self.card = card

        def do(self):
            self.player1.shown_cards.remove(self.card)
            self.player2.shown_cards.append(self.card)

        def send(self, target="broadcast"):
            # 虽然 target 没有用 但是还是放在这里防止报错
            # 不用区分
            return {
                "event": "TransferShownCard",
                "source": self.player1.ID,
                "card": self.card.name,
                "amount": None,
                "target": self.player2.ID
            }

    class LostShownCard:
        def __init__(self, player, card):
            # 输入：玩家 卡牌
            self.player = player
            self.card = card

        def do(self):
            self.player.shown_cards.remove(self.card)

        def send(self, target="broadcast"):
            # 虽然 target 没有用 但是还是放在这里防止报错
            # 不用区分
            return {
                "event": "LostShownCard",
                "source": self.player.ID,
                "card": self.card.name,
                "amount": None,
                "target": None
            }

    class GetGold:
        # 注意：包括负数
        def __init__(self, player, amount):
            # 输入：玩家 数量
            self.player = player
            self.amount = amount

        def do(self):
            self.player.gold += self.amount

        def send(self, target="broadcast"):
            # 虽然 target 没有用 但是还是放在这里防止报错
            # 不用区分
            return {
                "event": "GetGold",
                "source": self.player.ID,
                "card": None,
                "amount": self.player.gold,  # 注意：直接同步数字，防止意外（或者客户端开挂）
                "target": None
            }

    class TransferGold:
        def __init__(self, player1, player2, amount):
            # 输入：玩家 数量
            self.player1 = player1
            self.player2 = player2
            self.amount = amount

        def do(self):
            self.player1.gold -= self.amount
            self.player2.gold += self.amount

        def send(self, target="broadcast"):
            # 虽然 target 没有用 但是还是放在这里防止报错
            # 不用区分
            return {
                "event": "TransferGold",
                "source": self.player1.ID,  # 注意：source 是被转移者，target 是获得者
                "card": None,
                "amount": self.amount,
                "target": self.player2.ID
            }

    class Skill:
        class woyunla:
            pass

    class Round:
        class ChooseChar:
            pass

        class Start:
            pass

        class End:
            pass

    class Turn:
        class Start:
            pass

        class End:
            pass

        class unknown:
            pass


class EventDealer:

    def __init__(self, game, network=""):
        self.game = game  # 将？？传进来
        self.network = network
        self.event_queue = Queue()

    def deal(self):
        event = self.event_queue.pop()
        if event is not False:  # 因为 event 可能是 Event 也可能是 Bool，所以不能写 if not event
            event.do()
            # self.game.broadcast(event.send())  # 暂时是这样
            print(event.send())
        else:
            print("no event currently")

    def start(self):
        thread = threading.Thread(target=self.__thread, args=(), daemon=True)
        thread.start()

    def __thread(self):
        while not self.game.end:
            self.deal()
            time.sleep(1)


class GameLogic:
    end = False
    cdl = list()
    # cdl = card list, 牌堆

    def round(self):
        ED.event_queue.push(Event.Round.Start)
        ED.event_queue.push(Event.Round.ChooseChar)
        ED.event_queue.push(Event.Round.End)


    def start(self):
        print("GameLogic Started")
        # player_number = 8  # 玩家人数
        # 作弊牌堆如下
        self.cdl = [22, 22, 22, 22, 22, 22, 22]
        champion_pool = list(range(0, 1))  # 英雄池(从0开始)
        self.turn_controller()


class Game:
    def __init__(self):
        self.GL = GameLogic()
        # self.NW = Network()
        self.ED = EventDealer(game=self.GL, network="NW")

    def start(self):
        self.ED.start()
        self.GL.start()


if __name__ == "__main__":
    ED = EventDealer(game=GameLogic())
    thread = threading.Thread(target=ED.start, args=(), daemon=False)
    thread.start()
    for _ in range(5):
        ED.event_queue.push(Event.GetGold(player=Player("nihao"), amount=2))
        time.sleep(random.randint(1, 5))
    # time.sleep(1)

    # for _ in range(3):
    #     ED.deal()
