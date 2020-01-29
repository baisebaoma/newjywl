import socket
import json
import threading
import random


def send(connection, **dictionary):
    connection.send(json.dumps(dictionary).encode())


def receive_message(connection):
    # 输入connection，输出一个含有所有obj的list

    while True:
        full_buffer = ''
        obj_split = list()
        try:
            # 解决断包问题
            while True:
                buffer = connection.recv(1024).decode()
                full_buffer += buffer
                if buffer == '' or buffer[-1] == '}':
                    break

            # 解决黏包问题
            i = 0
            full_buffer_split = list()
            while i < len(full_buffer) - 1:
                if full_buffer[i] == "}" and full_buffer[i + 1] == "{":
                    full_buffer_split.append(full_buffer[0:i + 1])  # 注意：包括开头，不包括结尾！
                    full_buffer = full_buffer[i + 1:]
                    i = -1
                i += 1
            full_buffer_split.append(full_buffer)
            if full_buffer_split:
                for item in full_buffer_split:
                    obj_split.append(json.loads(item))
                full_buffer_split.clear()
                return obj_split
            else:
                obj = json.loads(full_buffer)
                return list(obj)
        except OSError:
            print(f"{connection.getpeername()} 的connection已断开。")
            return
        # except OSError:
        except json.decoder.JSONDecodeError:
            if full_buffer == '':
                print('\n可能是客户端关闭或BUG，无法接收信息。')
                return
            else:
                print(f'\n{full_buffer}\n')
                print('可能是黏包问题，解码失败，无法显示这句话。')
                return


def user_thread(connection):
    message_queue = receive_message(connection)
    # 检查版本号
    if message_queue[0]['version'] != 10.2:  # 用【version】存储版本号
        print(f"尝试登录的用户（{connection.getpeername()}）的版本过低。")
        send(connection, event='VersionNotMatch', target=random.random())
        # 用【target】存储新版本地址
        if message_queue[1:]:
            for message in message_queue[1:]:
                deal(message, connection)
    else:
        print(f"尝试登录的用户（{connection.getpeername()}）的版本正确。")
        send(connection, event='VersionMatch')

    while True:
        message_queue = receive_message(connection)
        if message_queue:
            for message in message_queue:
                deal(message, connection)
        else:
            connection.close()
            return False


def deal(message, connection):
    # 它只能处理单条message
    print(f"{connection.getpeername()} ：{message}")
    if message['行为'] == '登录':
        # 检查是否重名
        for target in 玩家控制.player_list:
            if target.用户名 == message['用户']:
                print(f"尝试登录的用户（{connection.getpeername()}）选择了一个和已存在用户相同的用户名。请重试。")
                connection.send(json.dumps(
                    {
                        '用户': '系统',
                        '行为': '拒绝登录：重名',
                    }
                ).encode())

        # 以上两个都过了，那么这个玩家应该没问题，先加入列表
        玩家控制.player_list.append(玩家(用户名=message['用户'], connection=connection))

        # 然后发送登录成功的message（因为这样方便一些）
        玩家控制.私发(message['用户'], 用户='系统', 行为=f"成功登录")

        # 给这个登录的人发送当前的player_list
        for target in 玩家控制.player_list:
            玩家控制.私发(message['用户'], 用户=target.用户名, 行为='登录')

        # 给这个登录的人发送玩家是否准备
        for target in 玩家控制.player_list:
            if target.准备 is True:
                玩家控制.广播(用户=target.用户名, 行为='准备')

        # 给其他的人发送这个人connection的message
        for target in 玩家控制.player_list:
            if target.用户名 != message['用户']:
                target.发送(用户=message['用户'], 行为='登录')

    elif message['行为'] == '准备':
        玩家控制.搜索(message['用户']).准备 = True
        print(f"{message['用户']} 已准备")
        玩家控制.广播(用户=message['用户'], 行为='准备')
        全玩家准备 = True
        for target in 玩家控制.player_list:
            if target.准备 is False:
                全玩家准备 = False
                break
        if 全玩家准备 and len(玩家控制.player_list) >= 2:  # and 房主开始:
            玩家控制.广播(用户='系统', 行为=f"游戏开始")
            # 游戏开始
            thread = threading.Thread(target=游戏.启动, args=())
            thread.start()
            pass

    else:
        pass
        # 玩家控制.广播(行为='广播', message=f"{message['用户名']} 选择了 {message['message']}！")


class Server:
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 12345))
        s.listen(5)
        while True:
            connection, address = s.accept()
            print('收到一个新connection', connection.getpeername(), connection.fileno())
            # 第一步检查版本号
            t = threading.Thread(target=user_thread, args=(connection,), daemon=True)
            t.start()


if __name__ == "__main__":
    Server().start()
