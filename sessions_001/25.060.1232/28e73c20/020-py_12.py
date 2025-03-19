"""
The transformation creates a pattern of nested squares and a cross shape using green (3) on a white (0) background. The process involves:
1. Initializing a 15x15 grid with all 0s (white).
2. Creating an outer green square by changing the outermost border to 3s.
3. Making an inner white border by setting the pixels one inside the outermost border to 0.
4. Drawing a green cross centered in the grid with arms of length 3.
5. Filling the corners inside the cross with 3x3 green squares.
6. Setting the very center point to 3.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    n = output_grid.shape[0]

    # Outer Green Square (Step 2)
    output_grid[:, [0, n-1]] = 3
    output_grid[[0, n-1], :] = 3

    # Inner White Border (Step 3)
    output_grid[:, [1, n-2]] = 0
    output_grid[[1, n-2], :] = 0
    
    # Main Structure Creation: cross (Step 4)
    center = n // 2
    arm_length = 3
    for i in range(center - arm_length, center + arm_length + 1):
        output_grid[center, i] = 3
        output_grid[i, center] = 3

    # Fill corners (Step 5)
    for i in range(center - arm_length, center - arm_length + 3 ):
      for j in range(center-arm_length, center-arm_length+3):
        output_grid[i,j] = 3
        output_grid[i+2*arm_length-2,j] = 3
        output_grid[i, j+2*arm_length-2] = 3
        output_grid[i+2*arm_length-2,j+2*arm_length-2] = 3
        

    # center point (Step 6)
    output_grid[center, center] = 3
    
    return output_grid