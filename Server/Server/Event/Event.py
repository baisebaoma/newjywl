
class Event:
    class __Event:
        def cancel(self):
            def cancel():
                print("这个事件已被取消")

            self.do = cancel

    class GetChampion(__Event):
        def __init__(self, player, champion):
            # 输入：玩家 要拿取的卡牌数量
            self.player = player
            self.champion = champion

        def do(self):
            self.player.champion = self.champion
            print(f"成功：{self.player.ID} 获得英雄 {self.champion.name}")

        def send(self, target="broadcast"):
            if target == "broadcast":
                return {
                    "event": "GetChampion",
                    "source": self.player.ID,
                    "card": None,
                    "amount": None,
                    "target": self.champion.name
                }
            # 最好在发送的时候也包装一下？
            elif target == "private":
                return {
                    "event": "GetChampion",
                    "source": self.player.ID,
                    "card": None,
                    "amount": None,
                    "target": self.champion.name
                }

    class GetCard(__Event):
        card_got = None

        def __init__(self, player, amount):
            # 输入：玩家 要拿取的卡牌数量
            self.player = player
            self.amount = amount
            self.game_logic = None

        def do(self):
            print(f"成功：{self.player.ID} 获得 {self.amount} 张牌")
            for _ in range(0, self.amount):
                self.player.hidden_cards.append(self.game_logic.cdl.pop())

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

    class PutHiddenCard(__Event):

        def __init__(self, player, card):
            # 输入：玩家 要拿取的卡牌数量
            self.player = player
            self.card = card

        def do(self):
            if self.player.gold >= self.card.value:
                print(f"成功：{self.player.ID} 花费 {self.card.value} 金币 将手牌 {self.card.name} 置入明牌区")
                self.player.gold -= self.card.value
                self.player.hidden_cards.remove(self.card)
                self.player.shown_cards.append(self.card)
            else:
                print(f"失败：{self.player.ID} 想花费 {self.card.value} 金币 将手牌 {self.card.name} 置入明牌区，可是钱不够")

        def send(self, target="broadcast"):
            return {
                "event": "GetCard",
                "source": self.player.ID,
                "card": None,
                "amount": None,
                "target": None
            }

    class TransferHiddenCard(__Event):
        def __init__(self, player1, player2, card):
            # 输入：玩家1 玩家2 卡牌
            self.player1 = player1
            self.player2 = player2
            self.card = card

        def do(self):
            self.player1.hidden_cards.remove(self.card)
            self.player2.hidden_cards.append(self.card)
            print(f"成功：{self.player1.ID} 的手牌 {self.card.name} 被转移至 {self.player2.ID}")

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

    class LostHiddenCard(__Event):
        def __init__(self, player, card):
            # is card tuple?
            # 输入：玩家 卡牌
            self.player = player
            self.card = card

        def do(self):
            self.player.hidden_cards.remove(self.card)
            print(f"成功：{self.player.ID} 的手牌 {self.card.name} 被拆除")

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

    class TransferShownCard(__Event):
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
            print(f"成功：{self.player1.ID} 的明牌区中 {self.card.name} 被转移至 {self.player2.ID}")

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

    class LostShownCard(__Event):
        def __init__(self, player, card):
            # 输入：玩家 卡牌
            self.player = player
            self.card = card

        def do(self):
            self.player.shown_cards.remove(self.card)
            print(f"成功：{self.player.ID} 的明牌区中 {self.card.name} 被拆除")

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

    class GetGold(__Event):
        # 注意：包括负数
        def __init__(self, player, amount):
            # 输入：玩家 数量
            self.player = player
            self.amount = amount

        def do(self):
            self.player.gold += self.amount
            print(f"成功：{self.player.ID} 获得 {self.amount} 金币 至 {self.player.gold}")

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

    class TransferGold(__Event):
        def __init__(self, player1, player2, amount):
            # 输入：玩家 数量
            self.player1 = player1
            self.player2 = player2
            self.amount = amount

        def do(self):
            self.player1.gold -= self.amount
            self.player2.gold += self.amount
            print(f"成功：{self.player1.ID} 的 {self.amount} 金币 被转移至 {self.player2.ID}")

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

    class Skill(__Event):
        class woyunla:
            pass

    class Round:
        class ChooseCham:
            def __init__(self, player, champion_pool_left):
                self.event_queue = None
                self.player = player
                self.champion_pool_left = champion_pool_left

            def do(self):
                print(f"成功：{self.player.ID} 正在选择英雄")
                print(f"剩余英雄：{self.champion_pool_left}")

                a = input("输入数字来选择一名英雄：")
                try:
                    a = int(a)
                    if a == 0:
                        return
                    a -= 1
                    self.player.champion = self.champion_pool_left[a]
                    self.event_queue.head(Event.GetChampion(player=self.player, champion=self.player.champion))
                    self.champion_pool_left.remove(self.champion_pool_left[a])
                except ValueError:
                    pass
                except IndexError:
                    print("输入的数字无法对应英雄！")
                print(f"成功：{self.player.ID} 的 英雄已选定为 {self.player.champion.name}")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "ChooseCham",
                    "source": self.player.ID,  # 注意：source 是被转移者，target 是获得者
                    "card": None,
                    "amount": None,
                    "target": self.player.champion.name
                }
            #

        class Start:
            def __init__(self):
                pass

            def do(self):
                print(f"成功：新一轮开始")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "RoundStart",
                    "source": None,
                    "card": None,
                    "amount": None,
                    "target": None
                }

        class End:
            def __init__(self):
                pass

            def do(self):
                print(f"成功：一轮结束")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "RoundEnd",
                    "source": None,
                    "card": None,
                    "amount": None,
                    "target": None
                }

    class Turn:
        class Start:
            def __init__(self, player):
                self.player = player

            def do(self):
                print(f"成功：{self.player.ID} 的回合开始")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "TurnStart",
                    "source": self.player.ID,
                    "card": None,
                    "amount": None,
                    "target": None
                }

        class ShowChamp:
            def __init__(self, player):
                self.player = player

            def do(self):
                print(f"成功：{self.player.ID} 的英雄是 {self.player.champion.name}")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "TurnShowChamp",
                    "source": self.player.ID,
                    "card": None,
                    "amount": None,
                    "target": self.player.champion.name
                }

        class Choose:
            def __init__(self, player):
                self.player = player
                self.event_queue = None

            def do(self):
                print(f"成功：{self.player.ID} 正在选择获取内容")
                a = input("输入 1 获得牌， 2 获得金币：")
                if a == "1":
                    self.event_queue.head(Event.GetCard(player=self.player, amount=2))
                elif a == "2":
                    self.event_queue.head(Event.GetGold(player=self.player, amount=2))

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "TurnShowChamp",
                    "source": self.player.ID,
                    "card": None,
                    "amount": None,
                    "target": self.player.champion.name
                }

        class Main:
            def __init__(self, player):
                self.player = player
                self.event_queue = None

            def do(self):
                print(f"成功：{self.player.ID} 的行动阶段开始")
                print(f"{self.player.ID} 的手牌：{self.player.hidden_cards}")
                print(f"{self.player.ID} 的明牌区：{self.player.shown_cards}")
                a = input("输入数字来将一张手牌放入明牌区，0放弃：")
                try:
                    a = int(a)
                    if a == 0:
                        return
                    a -= 1
                    self.card = self.player.hidden_cards[a]
                    self.event_queue.head(Event.PutHiddenCard(player=self.player, card=self.player.hidden_cards[a]))
                except ValueError:
                    pass
                except IndexError:
                    print("输入的数字无法对应牌！置入行动已被取消")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "TurnMain",
                    "source": self.player.ID,
                    "card": self.card.name,
                    "amount": None,
                    "target": None
                }


        class End:
            def __init__(self, player):
                self.player = player

            def do(self):
                print(f"成功：{self.player.ID} 的回合结束")

            def send(self, target="broadcast"):
                # 虽然 target 没有用 但是还是放在这里防止报错
                # 不用区分
                return {
                    "event": "TurnStart",
                    "source": self.player.ID,
                    "card": None,
                    "amount": None,
                    "target": None
                }


