"""
The transformation involves specific horizontal and vertical shifts of colored pixels, maintaining the positions of the gray diagonal and implicitly treating white as the background. The red pixels keep relative position.

1.  **Identify Objects:** Locate all pixels with colors other than white (0). These are our objects.
2.  **Gray (5) Diagonal:** The gray (5) pixels along the main diagonal remain in the same positions.
3. **Azure (8) Shift:** The azure (8) pixels shift two columns to the right.
4.  **Red (2) Shift:** The red (2) pixels shift up two rows, and two columns to the right.
5. **Blue (1) Shift:** Find the blue (1) pixel and put gray(5) in its original row and col, and place the blue (1) in gray(5)'s place.
6.  **Background:** All other cells remain white (0).
"""

import numpy as np

def find_object(grid, color):
    positions = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                positions.append((i, j))
    return positions

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)

    # gray diagonal
    for i in range(input_grid.shape[0]):
        output_grid[i,i] = input_grid[i,i] if input_grid[i, i] == 5 else 0

    # azure shift
    azure_positions = find_object(input_grid, 8)
    for pos in azure_positions:
        output_grid[pos[0], pos[1] + 2] = 8
    
    #red shift
    red_positions = find_object(input_grid, 2)
    for pos in red_positions:
      output_grid[1, pos[1]+2] = 2

    # blue(1)
    blue_positions = find_object(input_grid, 1)
    if (len(blue_positions) > 0 ):
      blue_pos = blue_positions[0]
      output_grid[blue_pos[0], blue_pos[1]] = 0 #clear position
      output_grid[blue_pos[0]-1, blue_pos[1]-1] = 1
      output_grid[blue_pos[0], blue_pos[1]] = 5

    return output_grid