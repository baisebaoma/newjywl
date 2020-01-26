import random
import threading
import time

class Queue:
    '''
    提供4个函数:
    print: 打印当前队列
    push: 向末尾添加项
    pop: 从最前提取一个项，如果空则返回 False
    '''

    __queue = list()

    def is_empty(self):
        if self.__queue:
            return True
        else:
            return False

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
    ID = None
    gold = 0
    shown_cards = list() 
    hidden_cards = list()

    def __init__(self, ID):
        self.ID = ID


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




class EventDealer:
    event_queue = Queue()

    def __init__(self, game):
        self.game = game

    def deal(self):
        event = self.event_queue.pop()
        if event is not False:
            event.do()
            print(event.send())  # 暂时是这样

    def start(self):
        while self.event_queue:
            self.deal()



class Game:
    
    cdl = list()
    # cdl = card list, 牌堆

    class Card:
        pass

    class Player:
        gold = 2
        card = list()
        shown_card = list()

    def get_card(self, player_to_get, card_to_get):
        # 用来获得牌。
        # 输入：玩家（玩家类），几张牌（数）
        # 输出：成功 True 失败 False
        if len(self.cdl) < card_to_get:
            printb('牌堆牌数不够')
            return False
        else:
            i = 1
            while i <= card_to_get:
                shoupai[player_to_get].insert(0, self.cdl[0])
                self.cdl.remove(self.cdl[0])
                i += 1

    def get_card_1_in_2(self, player_to_get):
        if not self.cdl:
            printb('洗牌后牌堆牌数仍不够，已自动转为获得2金')
            gold[player_to_get] += 2
            printb(f'金币 = {gold}')
            return
        print(translate_card(self.cdl))
        printp(f'''\n       1. {card[self.cdl[0]]}   和   2. {card[self.cdl[1]]}
                {card_cost[self.cdl[0]]}金                {card_cost[self.cdl[1]]}金
    增益对象：    {champ[card_color[self.cdl[0]]]}            {champ[card_color[self.cdl[1]]]}\n''', player_to_get)
        '''
        {card_cost[self.cdl[0]]}金 和 {card_cost[self.cdl[1]]}金
    增益对象：{champ[card_color[self.cdl[0]]]} 、{champ[card_color[self.cdl[1]]]}
        '''
        control = inputp(f'[INPUT]请从 1. {card[self.cdl[0]]} 和 2. {card[self.cdl[1]]} 中选择: ', player_to_get)
        if control == 1:
            print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
            shoupai[player_to_get].append(self.cdl[0])
            print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
            self.cdl.remove(self.cdl[0])
        elif control == 2:
            print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
            shoupai[player_to_get].append(self.cdl[1])
            print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
            self.cdl.remove(self.cdl[1])
        self.cdl.append(self.cdl[0])
        self.cdl.remove(self.cdl[0])

    def playcard(self, player):
        printp(f"""
    拥有手牌：{translate_card(shoupai[player])}
    手牌增益：{translate_champ(translate_color(shoupai[player]))}
    装备花费：{translate_cost(shoupai[player])}
    可用金币：{gold[player]}""", player)
        good = False
        while not good:
            pai = int(inputp("[INPUT] 请装备，-1为放弃，1为第一张，2为第二张，以此类推：", player))
            if pai != -1 and 1 <= pai <= len(shoupai[player]):
                # b 是确保没有两张一样的牌的bool
                b = True
                for item in owned_cards[player]:
                    if card.get(item) == card.get(shoupai[player][pai - 1]) and card.get(
                            shoupai[player][pai - 1]) != '金铲铲':
                        printp(f"不能持有两件相同装备：{card[item]}", player)
                        b = False

                if gold[player] >= card_cost.get(shoupai[player][pai - 1]) and b is True:
                    gold[player] -= card_cost.get(shoupai[player][pai - 1])
                    printb(f"{player_ID[player]} 装备了 {card[shoupai[player][pai - 1]]}")
                    if shoupai[player][pai - 1] == 22 or shoupai[player][pai - 1] == 23:
                        item_skills('"你也有份"', player)
                    owned_cards[player].append(shoupai[player][pai - 1])
                    shoupai[player].remove(shoupai[player][pai - 1])
                    printp(f"""手牌：{translate_card(shoupai[player])}
    装备栏：{translate_card(owned_cards[player])}
    已得分：{score_count(player)}
    剩余金币：{gold[player]}""", player)
                    score[player] = score_count(player)
                    break
                elif b:
                    printp(f"[ERROR] 金币不足", player)
                    pass
            else:
                printp(f"已放弃", player)
                break

    def turn(self, champion_for_turn):  # player 是自己！！！
        '''
        check if killed
        show champion
        if constructions get extra gold
        choose whether get card or gold
        if constructor then up to 3 card
        if use card
        end
        '''
        # is_doubled = False
        player = from_champion_find_player(champion_for_turn)
        if player == -1:
            printb(f"""\n没有人选择 {champ[champion_for_turn]} """)
            return
        printb(f'''\n\n\n\n****现在轮到选择 {champ[champion_for_turn]} 的玩家行动''')
        if not if_killed[player]:
            printb(f"""选择 {champ[champion_for_turn]} 的玩家是 {player_ID[player]} (玩家{player}) ！
    {champ_explanation[champion_for_turn]}
    """)
            if if_stolen[player]:
                gold[from_champion_find_player(1)] += gold[player]
                gold[player] = 0
                if is_owned(49, from_champion_find_player(1)):
                    item_skills("三相之力", from_champion_find_player(1), kill=player)
                    # 注意 kill 是正在回合的人
                printb(f'\n{player_ID[player]} (玩家{player}) 的钱已被偷光。\n当前金币：{gold[player]}\n'
                       f'探险家当前金币：{gold[from_champion_find_player(1)]}')
            printp('''
    *************************************************
    *************************************************
          轮          到          你         了
    *************************************************
    *************************************************
    ''', player)

            if champion_for_turn == 3:
                king = player
                printb("德玛西亚皇子已获得下次先手权")
            elif champion_for_turn == 5:
                gold[player] += 2
                printb(f"血港鬼影已额外获得2金，可用金币：{gold[player]}")
            # 上海大炮
            if is_owned(37, player):
                item_skills("上海大炮", player)
            printb('正在等待玩家操作')
            if item_count(champion_for_turn) != 0:
                gold[player] += item_count(champion_for_turn)
                printb(
                    f"{champ[champion_for_turn]} 拥有 {item_count(champion_for_turn)} 个对应装备，已加 {item_count(champion_for_turn)} 金，当前 {gold[player]} 金")
            skillused = False
            actionbool = False
            while not skillused:
                printp(
                    f'你的英雄：{champ[champion_for_turn]}'
                    f'\n你的手牌：{translate_card(shoupai[player])}'
                    f'\n手牌价格：{translate_cost(shoupai[player])}'
                    f'\n你的金币：{gold[player]}'
                    f'\n你的装备：{translate_card(owned_cards[player])}'
                    f'\n已得分：{score_count(player)}', player)
                action = int(
                    inputp(f'\n[INPUT] 请 {player_ID[player]} (玩家{player}) 选择：1.获得2金 2.从2张牌中选择1张作为手牌 3.使用技能： ', player))
                if action == 1:
                    gold[player] += 2
                    printb(f'''{player_ID[player]} (玩家{player}) 已获得2金
    ''')
                    actionbool = True
                    break
                elif action == 2:
                    if champion_for_turn == 6:
                        printb(f'{player_ID[player]} (玩家{player}) 选择 山隐之焰，可以直接获得2张牌')
                        getcard(player, 2)
                    else:
                        printb(f'{player_ID[player]} (玩家{player}) 选择了拿1张牌')
                        getcard1in2(player)
                        printb(
                            f'{player_ID[player]} (玩家 {player}) 已获得一张牌，当前手牌数：{shoupai_count()[player]}')
                        print(f'''牌堆 = {translate_card(self.cdl)}
    手牌 = {translate_shoupai(player)}
    ''')
                    actionbool = True
                    break
                elif action == 3:
                    if if_used_skill[player]:
                        printp("[ERROR] 技能已使用", player)
                    else:
                        champion_skills(champion_for_turn)
                        if actionbool:
                            break
                    # if if_used_skill[player]:
                    # break
            if champion_for_turn == 6:
                x = 1
                printb(f'\n山隐之焰 开始装备3次')
                while x < 4:
                    printb(f'\n这是 山隐之焰 第{x}次 装备！')
                    playcard(player)
                    x += 1
                printb(f'\n奥恩已装备完成')
            else:
                playcard(player)

            countjinchanchan = 0
            for item in owned_cards[player]:
                if 38 <= item <= 40:
                    countjinchanchan += 1
            if countjinchanchan >= 2:
                end_the_game = True
                jinchanchan = player  # 这个变量是用来告诉end 有没有人有金铲铲
                end()
            # end the game
            if not if_used_skill[player] and not (3 <= champion_for_turn <= 6):
                printp(f'\n***你还未使用技能，再次询问：***', player)
                champion_skills(champion_for_turn)
            if max_card() >= end_game_items:
                printb(f"**********已有玩家获得{end_game_items}件装备 游戏即将结束**********")
                end_the_game = True
            # 自然之力
            if is_owned(42, player) and is_doubled is False:
                is_doubled = True
                item_skills("自然之力", player)
            printb(f'                       {player_ID[player]} 的回合结束')
            is_doubled = False
        else:
            printb(f"""\n{champ.get(champion_for_turn)} 已被击杀""")

    def turn_controller():

        round_counter = 1
        while True:
            printb(f"\n\n这是第{round_counter}个回合！")

            # 这是用来修复少于8人时 正在等待玩家操作 那一行的 out of range
            repair = 0
            while repair <= len(champion_selected) - 1:
                if repair >= player_number:
                    champion_selected[repair] = -1
                repair += 1

            for c in champion_selected:
                try:
                    printp(f"\n\n***你的英雄是 {champ.get(c, '无')} ！***", from_champion_find_player(c))
                    printp(f'你的手牌是 {translate_shoupai(from_champion_find_player(c))} ！', from_champion_find_player(c))
                    printp(f'你的装备是 {translate_card(owned_cards[from_champion_find_player(c)])} ！\n\n',
                           from_champion_find_player(c))
                except IndexError:
                    pass

            print(f"【champion_selected】={champion_selected}")
            i = 0
            while i < len(champ):
                turn(i)
                i += 1
            end()
            if end_the_game:
                break
            pick_champion(king)
            if_killed = [False for i in range(player_number)]
            if_stolen = [False for i in range(player_number)]
            if_used_skill = [False for i in range(player_number)]
            round_counter += 1

    """
    def end():

        # 作弊代码
        '''
        end_the_game = True
        player_number = 8
        score = [3, 2, 4, 6, 3, 4, 5, 100]
        jinchanchan = 2
        player_ID = ['nimasile', 'nimasile', 'nimasile', 'nimasile', 'nimasile', 'nimasile', 'nimasile', 'nimasile']
        '''

        if end_the_game:
            printb("\n\n\n\n\n*****游戏已结束*****")
            player_list = list(range(0, player_number))
            for i in range(player_number - 1):
                for j in range(1, player_number - i):
                    if int(score[j - 1]) > int(score[j]):
                        score[j - 1], score[j] = score[j], score[j - 1]
                        player_list[j - 1], player_list[j] = player_list[j], player_list[j - 1]
            # 好像可以用zip 我不会
            if jinchanchan != -1:
                printb(f'拥有2个金铲铲的 {player_ID[jinchanchan]} (玩家{jinchanchan}) 排名第一')
            x = 0
            while x < player_number:
                printb(f"{score[x]} {player_ID[x]}")
                x += 1
            printb(f"排行榜：{score}")
            time.sleep(30)
        return
    """

    def end():

        # 作弊代码
        '''
        end_the_game = True
        player_number = 8
        score = [3, 2, 4, 6, 3, 4, 5, 100]
        jinchanchan = 2
        player_ID = ['a0', 'b1', 'c2', 'd3', 'e4', 'f5', 'g6', 'h7']
        if end_the_game:
            print("\n\n\n\n\n*****游戏已结束*****\n")
            player_list = list(range(0, player_number))
            score_for_end = list(score)  # 一定要有这个list 不然这两个会同时变化

            for i in range(player_number - 1):
                for j in range(1, player_number - i):
                    if int(score_for_end[j - 1]) < int(score_for_end[j]):
                        score_for_end[j - 1], score_for_end[j] = score_for_end[j], score_for_end[j - 1]
                        player_list[j - 1], player_list[j] = player_list[j], player_list[j - 1]
            x = 1
            if jinchanchan != -1:
                print(f"第1名：{player_ID[jinchanchan]} (玩家 {jinchanchan}) 得分：{score[jinchanchan]} **拥有2把金铲铲**\n")
                x += 1
            for y in player_list:
                if jinchanchan != y:
                    print(f"第{x}名：{player_ID[y]} (玩家 {y}) 得分：{score[y]}\n")
                    x += 1
            time.sleep(120)
            exit()
        '''
        if end_the_game:
            printb("\n\n\n\n\n*****游戏已结束*****\n")
            player_list = list(range(0, player_number))
            s = 0
            while s <= player_number - 1:
                score_count(s)
                print(score[s])
                s += 1
            score_for_end = list(score)  # 一定要有这个list 不然这两个会同时变化
            for i in range(player_number - 1):
                for j in range(1, player_number - i):
                    if int(score_for_end[j - 1]) < int(score_for_end[j]):
                        score_for_end[j - 1], score_for_end[j] = score_for_end[j], score_for_end[j - 1]
                        player_list[j - 1], player_list[j] = player_list[j], player_list[j - 1]
            x = 1
            if jinchanchan != -1:
                printb(f"第1名：{player_ID[jinchanchan]} (玩家 {jinchanchan}) 得分：{score[jinchanchan]} **拥有2把金铲铲**\n")
                x += 1
            for y in player_list:
                if jinchanchan != y:
                    printb(f"第{x}名：{player_ID[y]} (玩家 {y}) 得分：{score[y]}\n")
                    x += 1
            time.sleep(120)
            exit()
            # 好像可以用zip 我不会
        # time.sleep(120)

    def max_card():
        a = len(owned_cards[0])
        for item in owned_cards:
            if len(item) >= a:
                a = len(item)
        return a

    def item_count(self, champion):
        player = from_champion_find_player(champion)
        i = 0
        for item in owned_cards[player]:
            if card_color[item] == champion:
                i += 1
        return i

    def champion_skills(self, champion):

        player = from_champion_find_player(champion)
        if champion == 0:  # 刺客
            printp('''    
        0: 影流之镰
        1: 探险家
        2: 卡牌大师
        3: 德玛西亚皇子
        4: 海兽祭司
        5: 血港鬼影
        6: 山隐之焰
        7: 解脱者''', player)
            kill = inputp(f"[INPUT] 选择要击杀的英雄，-1为放弃：", player)
            kill = translate_input(kill)
            if kill != -1 and 0 <= kill <= len(champ) - 1:
                if kill != 0:
                    if from_champion_find_player(kill) != -1:
                        if_killed[from_champion_find_player(kill)] = True
                    printb(f"{player_ID[player]} (影流之镰) 已击杀 {champ[kill]}")
                    if_used_skill[player] = True  # player草草草 草草草草草草
                else:
                    printp(f"[ERROR] 不能自杀", player)
            else:
                printp(f"已放弃", player)

        elif champion == 1:  # 窃贼
            printp('''
            0: 影流之镰
            1: 探险家
            2: 卡牌大师
            3: 德玛西亚皇子
            4: 海兽祭司
            5: 血港鬼影
            6: 山隐之焰
            7: 解脱者''', player)
            kill = int(inputp("[INPUT] 选择要偷钱的英雄，-1为放弃：", player))
            kill = translate_input(kill)
            if kill != -1:
                try:
                    if kill != 1 and kill != 0 and not (
                    if_killed[from_champion_find_player(kill)]) and 0 <= kill <= len(champ) - 1:
                        # 记得修 偷到没有人选的会清零自己的装备
                        # gold[player] += gold[from_champion_find_player(kill)]
                        # gold[from_champion_find_player(kill)] = 0
                        if from_champion_find_player(kill) != -1:
                            if_stolen[from_champion_find_player(kill)] = True
                        print(from_champion_find_player(kill))
                        print(if_stolen)
                        printb(f"{player_ID[player]} (探险家) 已偷光 {champ[kill]} 的钱，将在 {champ[kill]} 的回合生效\n")
                        if_used_skill[player] = True
                    else:
                        printp(f"[ERROR] 不能偷这个人", player)
                except IndexError:
                    printp(f"[ERROR] IndexError", player)

            else:
                printp(f"已放弃", player)

        elif champion == 2:  # 魔术师
            printp('''
            0: 影流之镰
            1: 探险家
            2: 卡牌大师
            3: 德玛西亚皇子
            4: 海兽祭司
            5: 血港鬼影
            6: 山隐之焰
            7: 解脱者''', player)
            kill = int(inputp("[INPUT] 选择要换牌的英雄，-1为放弃：", player))
            kill = translate_input(kill)
            if kill != -1 and 0 <= kill <= len(champ) - 1:
                if kill != 2 and from_champion_find_player(kill) != -1:
                    temp = shoupai[from_champion_find_player(kill)]
                    shoupai[from_champion_find_player(kill)] = shoupai[player]
                    shoupai[player] = temp
                    printb(f"{player_ID[player]} (卡牌大师) 已与 {champ[kill]} 换牌")
                    if_used_skill[player] = True  # player草草草 草草草草草草
                    print(f"所有人的手牌：{shoupai_count()}")
                else:
                    printp(f"[ERROR] 不能与他换：没有选择或是自己", player)
            else:
                printp(f"已放弃", player)

        elif 3 <= champion <= 6:  # 国王 等
            printp(f"""{champ[champion]} 的两个技能都为被动技能，无需主动发动""", player)
            if_used_skill[player] = True  # player草草草 草草草草草草
        elif champion == 7:
            name = 0
            while name < len(player_ID):
                printp(f"       {name}: {player_ID[name]}, {len(owned_cards[name])} 件装备", player)
                name += 1
            kill = int(inputp("[INPUT] 输入数字来选择要拆的*玩家*，-1为放弃：", player))
            kill = translate_input(kill)
            if kill != -1:
                if kill != 7 and 0 <= kill <= player_number - 1:
                    printp(f"{player_ID[kill]} 的装备有：{translate_card(owned_cards[from_champion_find_player(kill)])}",
                           player)
                    printp(f"价值：{translate_cost(owned_cards[from_champion_find_player(kill)])}\n 你需要花费 价值-1 的金币来拆",
                           player)
                    if not owned_cards[from_champion_find_player(kill)]:
                        printp('[ERROR] 没有可拆之物！', player)
                        return
                    printp(f"现有金币 {gold[player]}", player)
                    kill2 = int(inputp("[INPUT] 选择要拆的装备，0为第一件，以此类推，-1为放弃：", player))
                    if kill2 != -1 and 0 <= kill <= len(owned_cards[kill]) - 1:
                        print(f"gold[player] = {gold[player]}")
                        print(
                            f"card_cost.get(owned_cards[kill][kill2]) - 1 = {card_cost.get(owned_cards[kill][kill2]) - 1}")
                        print(f"from_champion_find_player(kill) = {from_champion_find_player(kill)}")
                        if gold[player] >= card_cost.get(owned_cards[kill][kill2]) - 1 and from_champion_find_player(
                                kill) != 4:
                            # 上面这行报错
                            gold[player] -= card_cost.get(owned_cards[kill][kill2]) - 1
                            printb(
                                f'{player_ID[player]} (解脱者) 已使用 {card_cost[owned_cards[kill][kill2]] - 1} 金拆下 {player_ID[kill]} 的装备 {card[owned_cards[kill][kill2]]}')
                            self.cdl.append(owned_cards[kill][kill2])
                            owned_cards[kill].remove(owned_cards[kill][kill2])
                            if_used_skill[player] = True  # player草草草 草草草草草草
                        elif gold[player] < card_cost[owned_cards[kill2]] - 1:
                            printp(f"[ERROR] 拆失败，金钱不足", player)
                            return
                        elif from_champion_find_player(kill) == 4:
                            printp(f"[ERROR] 拆失败，海兽祭司免疫你的技能", player)
                            return
                else:
                    printp(f"[ERROR] 不能拆自己", player)
            else:
                printp(f"已放弃", player)
        else:
            printb(f"[ERROR] 正在开发")

    # 这个还在开发
    def item_skills(self, item, player, kill=None):

        if item == '"你也有份"':
            printb(f'{player_ID[player]} 装备了 "你也有份"，立即获得4金')
            gold[player] += 4

        if item == "上海大炮":
            count = 1
            printb(f"上海大炮 正在产生效果")
            while count <= 1:
                # 上海大炮随机摧毁2件装备
                kill = random.randint(0, player_number - 1)
                try:
                    kill2 = random.randint(0, len(owned_cards[kill]) - 1)
                    # 注意！从0开始计数，后面要 -1 ！搞了好多次了
                    if kill == player and owned_cards[kill][kill2] == 37:
                        printb(f'* {player_ID[player]} 的 上海大炮 想把自己拆掉，但不可以。')
                    elif champion_selected[kill] == 4:
                        printb(f'* {player_ID[player]} 的 上海大炮 想拆 海兽祭司 的装备，但被免疫了。')
                    else:
                        printb(
                            f'* {player_ID[player]} 的 上海大炮 拆下了 {player_ID[kill]} 的装备 {card[owned_cards[kill][kill2]]}！')
                        self.cdl.append(owned_cards[kill][kill2])
                        # print(f"owned_cards = {owned_cards}\nowned_cards[kill][kill2] = {owned_cards[kill][kill2]}")
                        owned_cards[kill].remove(owned_cards[kill][kill2])
                except (IndexError, ValueError):
                    printb(f"* {player_ID[player]} 的 上海大炮 尝试拆 {player_ID[kill]} 的装备，但是他没有！")
                # except ValueError:
                #    printb(f'{player_ID[player]} 的 上海大炮 想拆的人没有装备。')
                count += 1
            printb('')

        if item == "自然之力":
            # 自然之力
            printb(f"自然之力 正在产生效果，为携带者额外获得一个回合")
            turn(champion_selected[player])

        if item == "三相之力":
            if champion_selected[player] == 1 and kill is not None:
                printb(f'三相之力 正在产生效果，为探险家额外偷走一件装备')
                try:
                    kill2 = random.randint(0, len(owned_cards[kill]) - 1)
                    printb(f'* {player_ID[kill]} 的装备 {card[owned_cards[kill][kill2]]} 被偷走')
                    # print(f"owned_cards = {owned_cards}\nowned_cards[kill][kill2] = {owned_cards[kill][kill2]}")
                    owned_cards[player].append(owned_cards[kill][kill2])
                    owned_cards[from_champion_find_player(kill)].remove(owned_cards[kill][kill2])
                except (IndexError, ValueError):
                    printb(f"* {player_ID[player]} 的 三相之力 尝试偷 {player_ID[kill]} 的装备，但是他没有！\n")

    def is_owned(self, item, player):
        # 用来看有没有这件装备。输入item 和 player， 返回True 或 False
        for i in owned_cards[player]:
            if i == item:
                return True
        return False

    def pick_champion(self, king):

        champion_pool = list(range(0, len(champ)))
        champion_selected = [-1 for i in range(player_number)]
        for item in first_loop(king):
            printb(f'''\n\n\n\n****现在轮到 {player_ID[item]} (玩家{item}) 选择英雄
    正在等待玩家操作''')
            printp('''
    *************************************************
    *************************************************
          轮          到          你         了
    *************************************************
    *************************************************
            ''', item)
            '''
            数字. 英雄：
            英雄池: {translate_champ(champion_pool)}
            对应数字：{champion_pool}
            '''
            x = 0
            while x < len(champion_pool):
                printp(f'{champion_pool[x]}. {champ[champion_pool[x]]}', item)
                x += 1
            print(f'已选择: {champion_selected}')
            printp(
                f"\n你的手牌：{translate_shoupai(item)}\n手牌价格：{translate_cost(shoupai[item])}\n你的装备：{translate_card(owned_cards[item])}\n你的金币：{gold[item]}",
                item)
            champion_pick = inputp(f'''[INPUT] 请 {player_ID[item]} (玩家{item}) 从英雄池中选择一名英雄''', item)
            print(f'champion_pick = {champion_pick}')
            try:
                champion_pool.remove(champion_pick)
            except ValueError:
                printp(f"这个英雄已被选择或不存在。已为你从英雄池中随机选择。", x)
                champion_pick[x] = champion_pool[0]
            champion_selected[item] = champion_pick
            printb(f"{player_ID[item]} (玩家{item}) 已完成")
        printb(f'\n还剩下{translate_champ(champion_pool)} 没有被选择。\n')

    def first_loop(self, king):
        a = []
        i = king
        while len(a) < player_number:
            a.append(i)
            if i != player_number - 1:
                i += 1
            else:
                i = 0
        return a

    def from_champion_find_player(self, champion):
        temp = 0
        for item in champion_selected:
            if champion_selected[temp] == champion:
                return temp
            else:
                temp += 1
        return -1  # 要是没找到 返回-1

    def translate_shoupai(self, player):
        # input 玩家id
        # output 他的手牌的翻译版
        translated_list = []
        for item in shoupai[player]:
            translated_list.append(card.get(item))
        return translated_list

    def main(self):
        # 初始化默认数据
        # 一定要global！！！

        # player_number = 8  # 玩家人数
        '''
        gold = [2 for i in range(player_number)]  # 钱
        if_killed = [False for i in range(player_number)]  # 被杀布尔变量
        shoupai = [[] for i in range(player_number)]  # 手牌空的
        if_used_skill = [False for i in range(player_number)]
        '''
        gold = [2 for i in range(player_number)]  # 钱
        if_killed = [False for i in range(player_number)]  # 被杀布尔变量
        if_stolen = [False for i in range(player_number)]  # 被偷布尔变量
        shoupai = [[] for i in range(player_number)]  # 手牌空的
        if_used_skill = [False for i in range(player_number)]
        self.cdl = random.shuffle.list(range(1, len(card)))  # 随机牌堆(从1开始)
        # 作弊牌堆如下
        self.cdl = [22, 22, 22, 22, 22, 22, 22] + list(range(1, len(card)))
        champion_pool = list(range(0, len(champ)))  # 英雄池(从0开始)
        jinchanchan = -1
        is_doubled = False
        getcardvariable = 0  # 发牌变量
        while getcardvariable < player_number:
            getcard(getcardvariable, 2)
            getcardvariable += 1
        owned_cards = [[] for i in range(player_number)]
        champion_selected = random.shuffle.list(range(0, len(champ)))  # 随机英雄
        # champion_selected = [0, 4, 7, 1, 3, 2, 5, 6]  # 固定英雄
        score = [0 for i in range(player_number)]
        king = from_champion_find_player(3)
        if king == -1 or king >= player_number:
            king = 0
        end_the_game = False
        printb(f"""
    初始化{player_number}人场完成""")
        turn_controller()

        def start(self):
            """
            启动服务器
            """
            # 绑定端口
            self.__socket.bind(('192.168.1.106', 5555))
            # 启用监听
            self.__socket.listen(5)
            print(f'服务器已开启。当前版本：{version}，{jirenchang}人场')

            # 清空连接
            self.connections.clear()
            self.nicknames.clear()
            self.connections = []
            self.nicknames = []

            # 清空ID
            player_ID = []
            conti = False

            # 开始侦听
            while True:
                connection, address = self.__socket.accept()
                print('收到一个新连接', connection.fileno())

                # 尝试接受数据
                # noinspection PyBroadException
                try:
                    buffer = connection.recv(1024).decode()
                    # 解析成json数据
                    obj = json.loads(buffer)
                    # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
                    if obj['type'] == 'login' and obj['version'] == version:
                        c = 0
                        cl = False
                        # cl 是重连变量
                        for item in player_ID:
                            if obj['nickname'] == item:
                                cl = True
                                player_ID.append(obj['nickname'])
                                connection.send(json.dumps({
                                    'id': c
                                }).encode())
                                connection.send(json.dumps({
                                    'sender_id': -1,
                                    'message': f'欢迎重连，你的id：{c}，名字：{player_ID[c]}'
                                }).encode())
                                # printp(f'欢迎重连，你的id：{c}，名字：{player_ID[c]}', c)
                                conti = True
                                # 开辟一个新的线程
                                thread = threading.Thread(target=self.__user_thread, args=(c,))
                                thread.setDaemon(True)
                                thread.start()
                                break
                            c += 1
                        if conti == True:
                            conti = False
                            continue
                        if cl is False:
                            self.connections.append(connection)
                            self.nicknames.append(obj['nickname'])
                            player_ID.append(obj['nickname'])
                            connection.send(json.dumps({
                                'id': len(self.connections) - 1
                            }).encode())
                            printp(f'\n{gengxinshuoming}\n\n已在房间中的有 {len(self.connections)} 人',
                                   len(self.connections) - 1)
                            '''
                            for item in player_ID:
                                printp(f"{item}", len(self.connections) - 1)
                            '''
                            # 上面两行效率太低了。改成有几个人在好了
                            printp(f'\n\n*******************\n本房间：\n结束条件：{end_game_items} 件装备\n'
                                   f'人数：{jirenchang}\n*******************\n\n', len(self.connections) - 1)

                            # 开辟一个新的线程
                            thread = threading.Thread(target=self.__user_thread, args=(len(self.connections) - 1,))
                            thread.setDaemon(True)
                            thread.start()
                        # 到时候要删掉的
                        print('检测人数')
                        if player_number == jirenchang:
                            # 记得回来 我删掉试试看
                            '''
                            while len(player_ID) <= 8:
                               player_ID.append('')
                               # 用于填充playerID使得他不要out of range
                            '''
                            printb(f'已有{player_number}人。正在等待服务器确认开始')
                            printb(f'开始游戏')
                            thread2 = threading.Thread(target=main())
                            thread2.setDaemon(True)
                            # 我把游戏线程也视为子线程
                            thread2.start()
                    elif obj['version'] != version:
                        connection.send(json.dumps({
                            'version': version
                        }).encode())
                        print(f'{connection.fileno()} 的版本过低。他的版本：{obj["version"]}')
                    else:
                        print('无法解析json数据包:', connection.getsockname(), connection.fileno())

                        '''
                        while len(player_ID) <= 8:
                            player_ID.append('')
                            print('while 执行一次')
                            # 用于填充playerID使得他不要out of range
                        '''

                except OSError:  # 记得调回去
                    print('断开连接:', connection.fileno())  # 这一行会出现OSError
                    print(f"当前连接数{player_number}")
                except json.decoder.JSONDecodeError:
                    print('JSONDecodeError:', connection.fileno())
                    time.sleep(0.5)
                    connection.close()

    # main()

    end_game_items = 4
    jirenchang = 2
    version = '1.15'
    gengxinshuoming = f"""监狱威龙 {version} 版本更新说明
    体验：
        输入“手牌”“金币”“装备”的反馈更加充分
        现在，输入"shoupai" "jinbi" "zhuangbei" 也可以触发反馈了
        用新的方式解决了黏包、断包问题，提升响应速度
        可读性显著提升
    聊天：
        新增代码：
            /mute all 屏蔽所有人发言
    削弱：
        上海大炮（10金，塞拉斯）：
            摧毁2件装备 --> 1件
            海兽祭司免疫被拆
    BUG修复：
        输错数字不再导致游戏崩溃，但会放弃。
        不会再让有一把金铲铲的玩家直接第一了
    """
    '''
    server = Server()
    server.start()
    '''
    '''
    已知BUG：
        游戏过程中玩家掉线会导致服务器崩溃
        玩家在游戏还没开始时退出会无法开始游戏
        在选择英雄时输入数字有时会变成聊天
    '''


if __name__ == "__main__":
    ED = EventDealer(game="temp")
    thread = threading.Thread(target=ED.start, args=(), daemon=False)

    ED.event_queue.push(Event.GetGold(Player("nihao"), -2))
    ED.event_queue.push(Event.GetGold(Player("nihao"), -2))
    ED.event_queue.push(Event.GetGold(Player("nihao"), -2))
    ED.event_queue.push(Event.GetGold(Player("nihao"), -2))
    ED.event_queue.push(Event.GetGold(Player("nihao"), -2))
    # time.sleep(1)
    thread.start()
    # for _ in range(3):
    #     ED.deal()
