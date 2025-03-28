"""
Transforms an input grid based on the following rule:
1. Initialize an output grid as a copy of the input grid.
2. Iterate through each pixel of the input grid.
3. If a pixel in the input grid is white (0):
    a. Check its 8 neighbors (horizontally, vertically, and diagonally).
    b. If any neighbor in the input grid is blue (1), change the corresponding pixel in the output grid to yellow (4).
    c. If no neighbors are blue, the pixel in the output grid remains white (as initialized).
4. If a pixel in the input grid is not white (e.g., blue (1) or red (2)), its color remains unchanged in the output grid (handled by the initial copy).
5. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is white (0)
            if input_grid[r, c] == 0:
                # Assume initially that no blue neighbor is found
                found_blue_neighbor = False
                # Check all 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the center pixel itself
                        if dr == 0 and dc == 0:
                            continue

                        # Calculate neighbor coordinates
                        nr, nc = r + dr, c + dc

                        # Check if neighbor coordinates are within grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor in the input grid is blue (1)
                            if input_grid[nr, nc] == 1:
                                found_blue_neighbor = True
                                break  # Stop checking neighbors once a blue one is found
                    if found_blue_neighbor:
                        break # Stop checking neighbor rows if blue found

                # If a blue neighbor was found, change the output pixel to yellow (4)
                if found_blue_neighbor:
                    output_grid[r, c] = 4
            # If the input pixel is not white, it remains unchanged in the output_grid (due to initial copy)

    return output_grid