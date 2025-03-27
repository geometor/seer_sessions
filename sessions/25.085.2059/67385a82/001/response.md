```python
"""
Iterate through each pixel of the input grid. If a pixel is green (color 3),
check its four orthogonal neighbors (up, down, left, right) within the grid boundaries.
If any of these orthogonal neighbors in the *input* grid are also green (color 3),
change the color of the current pixel to azure (color 8) in the output grid.
Otherwise (if the pixel is not green, or if it is green but has no orthogonal green neighbors),
the pixel retains its original color in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the adjacency of green pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid as a copy of the input grid
    # This handles the default case where pixels don't change
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is green (3)
            if input_grid[r, c] == 3:
                # Flag to track if a green orthogonal neighbor is found
                has_green_neighbor = False

                # Define potential orthogonal neighbor coordinates
                neighbors = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]

                # Check each orthogonal neighbor
                for nr, nc in neighbors:
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is green (3)
                        if input_grid[nr, nc] == 3:
                            has_green_neighbor = True
                            # Found a green neighbor, no need to check others
                            break

                # If at least one orthogonal neighbor was green, change the pixel in the output grid to azure (8)
                if has_green_neighbor:
                    output_grid[r, c] = 8
            
            # No explicit 'else' needed because output_grid was initialized as a copy,
            # so pixels that are not green, or green pixels without green orthogonal neighbors,
            # already have their correct original value.

    # Return the modified output grid
    return output_grid
```