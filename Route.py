class Route:
    clients = []

    def __init__(self, capacity, time):
        self.clients = []
        self.time_left = time
        self.capacity = capacity
        self.load = 0
        self.cost = 0
