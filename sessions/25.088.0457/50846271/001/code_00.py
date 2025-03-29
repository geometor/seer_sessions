"""
The transformation identifies white (0) pixels in the input grid that are adjacent (horizontally, vertically, or diagonally) to at least one red (2) pixel. 
These identified white pixels are changed to azure (8) in the output grid. 
All other pixels, including the red (2) pixels, gray (5) pixels, and white (0) pixels not adjacent to red (2) pixels, remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Changes white pixels adjacent to red pixels to azure.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if input_grid[r, c] == 0:
                # Assume no red neighbor initially
                found_red_neighbor = False
                # Examine its eight neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the input grid is red (2)
                        if input_grid[nr, nc] == 2:
                            found_red_neighbor = True
                            break  # Found a red neighbor, no need to check others
                
                # If a red neighbor was found, change the pixel in the output grid to azure (8)
                if found_red_neighbor:
                    output_grid[r, c] = 8

    # Return the modified output grid
    return output_grid