"""
Identifies the spatial pattern formed by non-white pixels in a 3x3 input grid and maps it to a specific output color code based on predefined patterns.

1.  Receive the 3x3 input grid.
2.  Identify all coordinates (row, column pairs) where the pixel color is not white (0). Store these coordinates as a set.
3.  Define four target sets of coordinates corresponding to the observed patterns:
    *   Pattern A: {(0,1), (1,1), (2,0)} maps to 3 (green)
    *   Pattern B: {(0,1), (1,0), (1,1), (1,2), (2,1)} maps to 6 (magenta)
    *   Pattern C: {(0,0), (0,2), (1,1), (2,0), (2,2)} maps to 2 (red)
    *   Pattern D: {(0,0), (1,0), (1,2)} maps to 1 (blue)
4.  Compare the set of non-white coordinates from the input grid with each of the four target patterns.
5.  Return a 1x1 grid containing the color code corresponding to the matched pattern.
"""

import numpy as np

def get_non_white_coords(grid):
    """Finds the coordinates of non-white pixels in the grid."""
    coords = set()
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                coords.add((r, c))
    return coords

def transform(input_grid):
    """
    Transforms the input grid based on the spatial pattern of non-white pixels.
    """
    # Define the known patterns and their corresponding output colors
    patterns = {
        frozenset([(0, 1), (1, 1), (2, 0)]): 3,  # Pattern A -> green
        frozenset([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]): 6,  # Pattern B -> magenta
        frozenset([(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]): 2,  # Pattern C -> red
        frozenset([(0, 0), (1, 0), (1, 2)]): 1,  # Pattern D -> blue
        # Added patterns from train_5 and train_7 which are identical to train_4 and train_6
        # Already covered by Pattern C and Pattern D definitions
    }

    # Get the coordinates of non-white pixels in the input grid
    non_white_coordinates = get_non_white_coords(np.array(input_grid))

    # Check if the extracted coordinates match any known pattern
    output_color = None
    for pattern_coords, color in patterns.items():
        if non_white_coordinates == pattern_coords:
            output_color = color
            break

    # Handle cases where no pattern matches (though not expected based on examples)
    if output_color is None:
        # Default or error handling - let's return white for now, though an error might be better
        # print("Warning: Input pattern does not match any known training patterns.")
        # output_color = 0
        raise ValueError("Input pattern does not match any known training patterns.")


    # Create the 1x1 output grid
    output_grid = np.array([[output_color]], dtype=int)

    return output_grid.tolist() # Return as list of lists per spec
