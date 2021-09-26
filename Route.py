class Route:
    clients = []

    def __init__(self, capacity):
        self.clients = []
        self.time_left = 3.5
        self.capacity = capacity
        self.load = 0
        self.cost = 0
