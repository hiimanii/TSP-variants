import random
import numpy as np
import matplotlib.pyplot as plt
class Star:
    def __init__(self, initial_solution):
        self.current_solution = initial_solution


        
        
class BlackHoleOptimisation:
    def generate_random_solution(self):
        self.num_candidates = self.num_candidates+1
        soln = [i for i in range(self.m)]
        random.shuffle(soln)
        return soln
    
    def calculate_cost(self, idx):
#         print("idx: ",idx)
        curr_soln = self.list_stars[idx].current_solution
        begin = curr_soln[0]
        end = curr_soln[-1]
        cost = self.dataset[begin][end]
        for i in range(1,self.m):
            first = curr_soln[i]
            second = curr_soln[i-1]
            cost = cost + self.dataset[first][second]
        return cost
    
    def update_black_hole(self):
        max_val = self.calculate_cost(self.black_hole_idx)
        max_idx = self.black_hole_idx
        for i in range(self.num_stars):
            curr_val = self.calculate_cost(i)
            if curr_val < max_val:
                max_val = curr_val
                max_idx = i
        self.black_hole_idx = max_idx
        
    def __init__(self, m, dataset, num_stars, num_iters):
        self.m = m #### Denotes number of cities
        self.num_stars = num_stars ### Denotes number of stars
        self.iters = num_iters ### Denotes number of iterations
        self.black_hole_idx = None ### Denotes the index of black hole
        self.list_stars = []
        self.dataset = dataset
        self.alpha = 0.6
        self.num_candidates = 0
        for i in range(self.num_stars):
            curr_soln = self.generate_random_solution()
            x = Star(curr_soln)
            self.list_stars.append(x)
        max_val = self.calculate_cost(0)
        max_idx = 0
        for i in range(self.num_stars):
            curr_val = self.calculate_cost(i)
            if curr_val<max_val:
                max_val = curr_val
                max_idx = i
        self.black_hole_idx = max_idx
        
    def calculate_diff(self, input_seq, output_seq):
        input_sequence = input_seq.copy()
        output_sequence = output_seq.copy()
        '''
        Calculates the difference between the input sequence and output sequence that creates the new subsequence.
        '''
        #### input_sequence ---> idx city
        #### output_sequence --->  idx city
        input_dict = [0]*self.m
        output_dict = [0]*self.m
        for i in range(self.m):
            ip_city = input_sequence[i]
            op_city = output_sequence[i]
            input_dict[ip_city] = i
            output_dict[op_city] = i
        diff_seq = []
        for i in range(self.m): 
            op_city = output_sequence[i]
            ip_idx = input_dict[op_city]
            ip_city = input_sequence[i]
            #### Swap ip_idx and i
            diff_seq.append((ip_idx, i))
            temp = input_sequence[ip_idx]
            input_sequence[ip_idx] = input_sequence[i]
            input_sequence[i] = temp
            input_dict[op_city] = i
            input_dict[ip_city] = ip_idx
        return diff_seq
    
    def multiply_swap_seq(self, swap_seq, scalar):
        res_swap_seq = []
        for i in range(self.m):
            if random.random()<scalar:
                res_swap_seq.append(swap_seq[i])
        return res_swap_seq
    
    def add_swap_seq(self, soln, swap_seq):
        for i in range(len(swap_seq)):
            first = swap_seq[i][0]
            second = swap_seq[i][1]
            temp = soln[first]
            soln[first] = soln[second]
            soln[second] = temp
        return soln
    
    def calculate_next_sequence(self, idx):
        curr_soln = self.list_stars[idx].current_solution
        global_soln = self.list_stars[self.black_hole_idx].current_solution
        diff1 = self.calculate_diff(curr_soln, global_soln)
        swap_seq = self.multiply_swap_seq(diff1, self.alpha)
        next_soln = self.add_swap_seq(curr_soln.copy(), swap_seq)
        return next_soln
            
    def calc_radius(self):
        totalsum = 0
        for i in range(self.num_stars):
            totalsum = totalsum + self.calculate_cost(i)
        cost_black_hole = self.calculate_cost(self.black_hole_idx)
        return cost_black_hole/totalsum
    
    def check_event_horizon(self):
        black_hole_cost = self.calculate_cost(self.black_hole_idx)
        radius = self.calc_radius()
        for i in range(self.num_stars):
            if i == self.black_hole_idx:
                continue
            curr_cost = self.calculate_cost(i)
            if abs(curr_cost - black_hole_cost)<radius:
                self.list_stars[i].current_solution = self.generate_random_solution()
            
    def solve(self):
        num_iter = 0
        while num_iter< self.iters:
            if num_iter%50 == 0:
                curr_global_cost = self.calculate_cost(self.black_hole_idx)
                print("Global Solution: ",curr_global_cost)
            for i in range(self.num_stars):
                next_sequence = self.calculate_next_sequence(i)
                self.num_candidates = self.num_candidates+1
                self.list_stars[i].current_solution = next_sequence
            self.update_black_hole()
            self.check_event_horizon()
            num_iter += 1
        global_soln = self.calculate_cost(self.black_hole_idx)
        result = self.list_stars[self.black_hole_idx].current_solution
        return result, curr_global_cost, self.num_candidates
    
def load_dataset(m):
    with open("./att"+str(m)+"_d.txt",'r') as f:
        lines = f.readlines()
    lines = np.array(lines)
    dataset = np.zeros((m,m))
    idx = 0
    for l in lines:
        l = l[:-1]
        line = l.split('      ')[1:]
        for i in range(len(line)):
            dataset[idx][i] = int(line[i])
        idx+=1
    return dataset
    
def solveBHO(m,n,iters):
    # m = 48
    # n = 100
    # iters = 10000
    dataset = load_dataset(m)
    solver = BlackHoleOptimisation(m, dataset, n, iters)
    global_soln_list, global_soln_val, num_candidates  = solver.solve()
    print("global solution list: ",global_soln_list)
    print("global solution value: ",global_soln_val)
#############################################################################
    with open("./att"+str(m)+".txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    #print(content) #one line of the doc--> num city +1, x, y

    num = []
    x_cord = []
    y_cord = []
    for line in content:
        items = line.split()
        num.append(int(items[0]) - 1)
        x_cord.append(int(items[1]))
        y_cord.append(int(items[2]))

    print("Number of stars used: {}".format(n))
    plt.figure(1, figsize=[8, 6], facecolor='#F0F0F0')
    plt.margins(0.1, 0.1)
    for i, c in enumerate(global_soln_list):  # output the cities to a plot
        plt.title("Black Hole Optimization TSP (48 cities)")
        plt.ylabel("Y Coordinates of cities")
        plt.xlabel("X Coordinates of cities")
        plt.plot(x_cord[i], y_cord[i], 'gx')
    
    for i in range(0, len(global_soln_list) - 1):  # plot connecting lines between each city visited in the order they are visited
        plt.plot([x_cord[global_soln_list[i]], x_cord[global_soln_list[i+1]]], [y_cord[global_soln_list[i]], y_cord[global_soln_list[i+1]]], 'c-',
                linewidth=2.0, alpha=0.4)
        plt.pause(0.05)

    plt.show()

    return global_soln_val, num_candidates

if __name__ == '__main__':
    solveBHO(m,n,iters)
    