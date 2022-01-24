# def tsp():
def tsp(num_cities, ants_num, iter_num):

   import aco
   import matplotlib.pyplot as plt
   # num_cities = 48
   # Intialize the ACO algorithm with some parameter values
   ACO = aco
   aco = aco.ACO(num_cities, initial_pheromone=1, alpha=1, beta=3,
                  pheromone_deposit=2, evaporation_constant=0.6)
   
   with open("./att"+str(num_cities)+".txt") as f:
      content = f.readlines()
   content = [x.strip() for x in content]

   for line in content:
      items = line.split()
      num = int(items[0]) - 1
      xcorr = int(items[1])
      ycorr = int(items[2])
      aco.add_nodes(ACO.City(num, xcorr, ycorr))
   
   # # run the aco algorithm and return the shortest path
   shortest_path = aco.best_path(num_ants=ants_num, num_steps=iter_num)
   # print("shortest_path: ", shortest_path)
   # # print("zzzzz")
   print("Number of ants used: {}".format(ants_num))
   print("Shortest route found: {0:.3f}".format(aco.shortest_path_len))

   plt.figure(1, figsize=[8, 6], facecolor='#F0F0F0')
   plt.margins(0.1, 0.1)
   for i, c in enumerate(aco.cities):  # output the cities to a plot
      plt.title("Ant Colony Optimization TSP (48 cities)")
      plt.ylabel("Y Coordinates of cities")
      plt.xlabel("X Coordinates of cities")
      plt.plot(c.x, c.y, 'gx')


   for i in range(0, len(
           shortest_path) - 1):  # plot connecting lines between each city visited in the order they are visited
      plt.plot([shortest_path[i].x, shortest_path[i + 1].x], [shortest_path[i].y, shortest_path[i + 1].y], 'c-',
               linewidth=2.0, alpha=0.4)
      plt.pause(0.05)

   plt.show()

   return aco.shortest_path_len