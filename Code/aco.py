#!/usr/bin/env python
import numpy
import math
import ant
import types
import random
from random import shuffle

from multiprocessing import Process, Queue, Pool, Manager
from functools import partial

# Parameters used -
# index - stores the city number
# x - x coordinate for the city i
# y - y coordinate for the city i
class City:
    def __init__(self,i=0, x_cord=0, y_cord=0):
        self.index = i
        self.x = x_cord
        self.y = y_cord

# Parameters used -
# num_cities - number of cities for travel
# initial_pheromone - initial value of pheromone deposited
# alpha - weight parameter for pheromones
# beta - weight parameter for desirability (attractiveness), which is inverse of distance
# pheromone_deposit - amount of pheromones which can be deposited
# evaporation_constant - amount of pheromone which will evaporate after a cycle
class ACO:
    def __init__(self, num_cities, initial_pheromone=1, alpha=1, beta=2,
                pheromone_deposit=1, evaporation_constant=0.4):
        self.cities = []
        self.shortest_paths = []
        self.shortest_paths_lens = []
        self.shortest_path_len = -1
        self.evaporationConst = evaporation_constant
        self.pheromone_deposit = pheromone_deposit
        self.pheromone = numpy.full((num_cities,num_cities),initial_pheromone)
        self.alpha = alpha
        self.beta = beta
        self.attractiveness = numpy.zeros((num_cities,num_cities))
        self.num_cities = num_cities
        # self.routing_table = numpy.full((num_cities,num_cities),(1.00/(num_cities-1)))

    # Adding cities present in the dataset
    def add_nodes(self, city):
        if isinstance(city, list):
            self.cities.extend(city)
        else:
            self.cities.append(city)

    # Use euclidean formula to calculate distance between two cities.
    # Cities class has x and y coordinates
    def euclidean_distance(self,city1,city2):
        return  (math.sqrt(math.pow((city1.x-city2.x),2)+math.pow((city1.y-city2.y),2)))

    # Attractiveness is reciprocal of distance. This function calculates
    # attractiveness between cities.
    def compute_attractiveness(self):
        city_list=self.cities
        for i in range(len(city_list)):
            for j in range(len(city_list)):
                distance = self.euclidean_distance(city_list[i], city_list[j])
                if distance > 0:
                    self.attractiveness[i][j] = 1/distance
                else:
                    self.attractiveness[i][j] = 0.00

    # a - a single ant
    # pheromone deposit on each path is updated by the ant visiting that path
    # we have deposited the phermone uniformly across the path
    # additionally, evaporation part is removed from the pheromone
    def update_pheromone(self,a, path_len):
        tmp = len(a.path)
        weight = 1/(path_len*(1-self.evaporationConst)) ## Q/L
        for i in range(0,tmp+1):
            try:
                # curr_pher = self.pheromone[a.path[i].index][a.path[i+1].index]
                self.pheromone[a.path[i%tmp].index][a.path[(i+1)%tmp].index] += weight
                self.pheromone[a.path[(i+1)%tmp].index][a.path[i%tmp].index] += weight
            except:
                break
        # self.pheromone = self.pheromone*(1-self.evaporationConst)

    # get the pheromone value for the path between city i and j
    def get_pheromone(self,i,j):
        return self.pheromone[i][j]

    def mp_tour(self,ant,q):
        # print(ant)
        # print(q)
        ant.reset_ant(self)
        # print("eeee")
        while(ant.unvisited):
            # print("wait")
            if random.random()<0:
                next_city = ant.unvisited.pop(random.randint(0,len(ant.unvisited)-1))
                ant.path.append(next_city)
                ant.currCity = next_city

            else:
                for c in ant.unvisited:
                    ant.transition_probs.append(ant.get_prob(c))

                ant.transition_probs = ant.transition_probs/sum(ant.transition_probs)
                selection = numpy.random.choice(ant.unvisited, 1, p = ant.transition_probs)
                next_city = selection[0]
                ant.path.append(next_city)
                ant.currCity = next_city
                ant.unvisited.pop(ant.unvisited.index(next_city))
            ant.transition_probs = []
        q.put(ant)
        # return ant,q

    # Getting the best path by traversing the number of ants num_steps times
    def best_path(self, num_ants=2, num_steps=3):
        ants = []
        self.compute_attractiveness()
        shuffle(self.cities)

        for i in range(0, num_ants):
            ants.append(ant.Ant(i, self))
        # print(ants)
        for step in range(0, num_steps):
            print("Step: {} of {}".format(step+1, num_steps))
            path_lens = []
            paths = []
            procs = []

            m = Manager()
            q = m.Queue()
            # print("0")
            p = Pool(10)
            pool_tuple = [(x, q) for x in ants]
            # tmp_ants = []
            with Pool(processes=10) as pool:
                pool.starmap(self.mp_tour, pool_tuple)
            ants = []
            while q.empty() == False:
                ants.append(q.get())
            # print("3")
            # print(ants)
            for a in ants:
                path_len = a.calc_edge_length()
                path_lens.append(path_len)
                paths.append(a.path)
                self.update_pheromone(a,path_len)
            self.pheromone = self.pheromone*(1-self.evaporationConst)
            # print(self.pheromone)
            for a in ants:
                a.update_table()
            # print("4")
            best_path_len = min(path_lens)
            best_path = paths[path_lens.index(best_path_len)]

            print("Step best path: {} Step: {}".format(best_path_len, step+1))

            self.shortest_paths.append(best_path)
            self.shortest_paths_lens.append(best_path_len)

        output_index = self.shortest_paths_lens.index(min(self.shortest_paths_lens))
        output_path = self.shortest_paths[output_index]
        self.shortest_path_len = self.shortest_paths_lens[output_index]
        self.shortest_paths = []
        self.shortest_paths_lens = []

        return output_path
