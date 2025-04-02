```python
"""
Transforms the input grid by identifying the 'core' structure of the azure (8) object.

The transformation first identifies all azure (8) pixels in the input grid.
It then applies a filter based on the local neighborhood of each azure pixel.
Specifically, an azure pixel is kept (retains its color 8) in the output grid
if it has at least 3 neighbors (including diagonals, i.e., 8-way connectivity)
that are also azure in the input grid.
All other pixels in the input grid (non-azure pixels, and azure pixels that
do not meet the neighbor threshold) are set to white (0) in the output grid.

Note: While this rule attempts to capture the "core" extraction observed in
the examples, testing indicates it does not perfectly replicate the output for
all provided training cases. It serves as an approximation of the observed
pattern of removing "thin" parts of the azure shape.
"""

import numpy as np

def get_neighbors(r, c, height, width):
    """
    Generates coordinates of 8-way adjacent neighbors for a given cell (r, c)
    within the grid boundaries (height, width).
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def count_azure_neighbors(grid, r, c):
    """
    Counts the number of azure (8) neighbors for a cell (r, c) in the grid,
    using 8-way adjacency.
    """
    height, width = grid.shape
    count = 0
    # Iterate through all 8 potential neighbors
    for nr, nc in get_neighbors(r, c, height, width):
        # If neighbor is azure, increment count
        if grid[nr, nc] == 8:
            count += 1
    return count

def transform(input_grid):
    """
    Filters the input grid to keep only 'core' azure pixels.

    An azure pixel is considered part of the 'core' if it has 3 or more
    azure neighbors (8-way adjacency).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid containing
                  the 'core' azure pixels against a white background.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Define the target color and neighbor threshold
    azure_color = 8
    neighbor_threshold = 3

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is azure
            if input_grid[r, c] == azure_color:
                # Count its azure neighbors
                num_neighbors = count_azure_neighbors(input_grid, r, c)
                # If the neighbor count meets the threshold, keep the pixel
                if num_neighbors >= neighbor_threshold:
                    output_grid[r, c] = azure_color
            # Otherwise, the output grid pixel remains white (0) as initialized

    # Return the resulting output grid
    return output_grid
```