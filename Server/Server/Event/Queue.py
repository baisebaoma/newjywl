
class Queue:
    """
    提供一堆函数:
    is_empty: 若是空 返回 alse 否则返回 True
    print: 打印当前队列
    push: 向末尾添加项
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

