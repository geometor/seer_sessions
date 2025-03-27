"""
Change a white pixel (0) to blue (1) if it is horizontally located between two pixels of the same non-white color. Otherwise, keep the original pixel color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the rule:
    A white pixel (0) becomes blue (1) if its immediate horizontal neighbors
    (left and right) are the same non-white color.
    All other pixels remain unchanged.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = input_np.copy()
    
    # Get the dimensions of the grid
    height, width = input_np.shape

    # Iterate through each pixel, excluding the border columns
    # Row indices range from 0 to height-1
    for r in range(height):
        # Column indices range from 1 to width-2 to allow checking left and right neighbors
        for c in range(1, width - 1):
            # Check if the current pixel is white (0)
            if input_np[r, c] == 0:
                # Get the colors of the left and right neighbors
                left_neighbor_color = input_np[r, c - 1]
                right_neighbor_color = input_np[r, c + 1]

                # Check if both neighbors are non-white AND have the same color
                if left_neighbor_color != 0 and left_neighbor_color == right_neighbor_color:
                    # Change the corresponding pixel in the output grid to blue (1)
                    output_grid[r, c] = 1
            # If the current pixel is not white, or the neighbor condition is not met,
            # the output_grid pixel retains its copied value from the input_grid.

    return output_grid.tolist() # Convert back to list of lists if necessary for the environment
