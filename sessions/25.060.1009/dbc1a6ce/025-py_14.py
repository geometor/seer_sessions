"""
1.  **Identify Source Pixels:** Find all pixels with the color blue (1). These are the "source" pixels.
2.  **Iterative Propagation:** For each source pixel:
    *   Start at source
    *   Create a queue containing all neighboring pixels of different color
    *   while queue is not empty:
        *   change current pixel to azure
        *   Add all non-blue neighbors of current pixel to the end of the queue.
3.  **Result:** The output grid is the result of this iterative propagation, where all pixels directly or indirectly connected (orthogonally or diagonally) to a blue pixel, and not separated by another color, are turned azure.
"""

import numpy as np
from collections import deque

def get_neighbors(grid, row, col):
    """
    Returns the neighbors of a pixel, the 8 pixels surrounding it
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find source pixels (blue pixels)
    source_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                source_pixels.append((r, c))

    # Iterative Propagation for each source pixel
    for source_row, source_col in source_pixels:
        queue = deque()
        
        #initialize queue with neighbors of source
        for neighbor_row, neighbor_col in get_neighbors(input_grid, source_row, source_col):
          if output_grid[neighbor_row,neighbor_col] != 1:
            queue.append((neighbor_row,neighbor_col))

        # while queue not empty
        while queue:
            row, col = queue.popleft()

            # change pixel to azure
            if output_grid[row, col] != 1:  # Check again to avoid overwriting other sources
                output_grid[row, col] = 8

            # add neighbors of current to queue
            for neighbor_row, neighbor_col in get_neighbors(output_grid, row, col):
                if output_grid[neighbor_row, neighbor_col] != 1 and output_grid[neighbor_row, neighbor_col] != 8 :
                  queue.append((neighbor_row,neighbor_col))

    return output_grid