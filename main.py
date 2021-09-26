from Model import Model
from Solver import Solver


m = Model(100)
m.BuildModel()
s = Solver(m, 100)
sol = s.solve()
s.report_solution()


