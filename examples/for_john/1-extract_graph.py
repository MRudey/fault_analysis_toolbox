# Import global packages
import numpy as np 
import networkx as nx
import cv_algorithms
import pickle

import matplotlib.pyplot as plt
plt.close("all")

    

# Import module
import sys
sys.path.append('/home/wrona/fault_analysis/code/')

from edits import *
from metrics import *
from plots import *


filename = "v5w4h60_z95_20MYR"


## LOAD IMAGE
data = np.load("./npy/" + filename + ".npy")[:,:,3]


## THRESHOLDING
value = 3e-15
threshold = np.where(data > value, 1, 0)
threshold = np.uint8(threshold)


## SKELETONIZE
skeleton = cv_algorithms.guo_hall(threshold)
skeleton[0, :] = skeleton[1, :]
skeleton[-1,:] = skeleton[-2,:]
skeleton[:, 0] = skeleton[:, 1]
skeleton[:,-1] = skeleton[:,-2]


## EXTRACT POINTS
points = np.where(skeleton != 0)


## EXTRACT GRAPH
N = len(points[0])

# Set up graph
G = nx.Graph()

# Add nodes
for n in range(N):
    G.add_node(n, pos=(points[1][n], points[0][n]))

# Add edges to graph
G = add_edges(G, N)



# Edit graph
G = count_edges(G)
G_clean = remove_small_components(G, minimum_size = 10)    
G_clean = label_components(G_clean)


#G_clean = remove_component(G,0)
#G_clean = remove_component(G,4)


# Plot graph
fig, ax = plt.subplots(1, 1, figsize=(8,10))
plt.imshow(data)
cb = plt.colorbar()
cb.ax.plot([0, 1], [value]*2, 'r')
plot_components(G_clean, box=False, ax = ax)
plt.savefig('./images/G_' + filename + '_threshold_' + str(value) + '.png', dpi=300)


# Pickle graph
pickle.dump(G_clean, open('./graphs/graph_' + filename +'.p', "wb" ))


