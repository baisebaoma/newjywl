import os
import operator
import time
import client.kbdlistener
import colorama
from client.game import 游戏
from client.network import *
colorama.init(autoreset=True)

class UIController:
    current_location = "Login"

    @classmethod
    def search(cls):
        if cls.current_location == 'Game':
            return UIinGame
        elif cls.current_location == 'Room':
            return UIinRoom
        elif cls.current_location == 'End':
            return UIinEnd
        elif cls.current_location == 'Login':
            return UILogin


class UIBase:
    """
    本类是所有UI类的父类，包含基本操作。
    _输出列表(列表)：返回【内容1 内容2 内容3 内容4】（带颜色）
    cls：清屏
    color：加颜色（可重写）
    长宽改变：一般也只用一次
    __汉字计数
    __颜色计数
    __空格补齐（未使用）
    printc
    refresh
    请重写_REFRESH方法。
    """

    键盘监听 = None
    busy = False
    指针 = 0
    宽度 = 55
    高度 = 60
    控制 = ["使用技能", "准备", "饮血剑", "长剑"]

    垂直同步 = True
    总输出 = ''  # 这个给垂直同步用
    输出列表 = None  # 这个给排行榜用

    current_location = "before_game"  # 这个给控制用

    @classmethod
    def _输出列表(cls, 列表):  # 打印列表
        if not 列表:
            return '无'
        字符串 = ''
        for 英雄 in 列表:
            字符串 += f'{cls.color(英雄)} '
        return 字符串[0:-1]  # 删掉最后一个空格

    @staticmethod
    def cls():
        os.system('cls')

    @staticmethod
    def color(消息):

        if 消息 in [""]:
            return f"\033[33m{消息}\033[0m"  # 黄色

        elif 消息 == '德思勤六楼的工头' or 消息 == '瞎子' \
                or 消息 == '机器人' or 消息 == '泰坦':
            return f"\033[31m{消息}\033[0m"  # 红色

        elif 消息 == '我是俊博之王' or 消息 == '霞' or 消息 == '阿卡丽' \
                or 消息 == '瑞兹' or 消息 == '剑姬' or 消息 == '卡莎':
            return f"\033[32m{消息}\033[0m"  # 绿色

        elif 消息 == '昊天金阙无上至尊自然妙有弥罗至真玉皇上帝' or 消息 == '寒冰' or 消息 == '探险家':
            return f"\033[35m{消息}\033[0m"  # 紫色

        elif 消息 == '穿山甲' or 消息 == '亚索':
            return f"\033[36m{消息}\033[0m"  # 天蓝

        elif 消息 == '盖伦':
            return f"\033[44m{消息}\033[0m"  # 天蓝

        else:
            return 消息

    @classmethod
    def 长宽改变(cls):
        os.system('title 监狱威龙客户端（控制台版）')
        os.system(f'MODE con: COLS={cls.宽度} LINES={cls.高度}')

    @staticmethod
    def __汉字计数(内容):
        计数 = 0
        for 字 in 内容:
            if '\u4e00' <= 字 <= '\u9fa5' or 字 in ["（", "）", "，", "。", "？", "！", "；", "：", "、", "“", "”", "《", "》"]:
                计数 += 1
        '''
        if 计数 % 2 == 1:
            计数 += 1
        '''
        return 计数

    @staticmethod
    def __颜色计数(内容):
        指针 = 0
        特殊指针 = 0
        m指针 = 0
        计数 = 0
        while 指针 < len(内容):
            if 内容[指针] <= '\033':
                特殊指针 = 指针
            if 内容[指针] == 'm' and '9' >= 内容[指针 - 1] >= '0':
                m指针 = 指针
                计数 += m指针 - 特殊指针 + 1
                特殊指针 = 0
                m指针 = 0
            指针 += 1
        '''
        if 计数 % 2 == 1:
            计数 += 1
        '''
        return 计数

    @classmethod
    def __空格补齐(cls, 内容):
        return len(内容) + cls.__汉字计数(内容)

    @classmethod
    def draw_line(cls, number=None, 用户名=None):
        if number and 用户名:
            cls.printc(f"-- {number} {用户名} --")
        else:
            cls.printc("  ---------------------------------------------------  ")

    @classmethod
    def printc(cls, 内容, 居中=True):  # 全局控制居中输出，只要垂直同步是True 就会保存到总输出里
        总共计数 = len(内容)
        颜色计数 = cls.__颜色计数(内容)
        汉字计数 = cls.__汉字计数(内容)
        空格数 = cls.宽度 // 2 - 总共计数 // 2 - 汉字计数 // 2 + 颜色计数 // 2
        if 空格数 < 0:
            空格数 = 0
        if not 居中:
            输出 = 内容
        else:
            输出 = ' ' * 空格数 + 内容
        if cls.垂直同步:
            if 内容 == '\n':
                cls.总输出 += '\n'
            else:
                cls.总输出 += 输出 + '\n'
        else:
            if 内容 == '\n':
                print()
            else:
                print(输出)

    @classmethod
    def printi(cls, 内容, 居中=True, delay=0.01):
        总共计数 = len(内容)
        颜色计数 = cls.__颜色计数(内容)
        汉字计数 = cls.__汉字计数(内容)
        空格数 = cls.宽度 // 2 - 总共计数 // 2 - 汉字计数 // 2 + 颜色计数 // 2
        if 空格数 < 0:
            空格数 = 0
        if not 居中:
            输出 = 内容
        else:
            输出 = ' ' * 空格数 + 内容
        if cls.垂直同步:
            if 内容 == '\n':
                cls.总输出 += '\n'
            else:
                cls.总输出 += 输出 + '\n'
        else:
            if 内容 == '\n':
                print()
            else:
                print(" " * 空格数, end="")
                for 字 in 内容:
                    print(字, end="")
                    time.sleep(delay)
                print('\n', end="")
    '''
    @classmethod
    def refresh(cls):
        if cls.busy is False:
            cls._REFRESH()
        else:
            while cls.busy is True:
                time.sleep(0.1)
            cls._REFRESH()
    '''

    @classmethod
    def refresh(cls):
        cls._REFRESH()

    @classmethod
    def _REFRESH(cls):
        pass


class UIinGame(UIBase):
    """UI类负责所有的（文字版本的）UI绘制"""
    垂直同步 = True

    @classmethod
    def __draw_rank(cls):
        rank = 1
        cls.draw_line()
        for 玩家 in cls.输出列表:
            cls.draw_line(number=rank, 用户名=玩家.用户名)
            cls.printc(f"{玩家.金币}金币" + ' ' * 3 +
                       f"{玩家.手牌数}手牌" + ' ' * 3 + str(玩家.积分) + '积分')
            if not 玩家.角色:
                cls.printc(f"【{cls.color('潜伏')}】")
            else:
                cls.printc(f"【{cls.color(玩家.角色)}】")
            cls.printc("英雄池：" + cls._输出列表(玩家.英雄池))
            if 玩家.用户名 == 游戏.自己.用户名:
                cls.printc("你的手牌：" + cls._输出列表(玩家.手牌))
            """
            if 玩家.用户名 == 游戏.自己.用户名:
                牌输出 = "手牌："
                for 牌 in 玩家.手牌:
                    牌输出 += f"{牌} "
                cls.printc(f"【{cls.color(牌)}】")
            """
            if rank != len(cls.输出列表):
                cls.printc('\n')
            rank += 1

    @classmethod
    def __draw_message(cls):
        cls.draw_line()
        条数 = 8
        while len(游戏.消息队列) > 条数:
            del 游戏.消息队列[0]
        for 消息 in 游戏.消息队列:
            cls.printc(消息)
        if len(游戏.消息队列) < 条数:
            for i in range(1, 条数 + 1 - len(游戏.消息队列)):
                cls.printc('\n')

    @classmethod
    def __draw_control(cls):
        距离 = 5
        # 输入系统(阶段)

        if cls.current_location == "before_game":
            cls.控制 = ["准备", "换房间", "换一个"]

        elif cls.current_location == "choose_champion":
            cls.控制 = 游戏.英雄池

        elif cls.current_location == "out_round":
            cls.控制 = 游戏.自己.手牌.copy
            cls.控制[cls.指针] = detail[cls.控制[cls.指针]]

        elif cls.current_location == "choose_gain":
            cls.控制 = ["获得2金币", "获得1张牌"]

        elif cls.current_location == "skill":
            cls.控制 = 游戏.自己.角色.控制()

        cls.draw_line()
        cls.printc(' ' * (cls.宽度 // 4 - 4) + "选项：\n", 居中=False)

        if cls.键盘监听 == 'up' and cls.指针 > 0:
            cls.指针 -= 1
            cls.键盘监听 = None

        elif cls.键盘监听 == 'down' and cls.指针 < len(cls.控制) - 1:
            cls.指针 += 1
            cls.键盘监听 = None

        指针 = 0
        while 指针 < len(cls.控制):
            if 指针 == cls.指针:
                cls.printc(' ' * (cls.宽度 // 4 - 3 - 距离) + ">>" + ' ' * 距离 + str(cls.color(cls.控制[指针])), 居中=False)
            else:
                cls.printc(' ' * (cls.宽度 // 4) + str(cls.color(cls.控制[指针])), 居中=False)
            指针 += 1
        if cls.键盘监听 == 'enter' or cls.键盘监听 == 'space':
            cls.__control(cls.控制[cls.指针])
            # 记得改
            cls.键盘监听 = None

    @classmethod
    def __control(cls, string):
        if cls.current_location == "before_game":
            if string == "准备":
                网络.发送(行为='准备', 对象=cls.控制[cls.指针])
            elif string == "换房间":
                游戏.消息队列.append("该版本不支持换房间。")
                cls.键盘监听 = None
            elif string == "换一个":
                cls.current_location = "choose_gain"
                cls.指针 = 0
                cls.键盘监听 = None

        elif cls.current_location == "choose_champion":
            cls.控制 = 游戏.英雄池

        elif cls.current_location == "out_round":
            cls.控制 = 游戏.自己.手牌.copy
            cls.控制[cls.指针] = detail[cls.控制[cls.指针]]

        elif cls.current_location == "choose_gain":
            cls.控制 = ["获得2金币", "获得1张牌"]

        elif cls.current_location == "skill":
            cls.控制 = 游戏.自己.角色.控制()

        '''
        if string == "准备":
            网络.发送(行为='准备', 对象=cls.控制[cls.指针])
        elif string == "使用技能":
            网络.发送(行为='技能', 对象=游戏.自己.用户名)
            # 这里写技能什么乱七八糟的
        
        else:
            网络.发送(行为=cls.控制[cls.指针], 对象=游戏.自己.用户名)
        '''

    @classmethod
    def __draw_round(cls):
        cls.printc(f"第{游戏.回合}回合")

    @classmethod
    def _REFRESH(cls):
        cls.busy = True
        cls.cls()
        # 复制一份

        cls.输出列表 = 游戏.玩家列表.copy()
        cls.输出列表.append(游戏.自己)
        '''
        try:
            cmpfun = operator.attrgetter('积分')
            cls.输出列表.sort(key=cmpfun, reverse=True)
        except AttributeError:
            pass
        '''
        cls.__draw_round()
        cls.__draw_message()
        try:
            cls.__draw_rank()
        except AttributeError:
            pass
        cls.__draw_control()

        if cls.垂直同步:
            cls.cls()
            print(cls.总输出)
            cls.总输出 = ''

        cls.busy = False


class UILogin(UIBase):
    busy = False
    高度 = 15
    垂直同步 = False

    @classmethod
    def refresh(cls):
        if not cls.busy:
            cls.busy = True
            cls.长宽改变()
            empty_line_number = UILogin.高度 // 3 - 3
            print('\n' * empty_line_number, end='')
            cls.printi("关闭“快速编辑模式”以获得最佳体验\n")
            time.sleep(0.3)
            cls.printi("白色饱马 独立作品\n")
            time.sleep(0.3)
            cls.printi("监狱威龙")
            time.sleep(1)
            print()
            connect = 网络.start()
            if connect is not True:
                if connect == 1:
                    cls.printc('服务器未开启或正在维护。请稍后重试。')
                    time.sleep(30)
                    exit(1)
                elif connect == 2:
                    cls.printc('你在已经连接的连接上再次创建连接。这应该是一个bug，请报告给 baisebaoma。')
                    time.sleep(30)
                    exit(1)
            # 如果上面的连接失败了，就不能够继续下面的操作
            update = 网络.检查更新()
            if not update:
                cls.printc("检测到新版本，请移步打开的网站下载新版本客户端！\n" + update)
                time.sleep(30)
                exit(1)
            cls.printc("输入用户名以登录至服务器\n")
            用户名 = input(" " * (UILogin.宽度 // 3 - 4) + "用户名：")
            cls.printc("正在登录\n")
            网络.登录(用户名)
            client.kbdlistener.键盘监听()
            UIController.current_location = "Game"
            UIController.search().长宽改变()
            UIController.search().refresh()
        else:
            return


class UIinRoom(UIBase):
    pass


class UIinEnd(UIBase):
    pass

