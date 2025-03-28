```python
"""
Create a copy of the input grid. Identify all azure (8) pixels. For every pair of azure pixels, if they share the same row, draw a horizontal azure line connecting them. If they share the same column, draw a vertical azure line connecting them. Return the modified grid.
"""

import numpy as np
from itertools import combinations

def transform(input_grid):
    """
    Draws horizontal and vertical lines connecting pairs of azure (8) pixels 
    that share the same row or column, respectively.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid with connecting lines.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify
    output_grid = grid.copy()
    
    # Find the coordinates of all azure (8) pixels
    azure_pixels = np.argwhere(grid == 8)
    
    # Iterate through all unique pairs of azure pixel coordinates
    # Use combinations to avoid redundant pairs and self-pairs
    for p1_coords, p2_coords in combinations(azure_pixels, 2):
        r1, c1 = p1_coords
        r2, c2 = p2_coords

        # Check if the pixels are in the same row
        if r1 == r2:
            # Determine the start and end columns for the horizontal line
            min_col = min(c1, c2)
            max_col = max(c1, c2)
            # Draw the horizontal line in the output grid
            output_grid[r1, min_col:max_col+1] = 8
            
        # Check if the pixels are in the same column
        elif c1 == c2:
            # Determine the start and end rows for the vertical line
            min_row = min(r1, r2)
            max_row = max(r1, r2)
            # Draw the vertical line in the output grid
            output_grid[min_row:max_row+1, c1] = 8

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()

```