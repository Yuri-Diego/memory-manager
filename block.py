class Block:
    def __init__(self, index, size=2):
        self.index = index
        self.size = size
        self.free = True
        self.process = None
        self.next = None