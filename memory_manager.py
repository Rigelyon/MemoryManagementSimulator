class MemoryBlock:
    def __init__(self, start, size, is_free=True, process=None):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process = process
        self.end = start + size - 1