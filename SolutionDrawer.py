import matplotlib.pyplot as plt

class SolDrawer:
    f = plt.figure()
    f.set_figwidth(15)
    f.set_figheight(15)
    @staticmethod
    def get_cmap(n, name='hsv'):
        return plt.cm.get_cmap(name, n)

    @staticmethod
    def draw(itr, sol, nodes, title):
        plt.clf()

        SolDrawer.drawPoints(nodes)
        SolDrawer.drawRoutes(sol)
        plt.title(title)
        plt.savefig(str(itr))

    @staticmethod
    def drawPoints(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            x.append(n.x)
            y.append(n.y)
        for i in range(len(x)):
            if i ==0:
                plt.scatter(x[i], y[i], c="red")
            else:
                plt.scatter(x[i], y[i], c="blue")
        plt.savefig(str('points'))

    @staticmethod
    def drawRoutes(sol):
        cmap = SolDrawer.get_cmap(len(sol.routes) + 1)
        if sol is not None:
            for r in range(0, len(sol.routes)):
                rt = sol.routes[r]
                for i in range(0, len(rt.clients) - 1):
                    c0 = rt.clients[i]
                    c1 = rt.clients[i + 1]
                    plt.plot([c0.x, c1.x], [c0.y, c1.y], c=cmap(r))

    @staticmethod
    def drawTrajectory(searchTrajectory):
        plt.clf()
        plt.plot(searchTrajectory, 'o-')
        plt.title('Search Trajectory')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function')
        plt.savefig(str("SearchTrajectory"))
