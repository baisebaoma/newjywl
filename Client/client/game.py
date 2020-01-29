class 基本信息:
    版本 = 2.1


class 玩家:
    金币 = 0
    角色 = None  # None = 未公布
    地 = list()
    建筑次数 = 1
    手牌 = list()  # 这个只给自己用
    积分 = 0
    准备 = False
    被偷钱 = False
    被换牌 = False
    被杀 = False
    优先 = False

    def __init__(self, 用户名):
        self.用户名 = 用户名


class 游戏:
    自己 = 玩家("")

    class 玩家列表类(list):
        def __init__(self, *args):
            super().__init__(*args)

        def 搜索(self, 用户名):
            for 玩家 in self:
                if 玩家.用户名 == 用户名:
                    return 玩家
            return None
    房间名 = '' + '的房间'
    玩家列表 = 玩家列表类()
    消息队列 = list()
    输入 = None
    控制 = list()
    手牌 = list()
    回合 = 1

    @classmethod
    def 启动(cls):
        for 玩家 in cls.玩家列表:
            玩家.金币 = 2


