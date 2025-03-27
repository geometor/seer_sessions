```python
"""
Transforms input grids by identifying rectangular regions of uniform color and modifying them based on their color and size.
Specifically:
1. Blue (1) regions are completely removed (filled with white/0).
2. Red (2) regions are replaced by grey (5) except the edge
3. Azure (8) regions of size greater than 2x2:
        - a. Fill the interior with green (3).
        - b. Set the bottom edge of the azure rectangles green (3).
4. Other regions remain unchanged.
"""

import numpy as np

def find_rectangles(grid):
    """
    Finds all rectangular regions of uniform color in a grid.
    Returns a list of tuples: (color, (row_start, col_start), (row_end, col_end)).
    """
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                r_start, c_start = r, c
                r_end, c_end = r, c

                # Expand right
                while c_end + 1 < cols and grid[r, c_end + 1] == color and not visited[r, c_end+1]:
                    c_end += 1

                # Expand down
                while r_end + 1 < rows and all(grid[r_end + 1, c_start:c_end + 1] == color) and not any(visited[r_end+1, c_start:c_end+1]):
                    r_end += 1
                
                # Mark visited
                visited[r_start:r_end + 1, c_start:c_end + 1] = True
                rectangles.append((color, (r_start, c_start), (r_end, c_end)))
    return rectangles

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = input_grid.copy()

    # Find all rectangular regions
    rectangles = find_rectangles(input_grid)
    
    # Iterate through each rectangle and apply transformation rules
    for color, (r_start, c_start), (r_end, c_end) in rectangles:
        # Rule 1: Remove blue (1) regions
        if color == 1:
            output_grid[r_start:r_end+1, c_start:c_end+1] = 0
        
        # Rule 2: Red (2) regions to gray (5) inside
        elif color == 2:
            output_grid[r_start:r_end+1, c_start:c_end+1] = 2 #reset
            if r_end - r_start + 1 > 2 and c_end - c_start + 1 > 2:
              output_grid[r_start+1:r_end, c_start+1:c_end] = 5

        # Rule 3: Modify azure (8) regions based on size
        elif color == 8:
            output_grid[r_start:r_end+1, c_start:c_end+1] = 8 #reset
            if r_end - r_start + 1 > 2 and c_end - c_start + 1 > 2:
                # Fill interior with green (3)
                output_grid[r_start+1:r_end, c_start+1:c_end] = 3
                # Set bottom edge to green (3)
                output_grid[r_end, c_start:c_end+1] = 3

    return output_grid
```