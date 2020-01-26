import socket
import threading
import json


def 接收消息(连接):
    # 输入连接，输出一个含有所有obj的list

    while True:
        全缓存 = ''
        obj分割 = list()
        try:
            # 解决断包问题
            while True:
                缓存 = 连接.recv(1024).decode()
                全缓存 += 缓存
                if 缓存 == '' or 缓存[-1] == '}':
                    break

            # 解决黏包问题
            指针 = 0
            全缓存分割 = list()
            while 指针 < len(全缓存) - 1:
                if 全缓存[指针] == "}" and 全缓存[指针 + 1] == "{":
                    全缓存分割.append(全缓存[0:指针 + 1])  # 注意：包括开头，不包括结尾！
                    全缓存 = 全缓存[指针 + 1:]
                    指针 = -1
                指针 += 1
            全缓存分割.append(全缓存)
            if 全缓存分割:
                for item in 全缓存分割:
                    obj分割.append(json.loads(item))
                全缓存分割.clear()
                return obj分割
            else:
                obj = json.loads(全缓存)
                return list(obj)
        except OSError:
            print(f"{连接.getpeername()} 的连接已断开。")
            return
        # except OSError:
        except json.decoder.JSONDecodeError:
            if 全缓存 == '':
                print('\n可能是客户端关闭或BUG，无法接收信息。')
                return
            else:
                print(f'\n{全缓存}\n')
                print('可能是黏包问题，解码失败，无法显示这句话。')
                return


def 用户线程(连接):
    消息列表 = 接收消息(连接)
    # 检查版本号
    if 消息列表[0]['对象'] != 基本信息.版本:  # 用【对象】存储版本号
        print(f"尝试登录的用户（{连接.getpeername()}）的版本过低。已发送提示更新版本的消息。")
        连接.send(json.dumps(
            {
                '用户': '系统',
                '行为': '拒绝登录：版本',
                '对象': [基本信息.新版本地址, 基本信息.更新说明]
            }
        ).encode())
        # 用【对象】存储新版本地址
        if 消息列表[1:]:
            for 消息 in 消息列表[1:]:
                处理消息(消息, 连接)
    else:
        print(f"尝试登录的用户（{连接.getpeername()}）的版本正确。")
        连接.send(json.dumps(
            {
                '用户': '系统',
                '行为': '版本正确',
                '对象': 0
            }
        ).encode())

    while True:
        消息列表 = 接收消息(连接)
        if 消息列表:
            for 消息 in 消息列表:
                处理消息(消息, 连接)
        else:
            connection_to_be_removed = 玩家控制.搜索连接(连接)
            if connection_to_be_removed is not False:
                玩家控制.玩家列表.remove(connection_to_be_removed)
            连接.close()
            return False


def 处理消息(消息, 连接):
    # 它只能处理单条消息
    print(f"来自 {连接.getpeername()} 的消息：{消息}")
    if 消息['行为'] == '登录':
        # 检查是否重名
        for 对象 in 玩家控制.玩家列表:
            if 对象.用户名 == 消息['用户']:
                print(f"尝试登录的用户（{连接.getpeername()}）选择了一个和已存在用户相同的用户名。请重试。")
                连接.send(json.dumps(
                    {
                        '用户': '系统',
                        '行为': '拒绝登录：重名',
                    }
                ).encode())
                return

        # 以上两个都过了，那么这个玩家应该没问题（还没有写反攻击机制），先加入列表
        玩家控制.玩家列表.append(玩家(用户名=消息['用户'], 连接=连接))

        # 然后发送登录成功的消息（因为这样方便一些）
        玩家控制.私发(消息['用户'], 用户='系统', 行为=f"成功登录")

        # 给这个登录的人发送当前的玩家列表
        for 对象 in 玩家控制.玩家列表:
            玩家控制.私发(消息['用户'], 用户=对象.用户名, 行为='登录')

        # 给这个登录的人发送玩家是否准备
        for 对象 in 玩家控制.玩家列表:
            if 对象.准备 is True:
                玩家控制.广播(用户=对象.用户名, 行为='准备')

        # 给其他的人发送这个人连接的消息
        for 对象 in 玩家控制.玩家列表:
            if 对象.用户名 != 消息['用户']:
                对象.发送(用户=消息['用户'], 行为='登录')

    elif 消息['行为'] == '准备':
        玩家控制.搜索(消息['用户']).准备 = True
        print(f"{消息['用户']} 已准备")
        玩家控制.广播(用户=消息['用户'], 行为='准备')
        全玩家准备 = True
        for 对象 in 玩家控制.玩家列表:
            if 对象.准备 is False:
                全玩家准备 = False
                break
        if 全玩家准备 and len(玩家控制.玩家列表) >= 2:  # and 房主开始:
            玩家控制.广播(用户='系统', 行为=f"游戏开始")
            # 游戏开始
            线程 = threading.Thread(target=游戏.启动, args=())
            线程.start()
            pass

    else:
        pass
        # 玩家控制.广播(行为='广播', 消息=f"{消息['用户名']} 选择了 {消息['消息']}！")


class Server:
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 8888))
        s.listen(5)
        while True:
            connection, address = s.accept()
            print('收到一个新连接', connection.getpeername(), connection.fileno())
            # 第一步检查版本号
            t = threading.Thread(target=用户线程, args=(connection,), daemon=True)
            t.start()