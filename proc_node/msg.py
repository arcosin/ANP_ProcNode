

MSG_TYPES = ["msg", "conn", "disc"]


class Msg:
    def __init__(self, type, data):
        super().__init__()
        self.type = type
        self.data = data

#===============================================================================
