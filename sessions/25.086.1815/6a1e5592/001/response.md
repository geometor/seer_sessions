```python
"""
Transforms the input grid based on the following rules:
1. Creates an output grid of the same dimensions as the input grid.
2. Iterates through each pixel of the input grid.
3. If the input pixel is red (2), the corresponding output pixel is set to red (2).
4. If the input pixel is gray (5), the corresponding output pixel is set to white (0).
5. If the input pixel is white (0):
    a. Examines its 8 neighbors (horizontal, vertical, diagonal) in the input grid.
    b. If any neighbor is red (2), the corresponding output pixel is set to blue (1).
    c. Otherwise (no red neighbors), the corresponding output pixel remains white (0).
"""

import numpy as np

def _has_red_neighbor(grid, r, c, height, width):
    """
    Checks if the cell at (r, c) in the grid has any red (2) neighbors.
    Handles boundary conditions.
    """
    # Define the 8 possible neighbor offsets
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    for dr, dc in neighbor_offsets:
        nr, nc = r + dr, c + dc
        # Check if the neighbor is within grid boundaries
        if 0 <= nr < height and 0 <= nc < width:
            # Check if the neighbor's color is red (2)
            if grid[nr, nc] == 2:
                return True
    # No red neighbors found
    return False

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions, potentially copying input
    # or creating a new one filled with zeros. Let's create a copy first.
    output_grid = np.copy(input_np) # Start with a copy

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            input_color = input_np[r, c]

            # Rule 3: If input is red (2), output remains red (2) - already handled by copy
            # No explicit action needed if output_grid is a copy of input_np for color 2.
            # if input_color == 2:
            #    output_grid[r, c] = 2 # Redundant if copied

            # Rule 4: If input is gray (5), output becomes white (0)
            if input_color == 5:
                output_grid[r, c] = 0

            # Rule 5: If input is white (0), check neighbors
            elif input_color == 0:
                # Check for red neighbors in the *input* grid
                if _has_red_neighbor(input_np, r, c, height, width):
                    # Rule 5b: Change to blue (1) if red neighbor exists
                    output_grid[r, c] = 1
                else:
                    # Rule 5c: Remain white (0) if no red neighbors
                    output_grid[r, c] = 0
            # else: color is already handled (e.g. red from the copy)

    return output_grid.tolist() # Return as list of lists if required by framework
```