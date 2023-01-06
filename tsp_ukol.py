import csv
from matplotlib import pyplot
import random
from random import randint
from math import sqrt

# The Nearest Neighbor method
def nearest_neighbor(coordinates):
    
    # Inicialization of status list and setting zero size of Hamilton circle
    s = ["N"] * (len(coordinates))
    w = 0
    
    # Set random first node and redefine it as closed
    start = randint(0,len(coordinates)-1)
    s[start] = "C"

    # Inicialization of path
    path = [start]

    # Adding nodes to Hamilton circle
    while "N" in s:

        # Inicialization of minimal distance, index of node and coordinates of last element in list 'path'
        w_min = float("inf")
        u = -1
        x1 = coordinates[path[len(path)-1]][0]
        y1 = coordinates[path[len(path)-1]][1]
        
        # Asking of each node if its not processed yet
        for i in range(len(coordinates)):
            
            # For not processed yet node calculate their coordinates and distance between this and last node 
            if s[i] == "N":
                x2 = coordinates[i][0]
                y2 = coordinates[i][1]
                w_i = sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # If is distance smaller then minimal distance replace it and also index
                if w_i < w_min:
                    w_min = w_i
                    u = i

        # Mark node as closed, add it to list of path and count minimal to overall distance
        s[u] = "C"
        path.append(u)
        w += w_min
    
    # Calculating last part of path back to the first node
    x1 = coordinates[path[u]][0]
    y1 = coordinates[path[u]][1]
    x2 = coordinates[path[0]][0]
    y2 = coordinates[path[0]][1]
    w += sqrt((x2 - x1)**2 + (y2 - y1)**2)
    path.append(path[0])
    return path, w

# The Best Insertion method
def best_insertion(coordinates):
    
    # Inicialization of list of coordinate list indexs and set zero size of Hamilton circle
    w = 0
    help_list = []
    for i in range(len(coordinates)):
        help_list.append(i)
    
    # Iniciaization of path list and set first random  node
    path = []
    path.append(randint(0,len(coordinates)-1))
    help_list.pop(path[0])
 
    # Creation of Hamilton circle of three nodes
    for i in range(3):
            x1 = coordinates[len(path)-1][0]
            y1 = coordinates[len(path)-1][1]            
            if i == 2:
                x2 = coordinates[path[0]][0]
                y2 = coordinates[path[0]][1]
                path.append(path[0])
            else:
                start = randint(0,len(help_list)-1)
                path.append(start)
                help_list.remove(start)
                x2 = coordinates[len(path)-1][0]
                y2 = coordinates[len(path)-1][1]
            w += sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
    # Adding rest of nodes to Hamilton circle 
    while len(help_list) > 0:
        
        # Inicialization of new node and minimal distance
        rand_node = random.choice(help_list)
        xn = coordinates[rand_node][0]
        yn = coordinates[rand_node][1]
        nd = -1
        w_min = float("inf")

        # Calculating coordinates and distances between new node and each two nodes in Hamilton circle
        for i in range(len(path)-1):
            x1 = coordinates[path[i]][0]
            y1 = coordinates[path[i]][1]
            x2 = coordinates[path[i+1]][0]
            y2 = coordinates[path[i+1]][1]
            w_1 = sqrt((xn - x1)**2 + (yn - y1)**2)
            w_2 = sqrt((xn - x2)**2 + (yn - y2)**2)
            w_3 = sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
            # Triangle inequality
            w_4 = w_1 + w_2 - w_3
            
            # Inicialization of new minimal distance
            if w_4 < w_min:
                w_min = w_4
                nd = i + 1
        
        # Adding node to Hamilton circle and couting overall distance
        w += w_min
        path.insert(nd,rand_node)
        help_list.remove(rand_node)

    return path, w
                
            
# The method of visualization
def visualization(coordinates, path):

    # Visualization of path
    x = []
    y = []
    for i in path:
        x.append(coordinates[i][0])
        y.append(coordinates[i][1])

    # Visualization of nodes
    x_nodes = []
    y_nodes = []
    for c in coordinates:
        x_nodes.append(c[0])
        y_nodes.append(c[1])

    # Final visualization
    pyplot.scatter(x_nodes, y_nodes, c = "blue")
    pyplot.plot(x, y, c = "red")
    pyplot.show()


# Inicialization of input 
coordinates = []
vstup = 0
print("Vyberte data:")
print("Stiskněte '1' pro výběr obcí Česka s počtem obyvatel nad 6000.")
print("Stiskněte '2' pro výběr obcí Karlovarského kraje s počtem obyvatel nad 100.")
vstup = int(input())

# Choosing input dataset
if int(vstup) == 1:
    data = 'Obce_cr_nad_6000.csv'
else:
    data = 'Obce_vary_nad_100.csv'

# Opening and reading input dataset
with open (data, encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")    
    for row in reader:
        if row[1] == "SX":
            continue
        coordinates.append([float(row[1]),float(row[2])])

# Choosing method
print("Kterou metodu chcete použít?")
print("Stiskněte '1' pro metodu Nearest neighbor.")
print("Stiskněte '2' pro metodu The best insertion.")
vstup = int(input())

# Applying method and output
if vstup == 1:
    path, w = nearest_neighbor(coordinates)
else:
    path, w = best_insertion(coordinates)
wkm = w/1000 
print("Délka Hamiltonova kruhu je "f"{wkm:.4f}""km.")
visualization(coordinates,path)  
