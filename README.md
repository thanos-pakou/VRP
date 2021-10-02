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

- Constraints - The constraints are that each truck's route ends in their final customer, each route has a time limit that cannot be surpase

## Flow

The program starts by initializing the GUI class and then starts the main loop of the Tkinter library. In the init method of GUI class the graphical environment is being initialized and then first screen is popping up to the screen allowing user to modify some varriables and constraints of the problem. In this screen the user can also select with which algorith the initial solution will occur (either nearest neighbour or minimum iterations. After that, the program finds a solution shows it to the user via pyplot as a graph. The user can see the initial cost and the trucks routes. In this screen the user can press the buttom "Improve Solution" to start the VND algorithm with the first solution as arguement. Then, the VND algorithm find the best combination of swap, rellocation and twoOpt moves and make step by step changes to improve the cost. If the cost cannot be imporved, the algorithm stops. All solutions are being saved in a list, ther best solution is being shown to the user as a graph and all other solutions are being put in a queue. Another thread is starting to pop all other solutions from the queue and saving them as images to then be presented to the user. User also has access to the Trajectory image showing the decrease in the value of the objective function.