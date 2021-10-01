import random
import math
from Client import Client
from SolutionDrawer import SolDrawer

class Model:
# instance variables
    def __init__(self, n_customers, depot_location, service_time, speed):
        self.all_nodes = []
        self.customers = []
        self.matrix_dist = []
        self.matrix_time = []
        self.number_of_customers = n_customers
        self.depot_x = depot_location[0]
        self.depot_y = depot_location[1]
        self.service_time = service_time
        self.speed = speed

    def BuildModel(self):



        customers = []
        depot = Client(0, 0, 0, self.depot_x, self.depot_y)
        depot.visited = True
        self.all_nodes.append(depot)
        random.seed(1)


        for i in range(0, self.number_of_customers):
            id = i + 1
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            st = self.service_time  # 15 minutes in hrs
            cust = Client(id, st, dem, xx, yy)
            self.all_nodes.append(cust)
            self.customers.append(cust)


        rows = len(self.all_nodes)
        self.matrix_dist = [[0.0 for x in range(rows)] for y in range(rows)]
        self.matrix_time = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.all_nodes)):
            for j in range(0, len(self.all_nodes)):
                a = self.all_nodes[i]
                b = self.all_nodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix_time[i][j] = dist / self.speed
                self.matrix_dist[i][j] = dist




