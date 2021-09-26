from Solution import Solution
from Route import Route

# class for storing relocation move information
from SolutionDrawer import SolDrawer


class relocation_move(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None
    # initialization method
    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9

# class for storing swap move information
class swap_move(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None
        # initialization method
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9

# class for storing twoOpt move information
class two_opt_move(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None
        # initialization method
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9

class Solver:
    def __init__(self, m, n_clients):
        self.allNodes = m.all_nodes
        self.customers = m.customers
        self.matrix_dist = m.matrix_dist
        self.sol = None
        self.bestSolution = None
        self.overallBestSol = None
        self.number_of_clients = n_clients
        self.visited_count = 0
        self.model = m
        self.search_trajectory = []


    def solve(self):
        self.sol = self.find_bad_solution(self.initialize_solution())

        self.VND()

    '''
    Creates a list of 30 empty routes with the capacities given (1200, 1500)
    '''
    def initialize_solution(self):
        init_sol = [Route for x in range(30)]
        for index in range(30):

            if index < 15:
                cap = 1500
            else:
                cap = 1200
            r = Route(cap)

            r.clients.append(self.model.all_nodes[0])
            init_sol[index] = r
        return init_sol

    '''
    Calculates the total cost of the current solution from the
    cost array matrix_dist created in the model class
    '''
    def get_solution_cost(self, solution):
        total_distance = 0.0
        for route in solution:
            for j in range(0, len(route.clients)):
                if not j == len(route.clients) - 1:
                    total_distance += self.model.matrix_dist[route.clients[j].id][route.clients[j + 1].id]
        return total_distance

    # TODO
    def find_bad_solution(self, sol):
        clients_visited = 1
        route_index = 0
        while clients_visited < len(self.allNodes):


            prev_node = sol[route_index].clients[-1]
            candidate_cost = None
            min_cost = 999999999
            min_index = 0
            for candidate_index in range(1, len(self.allNodes)):
                if self.allNodes[candidate_index].id != prev_node.id and not self.allNodes[candidate_index].visited:
                    candidate_cost = self.matrix_dist[prev_node.id][self.allNodes[candidate_index].id]
                    time_after = sol[route_index].time_left - self.model.all_nodes[
                        candidate_index].service_time - candidate_cost / 35
                    load_after = sol[route_index].load + self.allNodes[
                        candidate_index].demand
                    if candidate_cost < min_cost and time_after >= 0 and load_after <= sol[route_index].capacity:
                        min_cost = candidate_cost
                        min_index = candidate_index
                        min_load = load_after
                        min_time_after = time_after
            if min_index == 0:
                route_index += 1
            else:
                sol[route_index].clients.append(self.allNodes[min_index])
                sol[route_index].time_left = min_time_after
                sol[route_index].load = min_load
                sol[route_index].cost = min_cost
                self.allNodes[min_index].visited = True
        sol_to_return = Solution(sol)
        sol_to_return.cost = self.get_solution_cost(sol_to_return.routes)


        sol_to_return = Solution(sol)
        sol_to_return.cost = self.get_solution_cost(sol_to_return.routes)
        return sol_to_return
    '''
    With a given empty Solution object the method is constructing step by step the
    first solution for the optimization problem.
    '''
    def find_first_solution(self, sol):
        print('Finding first solution to the problem')
        # While there are still unvisited clients
        while self.visited_count <= self.number_of_clients:
            candidates = self.initialize_candidates(sol)
            # Variable to check if vehicle is in our base
            vehicle_in_store = False
            min_time = -1
            # Run through all routes in solution
            for routeIndex in range(len(sol)):
                if self.visited_count > self.number_of_clients:
                    break
                self.visited_count = 0
                min_cost = candidates[routeIndex][1]
                # if previous vehicle in base then next vehicle also in base
                if vehicle_in_store:
                    break
                # Run through all clients
                for nodeIndex in range(len(self.model.all_nodes)):
                    # Check if clients has been visited
                    if self.model.all_nodes[nodeIndex].visited:
                        self.visited_count += 1
                        # Terminates if all clients are visited
                        if self.visited_count > self.number_of_clients:
                            break
                        continue
                    # id for the last client in our Route client list
                    id_last_client: int = sol[routeIndex].clients[len(sol[routeIndex].clients) - 1].id
                    # If this route hasn't started yet
                    if id_last_client == 0:
                        vehicle_in_store = True
                    # Cost from last client to candidate client
                    candidate_cost = self.model.matrix_dist[id_last_client][nodeIndex]
                    # Capacity of route after the insertion
                    capacity_after = sol[routeIndex].capacity - sol[routeIndex].load - self.model.all_nodes[nodeIndex].demand
                    # Time of route after the insertion
                    time_after = sol[routeIndex].time_left - self.model.all_nodes[
                        nodeIndex].service_time - candidate_cost / 35
                    # If cost is lower and limitations are not violated
                    if candidate_cost < min_cost and capacity_after >= 0 and time_after >= 0:
                        min_cost = candidate_cost
                        min_node = self.model.all_nodes[nodeIndex]
                        min_time = time_after

                candidates[routeIndex][0] = min_node.id
                candidates[routeIndex][1] = min_cost

            final_min = 10000000
            final_node = None
            final_index = -1

            for i in range(len(candidates)):
                if candidates[i][1] < final_min:
                    final_min = candidates[i][1]
                    final_node = self.model.all_nodes[candidates[i][0]]
                    final_index = i
            if final_index == -1 or min_time == -1:
                continue
            self.model.all_nodes[final_node.id].visited = True
            sol[final_index].time_left -= final_min / 35 + 0.25
            sol[final_index].load += self.model.all_nodes[final_node.id].demand
            sol[final_index].clients.append(final_node)
            sol[final_index].cost += final_min
        sol_to_return = Solution(sol)
        sol_to_return.cost = self.get_solution_cost(sol_to_return.routes)
        print('Cost of first solution: ', sol_to_return.cost)
        return sol_to_return

    def initialize_candidates(self, sol):
        candidates = []
        for i in range(len(sol)):
            candidates.append([-1, 10000000])
        return candidates


    def report_solution(self):
        print('---------------------------------------')
        print()
        print()
        print('Routes of final solution: \n')

        for i in range(len(self.sol.routes)):

            print("Truck", i + 1)
            print("Route: ", end=' ')
            for j in self.sol.routes[i].clients:
                print(j.id, end=' ')
            print('')
            print("Capacity Left: ", self.sol.routes[i].capacity - self.sol.routes[i].load)
            total_loading_time = (len(self.sol.routes[i].clients) - 1) * 0.25
            print('Total km\'s done:', (3.5 - self.sol.routes[i].time_left - total_loading_time) * 35)
            print("Total time: ", 3.5 - self.sol.routes[i].time_left)
            print("----------------------------")
        print(self.sol.cost)

    def find_best_relocation_move(self, rm):
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range (0, len(self.sol.routes)):
                rt2:Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range (1, len(rt1.clients) - 1):
                    for targetNodeIndex in range (0, len(rt2.clients) - 1):

                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.clients[originNodeIndex - 1]
                        B = rt1.clients[originNodeIndex]
                        C = rt1.clients[originNodeIndex + 1]

                        F = rt2.clients[targetNodeIndex]
                        G = rt2.clients[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

                        costAdded = self.matrix_dist[A.id][C.id] + self.matrix_dist[F.id][B.id] + self.matrix_dist[B.id][G.id]
                        costRemoved = self.matrix_dist[A.id][B.id] + self.matrix_dist[B.id][C.id] + self.matrix_dist[F.id][G.id]

                        originRtCostChange = self.matrix_dist[A.id][C.id] - self.matrix_dist[A.id][B.id] - self.matrix_dist[B.id][C.id]
                        targetRtCostChange = self.matrix_dist[F.id][B.id] + self.matrix_dist[B.id][G.id] - self.matrix_dist[F.id][G.id]

                        moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost):
                            self.store_best_relocation_move(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)


    def find_best_swap_move(self, sm):
        for first_rt_index in range(0, len(self.sol.routes)):
            rt1 = self.sol.routes[first_rt_index]
            for second_rt_index in range(first_rt_index, len(self.sol.routes)):
                rt2 = self.sol.routes[second_rt_index]
                for first_node_index in range(1, len(rt1.clients) - 1):
                    start_of_second_index = 1
                    if rt1 == rt2:
                        start_of_second_index = first_node_index + 1
                    for second_node_index in range (start_of_second_index, len(rt2.clients) - 1):

                        a1 = rt1.clients[first_node_index - 1]
                        b1 = rt1.clients[first_node_index]
                        c1 = rt1.clients[first_node_index + 1]

                        a2 = rt2.clients[second_node_index - 1]
                        b2 = rt2.clients[second_node_index]
                        c2 = rt2.clients[second_node_index + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if first_node_index == second_node_index - 1:
                                costRemoved = self.matrix_dist[a1.id][b1.id] + self.matrix_dist[b1.id][b2.id] + self.matrix_dist[b2.id][c2.id]
                                costAdded = self.matrix_dist[a1.id][b2.id] + self.matrix_dist[b2.id][b1.id] + self.matrix_dist[b1.id][c2.id]
                                moveCost = costAdded - costRemoved
                            else:

                                costRemoved1 = self.matrix_dist[a1.id][b1.id] + self.matrix_dist[b1.id][c1.id]
                                costAdded1 = self.matrix_dist[a1.id][b2.id] + self.matrix_dist[b2.id][c1.id]
                                costRemoved2 = self.matrix_dist[a2.id][b2.id] + self.matrix_dist[b2.id][c2.id]
                                costAdded2 = self.matrix_dist[a2.id][b1.id] + self.matrix_dist[b1.id][c2.id]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        else:
                            if rt1.load - b1.demand + b2.demand > rt1.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > rt2.capacity:
                                continue

                            costRemoved1 = self.matrix_dist[a1.id][b1.id] + self.matrix_dist[b1.id][c1.id]
                            costAdded1 = self.matrix_dist[a1.id][b2.id] + self.matrix_dist[b2.id][c1.id]
                            costRemoved2 = self.matrix_dist[a2.id][b2.id] + self.matrix_dist[b2.id][c2.id]
                            costAdded2 = self.matrix_dist[a2.id][b1.id] + self.matrix_dist[b1.id][c2.id]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        if moveCost < sm.moveCost:
                            self.store_best_swap_move(first_rt_index, second_rt_index, first_node_index, second_node_index, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)



    def find_best_twoOpt_move(self, top):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2:Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.clients) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.clients) - 1):
                        moveCost = 10 ** 9

                        A = rt1.clients[nodeInd1]
                        B = rt1.clients[nodeInd1 + 1]
                        K = rt2.clients[nodeInd2]
                        L = rt2.clients[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.clients) - 2:
                                continue
                            costAdded = self.matrix_dist[A.id][K.id] + self.matrix_dist[B.id][L.id]
                            costRemoved = self.matrix_dist[A.id][B.id] + self.matrix_dist[K.id][L.id]
                            moveCost = costAdded - costRemoved
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.clients) - 2 and  nodeInd2 == len(rt2.clients) - 2:
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue

                        if moveCost < top.moveCost:
                            self.store_best_two_opt_move(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):

        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.clients[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.clients[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad

        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.capacity):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.capacity):
            return True

        return False

    def local_search(self):
        self.bestSolution = Solution(self.sol.routes)
        self.bestSolution.cost = self.sol.cost
        terminationCondition = False
        relocation_counter = 0
        print('Starting local search to find local optimum of first solution...')
        print('Using Relocation Move algorithm...')
        while terminationCondition == False:
            sm = swap_move()
            rm = relocation_move()
            rm.Initialize()
            sm.Initialize()
            self.find_best_relocation_move(rm)
            if rm.originRoutePosition is not None:
                if rm.moveCost < 0:
                    self.apply_relocation_move(rm)
                    relocation_counter += 1
                    print(relocation_counter, ' relocation ', 'Cost: ', self.sol.cost)

                else:
                    terminationCondition = True
            self.test_solution()
            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = Solution(self.sol.routes)
                self.bestSolution.cost = self.sol.cost

        self.sol = self.bestSolution
        print('Local optimum cost was found to be: ', self.sol.cost, ' after ', relocation_counter, ' relocation moves')
        print('------------------------------')
        print('')

    def store_best_swap_move(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost

    def store_best_relocation_move(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:relocation_move):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def store_best_two_opt_move(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def apply_two_opt_move(self, top):
        rt1:Route = self.sol.routes[top.positionOfFirstRoute]
        rt2:Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            reversedSegment = reversed(rt1.clients[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            rt1.clients[top.positionOfFirstNode + 1 : top.positionOfSecondNode + 1] = reversedSegment
            rt1.cost += top.moveCost

        else:
            relocatedSegmentOfRt1 = rt1.clients[top.positionOfFirstNode + 1 :]
            relocatedSegmentOfRt2 = rt2.clients[top.positionOfSecondNode + 1 :]
            del rt1.clients[top.positionOfFirstNode + 1:]
            del rt2.clients[top.positionOfSecondNode + 1:]
            rt1.clients.extend(relocatedSegmentOfRt2)
            rt2.clients.extend(relocatedSegmentOfRt1)

            self.update_route_cost_and_load(rt1)
            self.update_route_cost_and_load(rt2)

        self.sol.cost += top.moveCost

    def apply_relocation_move(self, rm: relocation_move):

        oldCost = self.get_solution_cost(self.sol.routes)

        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.clients[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.clients[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.clients.insert(rm.targetNodePosition, B)
            else:
                targetRt.clients.insert(rm.targetNodePosition + 1, B)

            originRt.cost += rm.moveCost
        else:
            del originRt.clients[rm.originNodePosition]
            targetRt.clients.insert(rm.targetNodePosition + 1, B)
            originRt.cost += rm.costChangeOriginRt
            targetRt.cost += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand

        self.sol.cost += rm.moveCost

        newCost = self.get_solution_cost(self.sol.routes)
        #debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
            print('Cost Issue')

    def apply_swap_move(self, sm):
       oldCost = self.get_solution_cost(self.sol.routes)
       rt1 = self.sol.routes[sm.positionOfFirstRoute]
       rt2 = self.sol.routes[sm.positionOfSecondRoute]
       b1 = rt1.clients[sm.positionOfFirstNode]
       b2 = rt2.clients[sm.positionOfSecondNode]
       rt1.clients[sm.positionOfFirstNode] = b2
       rt2.clients[sm.positionOfSecondNode] = b1

       if (rt1 == rt2):
           rt1.cost += sm.moveCost
       else:
           rt1.cost += sm.costChangeFirstRt
           rt2.cost += sm.costChangeSecondRt
           rt1.load = rt1.load - b1.demand + b2.demand
           rt2.load = rt2.load + b1.demand - b2.demand

       self.sol.cost += sm.moveCost
       self.sol.routes[sm.positionOfFirstRoute] = rt1
       self.sol.routes[sm.positionOfSecondRoute] = rt2
       newCost = self.get_solution_cost(self.sol.routes)
       # debuggingOnly
       if abs((newCost - oldCost) - sm.moveCost) > 0.0001:
           print('Cost Issue')


    def update_route_cost_and_load(self, rt: Route):
        tc = 0
        tl = 0
        for i in range(0, len(rt.clients) - 1):
            A = rt.clients[i]
            B = rt.clients[i+1]
            tc += self.matrix_dist[A.id][B.id]
            tl += A.demand
        rt.load = tl
        rt.cost = tc


    def VND(self):
        print('Starting the VND algorithm with inital solution cost: ', self.sol.cost)
        self.bestSolution = Solution(self.sol.routes)
        self.bestSolution.cost = self.sol.cost
        VNDIterator = 0
        kmax = 2
        rm = relocation_move()
        sm = swap_move()
        top = two_opt_move()
        k = 0
        rm_cn_vnd = 0
        sm_cn_vnd = 0
        top_cn_vnd = 0
        while k <= kmax:
            rm.Initialize()
            sm.Initialize()
            top.Initialize()

            if k == 1:
                self.find_best_relocation_move(rm)
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    print('Step ', VNDIterator, ' Applying relocation move')
                    print('Cost before step ', VNDIterator, ': ', self.sol.cost)
                    self.apply_relocation_move(rm)
                    rm_cn_vnd += 1
                    VNDIterator = VNDIterator + 1
                    self.search_trajectory.append(self.sol.cost)
                    k = 0
                else:
                    k += 1
            elif k == 2:
                self.find_best_swap_move(sm)
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    print('Step ', VNDIterator + 1, ' Applying swap move')
                    print('Cost before step ', VNDIterator + 1, ': ', self.sol.cost)
                    self.apply_swap_move(sm)
                    sm_cn_vnd += 1
                    VNDIterator = VNDIterator + 1
                    self.search_trajectory.append(self.sol.cost)
                    k = 0
                else:
                    k += 1
            elif k == 0:
                self.find_best_twoOpt_move(top)
                if top.positionOfFirstRoute is not None and top.moveCost < 0:
                    print('Step ', VNDIterator + 1, ' Applying twoOpt Move move')
                    print('Cost before step ', VNDIterator + 1, ': ', self.sol.cost)
                    self.apply_two_opt_move(top)
                    top_cn_vnd += 1
                    VNDIterator = VNDIterator + 1
                    self.search_trajectory.append(self.sol.cost)
                    k = 0
                else:
                    k += 1

            if (self.sol.cost < self.bestSolution.cost):
                print('Cost after step ', VNDIterator, ': ', self.sol.cost)
                self.bestSolution = Solution(self.sol)
                self.bestSolution.cost = self.sol.cost
            SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
        print('Local optimum cost was found to be: ', self.sol.cost, ' after: ')
        print(rm_cn_vnd, ' Relocation Moves, ')
        print(sm_cn_vnd, ' Swap Moves')
        print(top_cn_vnd, ' TwpOpt Moves')
        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
        SolDrawer.drawTrajectory(self.search_trajectory)


    def test_solution(self):
        totalSolCost = 0
        for r in range (0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            rtLoad = 0
            for n in range (0 , len(rt.clients) - 1):
                A = rt.clients[n]
                B = rt.clients[n + 1]
                rtCost += self.matrix_dist[A.id][B.id]
                rtLoad += B.demand
            if abs(rtCost - rt.cost) > 0.0001:
                print ('Route Cost problem')
            if rtLoad != rt.load:
                print ('Route Load problem')

            totalSolCost += rt.cost

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')