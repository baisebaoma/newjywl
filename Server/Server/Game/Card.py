from Game.Champion import Champion


class Card:
    class __Card:
        pass

    class GoldMaker(__Card):
        name = "金币制造厂"
        value = 8
        buff = (Champion.Emperor, )
