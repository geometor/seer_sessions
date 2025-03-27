"""
The transformation rule involves changing the color of certain blue (1) pixels to orange (7) in the input grid. 
The blue pixels that are changed are those that are adjacent to, or on the 'border' of white (0) pixels, forming an outline.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the 8-connected neighbors of a pixel in the grid.

    Args:
      grid: The 2D numpy array representing the grid.
      row: The row index of the pixel.
      col: The column index of the pixel.

    Returns:
      A list of (row, col) tuples representing the neighbors.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 1:
                neighbors = get_neighbors(output_grid, row, col)
                for n_row, n_col in neighbors:
                    if output_grid[n_row, n_col] == 0:
                        
                        neighbor_of_neighbor = get_neighbors(output_grid, n_row, n_col)
                        
                        count_one = 0
                        for nn_row, nn_col in neighbor_of_neighbor:
                            if output_grid[nn_row,nn_col] == 1:
                                count_one +=1
                        
                        if count_one > 0:
                            output_grid[row, col] = 7
                            break  # only change once per blue pixel

    return output_grid