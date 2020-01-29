@classmethod
def __draw_control(cls):
    距离 = 5
    # 输入系统(阶段)
    cls.draw_line()
    print(' ' * (cls.宽度 // 4 - 4) + "选项：\n")
    if cls.键盘监听 == 'up' and cls.指针 > 0:
        cls.指针 -= 1
        cls.键盘监听 = None
    if cls.键盘监听 == 'down' and cls.指针 < len(cls.控制) - 1:
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
    if string in ("准备",):
        网络.发送(行为='准备', 对象=cls.控制[cls.指针])
    elif string == "使用技能":
        if 游戏.自己.回合:  # 记得去 自己.回合 写 True,这是个布尔
            网络.发送(行为='技能', 对象=游戏.自己.用户名)
            # 这里写技能什么乱七八糟的

    else:
        网络.发送(行为=cls.控制[cls.指针], 对象=游戏.自己.用户名)
