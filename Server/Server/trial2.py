__queue = list()


def is_empty():
    global __queue
    if __queue:
        return True
    else:
        return False

print(is_empty())
