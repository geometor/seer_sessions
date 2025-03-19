"""
The transformation rule is as follows:
1. Identify the background: Gray (5) pixels form the background and remain unchanged.
2. Identify Objects: Connected components of white (0) pixels are identified as objects.
3. Selective Color Change: White (0) pixels that are part of 2x2, 2x1, or 1x2 regions of connected white pixels are changed to red (2).
4. Preservation of Gray: Gray (5) pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the orthogonally adjacent neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_part_of_small_region(grid, row, col, visited):
    """
    Checks if a white pixel is part of a 2x2, 1x2, or 2x1 region of white pixels
    """
    if (row, col) in visited or grid[row, col] != 0:
        return False

    visited.add((row,col))
    neighbors = get_neighbors(grid,row,col)
    white_neighbors = [(r,c) for r,c in neighbors if grid[r,c] == 0]
    
    #check for 2x2.  
    for nr, nc in white_neighbors:
        neighbors2 = get_neighbors(grid, nr, nc)
        white_neighbors2 = [(r,c) for r,c in neighbors2 if grid[r,c] == 0]
        
        count = 0
        for nr2, nc2 in white_neighbors2:
             if (nr2, nc2) == (row,col):
                continue
             neighbors3 = get_neighbors(grid, nr2, nc2)
             if (nr, nc) in neighbors3:
                count+=1
        if count > 0:
            return True
    

    if len(white_neighbors) > 1:
        return True
    
    return False


def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    visited = set()

    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 0:  # If white
                if is_part_of_small_region(output_grid, row, col, visited):
                    output_grid[row,col] = 2

    return output_grid