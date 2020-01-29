
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

        def do(self):
            print(f"成功：{self.player.ID} 获得 {self.amount} 张牌")

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
        class ChooseChar:
            pass

        class Start:
            pass

        class End:
            pass

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

        class unknown:
            pass

