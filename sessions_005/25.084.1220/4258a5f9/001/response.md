```python
"""
Creates an output grid based on an input grid.
1. Initialize the output grid as a copy of the input grid.
2. Find all gray (5) pixels in the input grid.
3. For each gray pixel found at location (r, c):
    a. Iterate through its 8 neighboring positions (including diagonals).
    b. For each neighbor position (nr, nc):
        i. Check if (nr, nc) is within the grid boundaries.
        ii. If within bounds, set the pixel at (nr, nc) in the output grid to blue (1).
4. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by finding gray pixels and coloring their neighbors blue.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Initialize output_grid as a copy of the input_grid
    # This ensures background and gray pixels are preserved initially
    output_grid = np.copy(input_grid)

    # Find the locations of all gray (5) pixels
    gray_locations = np.argwhere(input_grid == 5)

    # Define the 8 neighbor offsets (relative coordinates)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each found gray pixel location
    for r, c in gray_locations:
        # Iterate through the 8 neighbor offsets
        for dr, dc in neighbor_offsets:
            # Calculate the neighbor's coordinates
            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Change the neighbor pixel in the output grid to blue (1)
                output_grid[nr, nc] = 1

    # Return the final output grid
    return output_grid
```