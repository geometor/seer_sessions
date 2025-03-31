```python
import numpy as np
from itertools import combinations

"""
Identifies all 'red plus' shapes (a central red pixel with red N, S, E, W neighbors) in the input grid. 
For every pair of these shapes whose centers are aligned either horizontally or vertically, 
draws a blue line connecting the centers by changing the intervening white background pixels to blue.
"""

def find_plus_centers(grid):
    """
    Finds the coordinates of the center pixel of all 'red plus' shapes.
    A 'red plus' shape is defined as a red (2) pixel surrounded by red (2) pixels 
    directly above, below, left, and right.
    """
    centers = []
    height, width = grid.shape
    # Iterate through possible center locations (avoiding edges)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the current pixel is red
            if grid[r, c] == 2:
                # Check if all four cardinal neighbors are also red
                if (grid[r - 1, c] == 2 and
                    grid[r + 1, c] == 2 and
                    grid[r, c - 1] == 2 and
                    grid[r, c + 1] == 2):
                    centers.append((r, c))
    return centers

def transform(input_grid):
    """
    Transforms the input grid by connecting aligned 'red plus' shapes with blue lines.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with blue lines added.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    height, width = grid_np.shape

    # Find the centers of all red plus shapes
    centers = find_plus_centers(grid_np)

    # Iterate through all unique pairs of centers
    for (r1, c1), (r2, c2) in combinations(centers, 2):
        # Check for horizontal alignment
        if r1 == r2 and abs(c1 - c2) > 1:
            # Determine the start and end columns for the line
            start_c = min(c1, c2) + 1
            end_c = max(c1, c2)
            # Fill the gap with blue (1) if the pixel is currently white (0)
            for c in range(start_c, end_c):
                if output_grid[r1, c] == 0:
                    output_grid[r1, c] = 1
                    
        # Check for vertical alignment
        elif c1 == c2 and abs(r1 - r2) > 1:
            # Determine the start and end rows for the line
            start_r = min(r1, r2) + 1
            end_r = max(r1, r2)
            # Fill the gap with blue (1) if the pixel is currently white (0)
            for r in range(start_r, end_r):
                if output_grid[r, c1] == 0:
                    output_grid[r, c1] = 1

    # Convert the result back to a list of lists
    return output_grid.tolist()
```