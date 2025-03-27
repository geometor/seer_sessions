```python
"""
This program determines the output based on the adjacency of red (2) and azure (8) pixels in the input grid.
If any red pixel is adjacent (including diagonally) to any azure pixel, the output is 0.
Otherwise, if no red pixel touches any azure pixel, the output is 8.
"""

import numpy as np

def transform(input_grid):
    """
    Checks for adjacency between red (2) and azure (8) pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        int: 0 if any red pixel is adjacent (including diagonally) to an azure pixel, 
             8 otherwise.
    """
    
    grid = np.array(input_grid)
    height, width = grid.shape

    # Define the 8 relative neighbor coordinates (including diagonals)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is red (value 2)
            if grid[r, c] == 2:
                # Check all 8 neighbors of the red cell
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor cell is azure (value 8)
                        if grid[nr, nc] == 8:
                            # Found an adjacent red and azure pixel, return 0
                            return 0

    # If the loops complete without finding any adjacent red and azure pixels, return 8
    return 8
```