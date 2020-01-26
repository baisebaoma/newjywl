import random, socket, threading, json, time, os

from dictionary import *


# 要房间系统和房主 准备系统
# 要分配ID 密码

# 这里的tranlate家族代码重复了好多次 以后再改


def clear():
    os.system('cls')
# 只能在Windows下使用


def printb(string):
    global server
    print(f'\n【发给所有人】\n{string}')
    server.broadcast(message=string)
    time.sleep(0.16)


def printp(string, player):
    global server
    global player_ID
    print(f'\n【发给 {player_ID[player]} (玩家{player})】\n{string}')
    server.connections[player].send(json.dumps({
        'sender_id': -1,
        'sender_nickname': '',
        'message': string
    }).encode())
    time.sleep(0.08)
    # server.connections[player].send(bytes(string, 'UTF-8'))


def inputp(string, player):
    global waiting
    # waiting[0] 是玩家，[1]是内容
    printp(string, player)
    waiting = (None, None)
    while waiting[0] != player:
        time.sleep(0.33)
    if waiting[1] is not None:
        return int(waiting[1])
    return 0
    # 假如 就返回0


def shoupai_count():
    # input nothing
    # output 每个人的手牌张数
    global shoupai
    output = []
    for item in shoupai:
        i = 0
        for item2 in item:
            i += 1
        output.append(i)
    return output


def score_count(player):
    global owned_cards
    c = 0
    for item in owned_cards[player]:
        c += card_score[item]
    return c


def translate_ingame_ID(x):
    return x - 1
# 0 是 系 统


def translate_card(original_card_list):
    translated_list = []
    for item in original_card_list:
        translated_list.append(card.get(item))
    return translated_list


def translate_owned_cards():
    global owned_cards
    global player_number
    translated_list = [[] for temp in range(player_number)]
    i = 0
    for item in owned_cards:
        if item != []:
            for item2 in item:
                translated_list[i].append(card.get(item2))
        i += 1
    return translated_list


def translate_champ(original_champ_list):
    translated_list = []
    for item in original_champ_list:
        translated_list.append(champ.get(item, '无对应英雄'))
    return translated_list


def translate_cost(original_card_list):
    translated_list = []
    for item in original_card_list:
        translated_list.append(card_cost.get(item))
    return translated_list


def translate_score(original_card_list):
    translated_list = []
    for item in original_card_list:
        translated_list.append(card_cost.get(item))
    return translated_list


def translate_color(original_card_list):
    translated_list = []
    for item in original_card_list:
        translated_list.append(card_color.get(item))
    return translated_list


def translate_expla(original_card_list):
    translated_list = []
    for item in original_card_list:
        translated_list.append(card_explanation.get(item))
    return translated_list


def translate_input(a):
    # 假如输入的是英雄中文，那就把它变成对应的英文。输入：字符串 输出：数字
    # 只要加一行kill = translate_input(kill)就可以了
    try:
        int(a)
        return int(a)
    except ValueError:
        if type(a) == str:
            x = 0
            while x <= len(champ) - 1:
                if a == champ.get(x) or a == champ_name.get(x):
                    return x
                x += 1
        return -1

    # a is a string


def getcard(player_to_get, card_to_get):
    global paidui
    global qipaidui
    global gold
    if paidui == [] or len(paidui) < card_to_get:
        printb('[ERROR] 牌堆牌数不够，正在尝试洗牌')
        qipaidui += paidui
        paidui = recard(qipaidui)
    if paidui == [] or len(paidui) < card_to_get:
        printb('[ERROR] 洗牌后牌堆牌数仍不够，已自动转为获得2金')
        gold[player_to_get] += 2
        printb(f'金币 = {gold}')
        return
    i = 1
    while i <= card_to_get:
        shoupai[player_to_get].insert(0, paidui[0])
        paidui.remove(paidui[0])
        i += 1


def getcard1in2(player_to_get):
    global paidui
    global qipaidui
    global shoupai
    if paidui == []:
        printb('[ERROR] 牌堆牌数不够，正在尝试洗牌')
        qipaidui += paidui
        paidui = recard(qipaidui)
    if paidui == []:
        printb('[ERROR] 洗牌后牌堆牌数仍不够，已自动转为获得2金')
        gold[player_to_get] += 2
        printb(f'金币 = {gold}')
        return
    print(translate_card(paidui))
    printp(f'''\n       1. {card[paidui[0]]}   和   2. {card[paidui[1]]}
            {card_cost[paidui[0]]}金                {card_cost[paidui[1]]}金
增益对象：    {champ[card_color[paidui[0]]]}            {champ[card_color[paidui[1]]]}\n''', player_to_get)
    '''
    {card_cost[paidui[0]]}金 和 {card_cost[paidui[1]]}金
增益对象：{champ[card_color[paidui[0]]]} 、{champ[card_color[paidui[1]]]}
    '''
    control = inputp(f'[INPUT]请从 1. {card[paidui[0]]} 和 2. {card[paidui[1]]} 中选择: ', player_to_get)
    if control == 1:
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        shoupai[player_to_get].append(paidui[0])
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        paidui.remove(paidui[0])
    elif control == 2:
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        shoupai[player_to_get].append(paidui[1])
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        paidui.remove(paidui[1])
    paidui.append(paidui[0])
    paidui.remove(paidui[0])


def recard(original_list):
    random.shuffle(original_list)
    string_card_list = []
    return original_list


def playcard(player):
    global shoupai
    global owned_cards
    global gold
    global score
    global player_ID
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
                if card.get(item) == card.get(shoupai[player][pai - 1]) and card.get(shoupai[player][pai - 1]) != '金铲铲':
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


def turn(champion_for_turn):  # player 是自己！！！
    '''
    check if killed
    show champion
    if constructions get extra gold
    choose whether get card or gold
    if constructor then up to 3 card
    if use card
    end
    '''
    global gold
    global shoupai
    global paidui
    global end_the_game
    global king
    global if_killed
    global owned_cards
    global jinchanchan
    global end_game_items
    global player_ID
    global if_stolen
    global is_doubled  # 自然之力
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
            printb(f"{champ[champion_for_turn]} 拥有 {item_count(champion_for_turn)} 个对应装备，已加 {item_count(champion_for_turn)} 金，当前 {gold[player]} 金")
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
            action = int(inputp(f'\n[INPUT] 请 {player_ID[player]} (玩家{player}) 选择：1.获得2金 2.从2张牌中选择1张作为手牌 3.使用技能： ', player))
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
                    print(f'''牌堆 = {translate_card(paidui)}
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
        if not if_used_skill[player] and not(3 <= champion_for_turn <= 6):
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
    global player_number
    global if_killed
    global if_stolen
    global king
    global end_the_game
    global score
    global if_used_skill
    global champion_selected
    global owned_cards

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
                printp(f'你的装备是 {translate_card(owned_cards[from_champion_find_player(c)])} ！\n\n', from_champion_find_player(c))
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
    global end_the_game
    global player_number
    global score
    global jinchanchan
    global player_ID

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
    global end_the_game
    global player_number
    global score
    global jinchanchan
    global player_ID

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
        global score
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
    global owned_cards
    global player_number
    a = len(owned_cards[0])
    for item in owned_cards:
        if len(item) >= a:
            a = len(item)
    return a


def item_count(champion):
    global owned_cards
    player = from_champion_find_player(champion)
    i = 0
    for item in owned_cards[player]:
        if card_color[item] == champion:
            i += 1
    return i


def champion_skills(champion):
    global if_used_skill
    global if_killed
    global if_stolen
    global gold
    global shoupai
    global king
    global owned_cards
    global player_ID

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
                if kill != 1 and kill != 0 and not(if_killed[from_champion_find_player(kill)]) and 0 <= kill <= len(champ) - 1:
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
                printp(f"{player_ID[kill]} 的装备有：{translate_card(owned_cards[from_champion_find_player(kill)])}", player)
                printp(f"价值：{translate_cost(owned_cards[from_champion_find_player(kill)])}\n 你需要花费 价值-1 的金币来拆", player)
                if not owned_cards[from_champion_find_player(kill)]:
                    printp('[ERROR] 没有可拆之物！', player)
                    return
                printp(f"现有金币 {gold[player]}", player)
                kill2 = int(inputp("[INPUT] 选择要拆的装备，0为第一件，以此类推，-1为放弃：", player))
                if kill2 != -1 and 0 <= kill <= len(owned_cards[kill]) - 1:
                    print(f"gold[player] = {gold[player]}")
                    print(f"card_cost.get(owned_cards[kill][kill2]) - 1 = {card_cost.get(owned_cards[kill][kill2]) - 1}")
                    print(f"from_champion_find_player(kill) = {from_champion_find_player(kill)}")
                    if gold[player] >= card_cost.get(owned_cards[kill][kill2]) - 1 and from_champion_find_player(kill) != 4:
                        # 上面这行报错
                        gold[player] -= card_cost.get(owned_cards[kill][kill2]) - 1
                        printb(f'{player_ID[player]} (解脱者) 已使用 {card_cost[owned_cards[kill][kill2]] - 1} 金拆下 {player_ID[kill]} 的装备 {card[owned_cards[kill][kill2]]}')
                        qipaidui.append(owned_cards[kill][kill2])
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
def item_skills(item, player, kill = None):
    global owned_cards
    global player_number
    global qipaidui
    global gold
    global player_ID
    global champion_selected

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
                    qipaidui.append(owned_cards[kill][kill2])
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


def is_owned(item, player):
    # 用来看有没有这件装备。输入item 和 player， 返回True 或 False
    global owned_cards
    for i in owned_cards[player]:
        if i == item:
            return True
    return False


def pick_champion(king):
    global champion_pool
    global champion_selected
    global player_number
    global shoupai

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
        printp(f"\n你的手牌：{translate_shoupai(item)}\n手牌价格：{translate_cost(shoupai[item])}\n你的装备：{translate_card(owned_cards[item])}\n你的金币：{gold[item]}", item)
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


def first_loop(king):
    global player_number
    a = []
    i = king
    while len(a) < player_number:
        a.append(i)
        if i != player_number - 1:
            i += 1
        else:
            i = 0
    return a


def from_champion_find_player(champion):
    temp = 0
    for item in champion_selected:
        if champion_selected[temp] == champion:
            return temp
        else:
            temp += 1
    return -1  # 要是没找到 返回-1


def translate_shoupai(player):
    # input 玩家id
    # output 他的手牌的翻译版
    global shoupai
    global player_number
    translated_list = []
    for item in shoupai[player]:
        translated_list.append(card.get(item))
    return translated_list


def main():
    # 初始化默认数据
    # 一定要global！！！
    global if_used_skill
    global player_number
    global player_ID
    global gold
    global if_killed
    global shoupai
    global paidui
    global qipaidui
    global champion_pool
    global champion_selected
    global king
    global owned_cards
    global score
    global end_the_game
    global waiting  # 这个是用来把游戏内部和游戏外部的input连起来的
    global jinchanchan
    global if_stolen
    global is_doubled

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
    paidui = recard(list(range(1, len(card))))  # 随机牌堆(从1开始)
    # 作弊牌堆如下
    paidui = [22, 22, 22, 22, 22, 22, 22] + list(range(1, len(card)))
    qipaidui = []  # 弃牌堆
    champion_pool = list(range(0, len(champ)))  # 英雄池(从0开始)
    jinchanchan = -1
    is_doubled = False
    getcardvariable = 0  # 发牌变量
    while getcardvariable < player_number:
        getcard(getcardvariable, 2)
        getcardvariable += 1
    owned_cards = [[] for i in range(player_number)]
    # 作弊装备
    # owned_cards[0].append(37)
    # owned_cards[0].append(42)
    # owned_cards[0].append(49)
    champion_selected = recard(list(range(0, len(champ))))  # 随机英雄
    # champion_selected = [0, 4, 7, 1, 3, 2, 5, 6]  # 固定英雄
    score = [0 for i in range(player_number)]
    king = from_champion_find_player(3)
    if king == -1 or king >= player_number:
        king = 0
    end_the_game = False
    printb(f"""
初始化{player_number}人场完成""")
    turn_controller()


class Server:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        global waiting
        global player_number
        player_number = 0
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = list()
        self.nicknames = list()

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        global player_number
        global waiting
        global shoupai
        global gold
        global player_ID
        global owned_cards

        connection = self.connections[user_id]
        nickname = self.nicknames[user_id]
        print(f'玩家{user_id}(USER_ID) {nickname}(ID) {connection.fileno()}(fileno) 加入房间')
        player_number += 1
        try:
            self.broadcast(message=f'玩家 {nickname} ({user_id}) 已准备')
        except AttributeError:
            pass
        print(f"当前连接数{player_number}")
        '''
        print("检测人数")
        if player_number == 2:
            # self.broadcast(message=f'已有{player_number}人。正在等待服务器确认开始')
            printb(f'已有{player_number}人。正在等待服务器确认开始')
            printb('开始游戏')
            '''

        '''
            thread2 = threading.Thread(target=main())
            thread2.setDaemon(True)
            # 我把游戏线程也视为子线程
            thread2.start()
        '''

        # 侦听
        while True:
            # noinspection PyBroadException
            try:
                '''
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                '''
                '''
                fuffer = ''
                # noinspection PyBroadException
                while True:
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    # print(f"fuffer = {fuffer}")
                    # print(buffer)
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break
                obj = json.loads(fuffer)
                '''
                # 解决断包问题
                fuffer = ''
                while True:
                    buffer = connection.recv(1024).decode()
                    fuffer += buffer
                    # print(f"fuffer = {fuffer}")
                    # print(buffer)
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break
                obj = json.loads(fuffer)
                # 如果是广播指令
                if obj['type'] == 'broadcast':
                    try:
                        if obj['message'] == '手牌' or obj['message'] == 'shoupai':
                            # printp(f"\n你的手牌：{translate_shoupai(obj['sender_id'])}\n所有人的手牌数：{shoupai_count()}\n", obj['sender_id'])
                            full_string = f"\n你的手牌：{translate_shoupai(obj['sender_id'])}\n\n"
                            name = 0
                            while name < len(player_ID):
                                full_string += f'{player_ID[name]} (玩家 {name})：{shoupai_count()[name]}张牌\n'
                                name += 1
                            printp(full_string, obj['sender_id'])
                        elif obj['message'] == '金币' or obj['message'] == 'jinbi':
                            # printp(f"\n你的金币：{gold[obj['sender_id']]}\n所有人的金币：{gold}\n", obj['sender_id'])
                            full_string = f"\n你的金币：{gold[obj['sender_id']]}\n"
                            name = 0
                            while name < len(player_ID):
                                full_string += f'{player_ID[name]} (玩家 {name})：{gold[name]}金\n'
                                name += 1
                            printp(full_string, obj['sender_id'])
                        elif obj['message'] == '装备' or obj['message'] == 'zhuangbei':
                            # printp(f"\n所有人的装备：{translate_owned_cards()}\n", obj['sender_id'])
                            full_string = '\n'
                            name = 0
                            while name < len(player_ID):
                                full_string += f'{player_ID[name]} (玩家 {name})：{translate_card(owned_cards[name])}\n'
                                name += 1
                            printp(full_string, obj['sender_id'])
                        else:
                            self.broadcast(obj['sender_id'], obj['message'])
                            print(f"【聊天】{player_ID[obj['sender_id']]} ({obj['sender_id']}) 说：{obj['message']}")
                    except NameError:
                        printp('无法使用代码：游戏还没开始！', obj['sender_id'])
                elif obj['type'] == 'input':
                    waiting = (obj['sender_id'], obj['message'])
                    print(f"收到 {player_ID[obj['sender_id']]} (玩家{obj['sender_id']}) ：{obj['message']}，类型：{obj['type']}")
                elif obj['type'] == 'cheat':
                    try:
                        if obj['message'] == 'showmethemoney':
                            gold[obj['sender_id']] += 10
                            printb(f"{player_ID[obj['sender_id']]} (玩家 {obj['sender_id']}) 使用了作弊代码，获得10金。"
                                   f"\n当前金钱：{gold[obj['sender_id']]}")
                        elif obj['message'] == 'gimmeaspatula':
                            owned_cards[obj['sender_id']].append(38)
                            printb(f"{player_ID[obj['sender_id']]} (玩家 {obj['sender_id']}) 使用了作弊代码，获得金铲铲。"
                                   f"\n当前装备：{translate_card(owned_cards[obj['sender_id']])}")
                    except NameError:
                        printp('无法使用代码：游戏还没开始！', obj['sender_id'])
                else:
                    print('[Server] 无法解析json数据包:', connection.fileno(), self.nicknames[user_id])
                    #  connection.getsockname(), connection.fileno(),
            except OSError:
                # print(f'\n\n{buffer}\n\n')
                print('连接失效:', connection.fileno(), self.nicknames[user_id])
                self.connections[user_id].close()
                # self.connections[user_id] = None
                # self.nicknames[user_id] = None 我要开发断线重连 所以这个必须删掉
                player_number -= 1
                print(f"当前连接数{player_number}")
                break
            except json.decoder.JSONDecodeError:
                if buffer == '':
                    print(f'{self.nicknames[user_id]}已断开连接')
                    self.connections[user_id].close()
                    self.connections[user_id] = None
                    self.nicknames[user_id] = None
                    player_number -= 1
                    print(f"当前连接数{player_number}")
                    return
                print('JSONDecodeError:', connection.fileno(), self.nicknames[user_id])
                time.sleep(0.1)

    def broadcast(self, user_id=-1, message=''):
        """
        广播
        :param user_id: 用户id(-1为系统)
        :param message: 广播内容
        """
        for i in range(0, len(self.connections)):
            if user_id != i and self.connections[i] is not None:
                self.connections[i].send(json.dumps({
                    'sender_id': user_id,
                    'sender_nickname': self.nicknames[user_id],
                    'message': message
                }).encode())

    def start(self):
        """
        启动服务器
        """
        global player_ID
        global player_number
        global jirenchang
        global version
        global gengxinshuoming
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
                        printp(f'\n{gengxinshuoming}\n\n已在房间中的有 {len(self.connections)} 人', len(self.connections) - 1)
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

            except OSError: # 记得调回去
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
server = Server()
server.start()
'''
已知BUG：
    游戏过程中玩家掉线会导致服务器崩溃
    玩家在游戏还没开始时退出会无法开始游戏
    在选择英雄时输入数字有时会变成聊天
'''

