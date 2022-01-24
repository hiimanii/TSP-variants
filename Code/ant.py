import math
import random
import numpy

class Ant:

    def __init__(self, i, aco):
        self.index = i
        self.reset_ant(aco)
        self.aco = aco
        self.routing_table = numpy.full((aco.num_cities,aco.num_cities),(1.00/(aco.num_cities-1)))

    def reset_ant(self, aco):
        self.path_length = 0  # initial ant's path length
        # starting city is indexed at 0
        self.currCity = aco.cities[0]
        self.path = []
        self.path.append(aco.cities[0])
        # unvisited cities for the current ant
        self.unvisited = []
        self.unvisited.extend(aco.cities[1:])
        # the probability distribution for the next city
        self.transition_probs = []

    def city_sum(self, city_cur,city_next):
        return ((math.pow(self.aco.pheromone[city_cur.index][city_next.index], self.aco.alpha))*(math.pow(self.aco.attractiveness[city_cur.index][city_next.index],self.aco.beta)))

    def update_table(self):
        denom = 0.0
        for c in self.path:
            temp_cities = list(self.path)
            temp_cities.remove(c)
            for valid in temp_cities:
                denom += self.city_sum(c, valid)

            for valid in temp_cities:
                numerator = self.city_sum(c, valid)
                if denom > 0:
                    self.routing_table[c.index][valid.index] = numerator/denom
                else:
                    self.routing_table[c.index][valid.index] = 0

    # city_y: the next city
    def get_prob(self, city_y):
        b = 0
        a = self.routing_table[self.currCity.index][city_y.index]
        for c in self.unvisited:
            b = b + self.routing_table[self.currCity.index][c.index]
        trans_prob = a/float(b)
        return trans_prob

    def euclidean_distance(self, a, b):
        return (math.sqrt(math.pow((a.x - b.x), 2.0) + math.pow((a.y - b.y), 2.0)))

    def calc_edge_length(self):
        sum_dist=0.00
        for i in range(0,len(self.path)):
            try:
                eucli_dist =  self.euclidean_distance(self.path[i], self.path[i+1])
                sum_dist += eucli_dist
                self.path_length = sum_dist
            except:
                return sum_dist
