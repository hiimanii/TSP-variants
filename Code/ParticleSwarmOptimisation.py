import random
import numpy as np
import matplotlib.pyplot as plt
##### Get data from dataset

class Particle:
    def __init__(self, initial_solution, initial_swap_seq):
        self.current_solution = initial_solution
        self.curr_swap_seq = initial_swap_seq
        self.local_best_solution = self.current_solution
        
class ParticleSwarmOptimisation:
    def get_random_soln(self):
        '''
        This function will return the random solution which is used to intialise the particles. 
        '''
        ### m -> Number of cities in the dataset
        curr_seq = [i for i in range(self.m)]
        random.shuffle(curr_seq)
        self.num_candidates = self.num_candidates + 1
        return curr_seq
    
    def get_random_swap_seq(self):
        '''
        This function will generate random swap sequence. To generate a basic random swap sequence, the algorithm generates two permutation and if the elements at index i is not equal then, the tuple is not appended to the swap sequence else it is added.
        '''
        seq1 = [i for i in range(self.m)]
        seq2 = [i for i in range(self.m)]
        random.shuffle(seq1)
        random.shuffle(seq2)
        swap_seq = []
        for i in range(self.m):
            if seq1[i] != seq2[i]:
                swap_seq.append((seq1[i], seq2[i]))
        return swap_seq
    
    def __init__(self, n, m, iterations, dataset):
        ### n -> number of particles in the swarm
        ### m -> number of cities in the dataset
        self.n = n
        self.list_particles = []
        self.alpha = 0.6 ### alpha -> importance to going in global direction
        self.beta = 0.3 ### beta -> importance to going in local direction
        self.num_iters = iterations
        self.dataset = dataset  ### dataset -> distance matrix
        self.global_best = None ### global_best -> Length of the global best tour
        self.global_best_soln = None ### global_best_soln -> Cost of traversing global best tour
        self.m = m ### m -> Number of cities
        self.num_candidates = 0
        for i in range(self.n):
            soln = self.get_random_soln()
            swap_seq = self.get_random_swap_seq()
            x = Particle(soln, swap_seq)
            self.list_particles.append(x)
#             print("particle num: ",i)
#             print("soln: ",soln)
#             print("cost: ",self.calculate_cost(soln))
            self.update_local_soln(i)
            self.update_global_soln(i)
    
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
    
    def combine_seq(self, seq1, seq2):
        '''
        This function combines the two sequences given in the input.
        '''
        new_seq = seq1.copy()
        for i in range(len(seq2)):
            new_seq.append(seq2[i])
        return new_seq
    
    def calculate_next_velocity(self, i):
        '''
        This function calculates the next velocity for the particle at index i.
        '''
        curr_particle = self.list_particles[i]
        curr_swap_seq = curr_particle.curr_swap_seq.copy()
        next_swap_seq = self.calculate_diff(curr_particle.current_solution.copy(), curr_particle.local_best_solution.copy())
        temp_swap_seq = []
        for i in range(len(next_swap_seq)):
            if random.random() < self.alpha:
                temp_swap_seq.append(next_swap_seq[i])
        next_swap_seq = temp_swap_seq
        curr_swap_seq = self.combine_seq(curr_swap_seq, next_swap_seq)
        next_swap_seq = self.calculate_diff(curr_particle.current_solution.copy(), self.global_best_soln.copy())
        temp_swap_seq = []
        for i in range(len(next_swap_seq)):
            if random.random() < self.beta:
                temp_swap_seq.append(next_swap_seq[i])
        next_swap_seq = temp_swap_seq
        curr_swap_seq = self.combine_seq(curr_swap_seq, next_swap_seq)
        return curr_swap_seq
    
    def calculate_next_sequence(self, idx):
        '''
        Calculates the next sequence for paricle at index idx.
        '''
        curr_particle = self.list_particles[idx]
        next_velocity = self.calculate_next_velocity(idx)
        curr_soln = curr_particle.current_solution.copy()
        for x in next_velocity:
            first = x[0]
            second = x[1]
            temp = curr_soln[first]
            curr_soln[first] = curr_soln[second]
            curr_soln[second] = temp
        return curr_soln, next_velocity
    
    def calculate_cost(self, seq):
        '''
        Calculates cost for the sequence
        '''
        cost = 0
        begin = seq[0]
        end = seq[len(seq)-1]
        for i in np.arange(1, len(seq)):
            curr = seq[i]
            prev = seq[i-1]
            cost = cost + self.dataset[curr][prev]
        cost = cost + self.dataset[begin][end]
        return cost
    
    def update_global_soln(self, idx):
        '''
        Update global solution for the dataset
        '''
        if self.global_best_soln is None:
#             print("@@@@@@@@@@")
            self.global_best_soln = self.list_particles[idx].current_solution
            self.global_best = self.calculate_current_cost(idx)
            return
        curr_global_val = self.calculate_global_best_cost()
        curr_val = self.calculate_current_cost(idx)
        if curr_global_val > curr_val:
#             print("curr_val: ",curr_val, " curr_global_val: ",curr_global_val)
#             print("global_best_soln: ",self.global_best_soln)
            self.global_best_soln = self.list_particles[idx].current_solution
            self.global_best = curr_val
#             print("**** best soln now: ",self.global_best)
        
    def update_local_soln(self, i):
        '''
        Update local solution for particle at index i
        '''
        curr_val = self.calculate_current_cost(i)
        local_best_val = self.calculate_local_best_cost(i)
        if local_best_val > curr_val:
            self.list_particles[i].local_best_solution = self.list_particles[i].current_solution
            
    def calculate_current_cost(self, i):
        '''
        Calculate cost for the sequence for particle at position i
        '''
        return self.calculate_cost(self.list_particles[i].current_solution)
    
    
    def calculate_global_best_cost(self):
        '''
        Calculate local best cost for the sequence for particle at position i
        '''
        return self.calculate_cost(self.global_best_soln)
    
    def calculate_local_best_cost(self, i):
        '''
        Calculate local best cost for the sequence for particle at position i
        '''
        return self.calculate_cost(self.list_particles[i].local_best_solution)
    
    
    def solve(self):
        # n-> number of particles
        num_iter = 0
        while(num_iter<self.num_iters):
            if(num_iter%50 == 0):
                print("iter: ",num_iter," curr_global_cost: ",self.calculate_global_best_cost())
#                 print("&&&&& global_best_seq: ",self.global_best_soln)
            for i in np.arange(self.n):
                curr_particle = self.list_particles[i]
#                 print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/iteration num______: ",i," global cost: ",self.calculate_cost(self.global_best_soln))
                next_sequence, next_velocity = self.calculate_next_sequence(i)
                self.num_candidates = self.num_candidates + 1
#                 print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/iteration num@@: ",i," global cost: ",self.calculate_cost(self.global_best_soln))
                ### Update the solution and swap sequence
                curr_particle.current_solution = next_sequence
                curr_particle.curr_swap_seq = next_velocity
                ### Update local best solution for the curr_particle
                self.update_local_soln(i)
                ### Update global best solution for curr_particle
#                 print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/iteration num: ",i," global cost: ",self.calculate_cost(self.global_best_soln))
#             print("global cost: ",self.calculate_cost(self.global_best_soln))
#             print("&&&&& global_best_seq: ",self.global_best_soln)
#             break
            for i in np.arange(self.n):
                self.update_global_soln(i)
            num_iter+=1
        return self.global_best_soln ,self.global_best, self.num_candidates

def load_dataset(m):
    ### m-> number of cities
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

def solveTSP(m,n,iters):
    # m = 48
    # n = 100
    # iters = 1000
    dataset = load_dataset(m)
#     dataset = np.array([[2,3,4,5,6],[3,8,9,10,11],[4,9,8,12,6],[5,10,12,2,3],[6,11,6,3,2]])
    print(dataset.shape)
    solver = ParticleSwarmOptimisation(n, m, iters, dataset)
#     for i in range(n):
#         print("For ant ",i," the local_best: ",solver.list_particles[i].local_best_solution," local_best_val: ",solver.calculate_local_best_cost(i))

    global_soln_list, global_soln_val, num_candidates  = solver.solve()
    print("global solution list: ",global_soln_list)
    print("global solution value: ",global_soln_val)

###########################################################################################

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
    # print("Shortest route found: {0:.3f}".format(aco.shortest_path_len))

    #plt.axes([0.15, 0.15, 0.8, 0.8])
    plt.figure(1, figsize=[8, 6], facecolor='#F0F0F0')
    plt.margins(0.1, 0.1)
    for i, c in enumerate(global_soln_list):  # output the cities to a plot
        plt.title("Particle Swarm Optimization TSP (48 cities)")
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
    solveTSP(m,n,iters)