"""
The transformation rule involves creating a core by doubling the input grid and then creating a frame around this core by reflecting the edges of the original input grid.

1. Create Core: Double the input grid horizontally. Double the result vertically.
2. Create Horizontal Frame Edges: Mirror the top and bottom edges of the input horizontally.
3. Create Vertical Frame Edges: Mirror the left and right edges of the input vertically.
4. Assemble Output: Combine the core and frame sections. The horizontal frame edges are placed above and below the core, and the vertical frame edges are placed to the left and right of the core.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Create Core: Double the input horizontally, then double vertically
    h_doubled = np.concatenate((input_grid, input_grid[:, ::-1]), axis=1)
    core = np.concatenate((h_doubled, h_doubled[::-1, :]), axis=0)

    # 2. Create Horizontal Frame Edges: Mirror top and bottom edges horizontally
    top_edge = input_grid[0, :]
    bottom_edge = input_grid[-1, :]
    top_frame = np.concatenate((top_edge, top_edge[::-1]), axis=0)
    bottom_frame = np.concatenate((bottom_edge, bottom_edge[::-1]), axis=0)

    # 3. Create Vertical Frame Edges: Mirror left and right edges vertically
    left_edge = input_grid[:, 0]
    right_edge = input_grid[:, -1]
    left_frame = np.concatenate((left_edge, left_edge[::-1]), axis=0).reshape(-1, 1)  # Reshape for vertical concatenation
    right_frame = np.concatenate((right_edge, right_edge[::-1]), axis=0).reshape(-1, 1) # Reshape for vertical concatenation

    # 4. Assemble Output
    # Create an empty output grid
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Place the core
    output_grid[rows//2:rows//2 + rows*2 - (rows%2)*2 , cols//2:cols//2 + cols*2 - (cols%2)*2] = core

    # Place the horizontal frame edges

    output_grid[0:1,:] = top_frame
    output_grid[-1:,:] = bottom_frame

    # Place the vertical frame edges

    output_grid[:,0:1] = left_frame
    output_grid[:,-1:] = right_frame
    

    return output_grid.tolist()