import os

from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


G = nx.Graph()

fileName = "resources/distances.csv"
htmlFileName = 'resources/grid.html'
symbol_to_replace = ';'
firstLineSkip = True

edges = list()

with open(fileName) as file:
    for line in file.readlines():
        if firstLineSkip:
            firstLineSkip = False
            continue

        if line == "\n":
            continue

        fromThe = str(line.split(symbol_to_replace)[0].replace("\"", ""))
        toThe = str(line.split(symbol_to_replace)[1].replace("\"", "").replace("", ""))
        weigh = str(line.split(symbol_to_replace)[2].replace("\"", "").replace("\n", ""))

        print("FROM {} TO {} WEIGHT {}".format(fromThe, toThe, weigh))

        edges.append([fromThe, toThe])
        G.add_edge(fromThe, toThe, length=weigh)

net = Network()
net.from_nx(G)
net.height = '1080px'
net.width = '1920px'
net.show(htmlFileName)

os.system("open resources/grid.html")
