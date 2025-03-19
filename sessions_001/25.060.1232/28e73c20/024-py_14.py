"""
1.  **Initialize:** Create an output grid of the same dimensions (n x n) as the input grid, filled entirely with white (color 0).

2.  **Outer Border:** Draw a green (color 3) border around the entire outer edge of the grid. This border is one pixel wide.

3.  **Inner Border:** Create a white (color 0) border one pixel wide inside the outer green border.

4.  **Calculate Cross Arm Length and Corner Size:**  Calculate the cross arm length (and corner square side length). This length is equal to `(n // 2) // 2`, where `n` is the dimension of the grid (e.g., 11, 15, or 19). This formula ensures the arm length and corner squares grow proportionally with the grid size.

5.  **Center Cross:** Draw a green (color 3) cross centered in the grid. The length of each arm of the cross, extending from the center pixel, is determined by the `arm_length` calculated in the previous step.

6.  **Corner Squares:** Draw four green (color 3) squares at the corners formed by conceptually extending the cross arms. The side length of each corner square is equal to the `arm_length`. These squares are positioned adjacent to the endpoints of the cross arms.

7.  **Center Pixel:** Set the very center pixel of the grid to green (color 3).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    n = output_grid.shape[0]

    # Outer Green Square (Step 2)
    output_grid[:, [0, n-1]] = 3
    output_grid[[0, n-1], :] = 3

    # Inner White Border (Step 3)
    output_grid[:, [1, n-2]] = 0
    output_grid[[1, n-2], :] = 0
    
    # Dynamic Arm Length Calculation (Step 4)
    arm_length = (n // 2) // 2
    corner_size = arm_length
    
    # Main Structure Creation: cross (Step 5)
    center = n // 2

    for i in range(center - arm_length, center + arm_length + 1):
        output_grid[center, i] = 3
        output_grid[i, center] = 3

    # Fill corners (Step 6)
    if corner_size > 0:
        for i in range(center - arm_length, center - arm_length + corner_size ):
          for j in range(center-arm_length, center-arm_length+corner_size):
            output_grid[i,j] = 3
            output_grid[i+2*(arm_length+1)-corner_size,j] = 3
            output_grid[i, j+2*(arm_length + 1)-corner_size] = 3
            output_grid[i+2*(arm_length + 1)-corner_size,j+2*(arm_length+1)-corner_size] = 3
        

    # center point (Step 7)
    output_grid[center, center] = 3
    
    return output_grid