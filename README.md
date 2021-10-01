# VRP Solver

## Intro

This project is made to solve a general VRP and present the solution to the user with some specific constraints. Project made using python and it uses tkinter for a basic GUI. 

## Description

The first step to solve an optimization problem is to create a model and define the objective function that we want to optimize. After that, we define the constraints of the problem and then we decide how are we going to apporach the solution. There are many ways including linear programming to find the optimal solution. Problem is, linear programming takes a lot of time and most of the times we cannot afford that. That's why this project's apporach is greedy using a simple constructive algorithm to create an initial solution and then with a VND algorithm it improves it step by step locally hoping that we are going to reach a global optimum. The solution might not be the best, but it gives a feasible solution pretty fast.

The VRP problem specifics:
- Model - The model needs the array with all the clients, the depot location (x,y), the service time each truck needs to serve a customer and the speed of the trucks. The model creates by itself, randomly with specific seed, the clients locations and the demand of each customer.
Οι τεχνολογίες που χρησιμοποιήθηκαν είναι οι εξείς.

- Route - Each route has an array with clients that will serve, the time that ihat it has left (initial time given by user),
- total capacity (given by user), load and cost.

- Client - Each client has an id, a service time (given by user), the demand, and the x y location.

- Solution - The solution is a class containing a list of Routes and the total cost.

- Constraints - The constraints are that each truck's route ends in their final customer, each route has a time limit that cannot be surpassed, each route has a capacity limit, each customer has to be served only by 1 truck-route.


