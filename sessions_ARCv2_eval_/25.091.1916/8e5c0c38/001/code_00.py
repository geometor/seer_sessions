"""
Transforms an input grid by identifying the background color and then iterating 
through each non-background pixel. If a non-background pixel has exactly 3 
neighbors (including diagonals) of the same color as itself, that pixel's color 
is changed to the background color in the output grid. Otherwise, the pixel's 
color remains unchanged.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """
    Identifies the most frequent color in the grid, considering it the background.
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        int: The color value considered as the background.
    """
    colors, counts = np.unique(grid, return_counts=True)
    background_color = colors[np.argmax(counts)]
    return background_color

def count_same_color_neighbors(grid, r, c, color):
    """
    Counts the 8 neighbors (orthogonal and diagonal) of a cell (r, c) 
    that have the specified color.

    Args:
        grid (np.array): The grid to check within.
        r (int): The row index of the cell.
        c (int): The column index of the cell.
        color (int): The color to match in the neighbors.

    Returns:
        int: The count of neighbors with the specified color.
    """
    height, width = grid.shape
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr, nc] == color:
                    count += 1
    return count

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Step 1: Identify the background color
    background_color = get_background_color(input_np)

    # Step 3 & 4: Iterate through each cell
    for r in range(height):
        for c in range(width):
            current_color = input_np[r, c]
            
            # Step 4: Check if the cell is NOT the background color
            if current_color != background_color:
                # Step 4.1: Count same-colored neighbors
                neighbor_count = count_same_color_neighbors(input_np, r, c, current_color)
                
                # Step 4.2: Condition and Action
                if neighbor_count == 3:
                    output_np[r, c] = background_color
            # Step 6: If it's background or neighbor count is not 3, 
            # the output_np already holds the correct value from the copy.

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    # Step 5 & 7: Return the modified grid
    return output_grid