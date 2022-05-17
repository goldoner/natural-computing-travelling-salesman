import operator
import os
import random
from copy import deepcopy

import networkx as nx
from matplotlib import pyplot as plt
from pyvis.network import Network


class Tsp:

    def __init__(self):

        # initialize arguments
        self.population = 8
        self.parents = []
        self.children = []
        # create 2D list
        self.cities = [[]]
        self.cities = [[0 for i in range(self.population)] for i in range(self.population)]
        self.createCities()
        self.bests = []
        self.final = []

    # fill the 2D list with the travel distances of this problem
    def createCities(self):
        self.readFromFile()

    def readFromFile(self):

        with open("resources/distances.csv") as file:
            # i = 0
            symbol_to_replace = ";"
            for line in file.readlines():
                if line.__contains__("FromCity;ToCity;Distance"):
                    continue
                if line == "\n":
                    continue
                # i += 1

                fromThe = int(line.split(symbol_to_replace)[0])
                toThe = int(line.split(symbol_to_replace)[1])
                length = int(line.split(symbol_to_replace)[2].replace("\n", ""))
                self.cities[fromThe][toThe] = length

    # make sure that the crossover list has not any duplicate values.
    def isUnique(self, childpos, temp):

        sample = [k for k in range(8)]
        for i in childpos:

            for index, k in enumerate(temp):
                # if a duplicate value from the first and second part of the list
                if i == k:

                    del temp[index]
                    for s in sample:
                        t = childpos + temp
                        # replace it with a value that does not already exists
                        if s not in t:
                            temp.insert(index, s)
                            break
        return temp

    # do a crossover action between two parents
    def crossover(self, v1, v2, ratio=3):

        rem_char = len(v1) - ratio
        clone1 = v1.copy()
        clone2 = v2.copy()

        # split the list in parts
        child1pos = clone1[:rem_char]
        child2pos = clone2[:rem_char]
        child1suf = clone1[-ratio:]
        child2suf = clone2[-ratio:]
        # check for duplicates
        unique1 = self.isUnique(child1pos, child2suf)
        unique2 = self.isUnique(child2pos, child1suf)
        # create children
        child1 = child1pos + unique1
        child2 = child2pos + unique2
        # return children
        return child1, child2

    # calculate fitness for each route
    def fitness(self, child):

        result = 0
        for i in range(0, len(child) - 2):
            result += self.cities[child[i]][child[i + 1]]
        return result

    # sort children and keep the 4 best
    def selection(self, lists):

        bests = []
        self.bests = []
        for i in lists:
            # calculate fitness and append in tuple for reference
            cost = self.fitness(i)
            bests.append((cost, i))

        # sort the  tuple by fitness function
        bests.sort(key=operator.itemgetter(0))
        self.bests = bests
        # keep only 4 best children
        bests = [x[1] for x in bests][:4]
        return bests

    # initialize the class program by creating parents
    def initialize(self):

        for i in range(self.population // 2):
            vector = random.sample(range(8), 8)
            self.parents.append(vector)

    # evaluate the GA algorithm
    def evalutation(self):

        self.children = []
        length = len(self.parents)
        ratio = random.randint(1, length)
        # crossover parents and create 2Xparents list of children
        crossovered1 = self.crossover(self.parents[0], self.parents[1], ratio)
        crossovered2 = self.crossover(self.parents[1], self.parents[2], ratio)
        crossovered3 = self.crossover(self.parents[2], self.parents[3], ratio)
        crossovered4 = self.crossover(self.parents[3], self.parents[0], ratio)
        self.children.append(crossovered1[0])
        self.children.append(crossovered1[1])
        self.children.append(crossovered2[0])
        self.children.append(crossovered2[1])
        self.children.append(crossovered3[0])
        self.children.append(crossovered4[1])
        self.children.append(crossovered4[0])
        self.children.append(crossovered4[1])
        # mutate children by randomize them
        mutated = self.mutation(self.children)
        # get the sorted selection
        selection = self.selection(mutated)
        self.parents = selection

    # mutate children under a certain property
    def mutation(self, children):

        choices = []
        # hardcopy the children list to avoid reference issues
        copies = deepcopy(children)
        # check that the above will happen three unique times
        while len(choices) < 3:
            # create a random index
            choice = random.randint(0, len(copies) - 1)
            # calculate a random boundary for the randomizing mutation process
            boundary = random.randint(0, len(copies) - 1)
            # check again for multiplied indexes
            if choice not in choices:
                # if the index is larger that the boundary do the mutation (randomizer)
                if choice >= boundary:
                    chosen = copies[choice]
                    # shuffle the array by changing the indexes of the values
                    random.shuffle(copies[choice])
                choices.append(choice)

        return copies

    # run the program
    def run(self, iter=1000):

        total = []
        self.initialize()
        for i in range(iter):
            self.evalutation()
            best = self.bests[0]
            total.append(best)
            # sort the best children list and print the best children as outcome of this program
        total.sort(key=operator.itemgetter(0))
        found = total[0]
        self.final = list(found[1])
        print("The sortest path under {} iterations is {} with cost {}".format(iter, found[1], found[0]))


t = Tsp()
t.run()

fin = t.final

result_edges = []

print(len(fin))
for i in range(len(fin) - 1):
    result_edges.append((fin[i], fin[i + 1]))
    # print("({},{})".format(fin[i], fin[i + 1]))

print(result_edges)


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

        G.add_node(fromThe)
        G.add_node(toThe)

        # print("FROM {} TO {} WEIGHT {}".format(fromThe, toThe, weigh))
        tup = (int(toThe), int(fromThe))
        revTup = (int(fromThe), int(toThe))
        if tup in result_edges or revTup in result_edges:
            G.add_edge(fromThe, toThe, length=weigh, color='red')
        else:
            G.add_edge(fromThe, toThe, length=weigh, color='black')

        edges.append([fromThe, toThe])

# G.edges[6][4][]

# G[6][4]["weight"] = 4.7
# G.edges[1, 2].update({0: 5})

# G.edges["6"]["4"]['color'] = "red"
# G.edges[6, 4].update({6, 4, length = 5})
# G.ed

net = Network()
net.from_nx(G)
net.height = '1080px'
net.width = '1920px'
net.show(htmlFileName)

# os.system("open resources/grid.html")
