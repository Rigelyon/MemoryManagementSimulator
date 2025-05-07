class Process:
    def __init__(self, name, size, duration):
        self.name = name
        self.size = size
        self.duration = duration
        self.elapsed_time = 0

    def __str__(self):
        return f"{self.name} ({self.size} MB)"