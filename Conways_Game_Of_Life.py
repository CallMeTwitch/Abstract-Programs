# #########################
# Conway's Game of Life is 
# a famous algorithm that 
# is known for being 
# unpredictable. For each 
# block if it is "on" and 
# is adjacent to 2-3 other 
# "on" blocks, it stays 
# "on", or if it's "off" 
# and is adjacent to to 
# blocks that are "on" 
# it turns on. Otherwise 
# it stays off.
# 
# Code written for 
# entertainment.
# #########################

from matplotlib import pyplot as plt
from scipy.signal import convolve2d
import matplotlib as mpl
import random  as r
import numpy as np

# Get dimensions of grid and initialize randomly (2% chance of starting on)
w, h = int(input('Width: ')), int(input('Height: '))
grid = np.array([[r.choice(([0] * 49) + [1]) for _ in range(w)] for _ in range(h)])

# Next Iteration
def next_epoch(grid):
    new = np.array([[0 for _ in range(len(grid[0]))] for _ in range(len(grid))])
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    conv = convolve2d(grid, kernel, mode = 'same')
    for q in range(len(grid)):
        for w in range(len(grid[q])):
            if (grid[q][w] == 1 and conv[q][w] in (2, 3)) or grid[q][w] == 0 and conv[q][w] == 2:
                new[q][w] = 1
    return new

cmap = mpl.colors.ListedColormap(['k', 'w'])

plt.ion()
# Iterate Epochs
for q in range(int(input('Epochs: '))):
    grid = next_epoch(grid)
    plt.imshow(grid, cmap = cmap)
    plt.show()
    plt.pause(0.01)
    plt.clf()