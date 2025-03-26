"""
Creates a 3x3 output grid. The placement of three gray (5) pixels within this grid
is determined by the frequency distribution of colors in the 3x3 input grid.

1. If the input grid is monochrome (contains only one color, frequency 9), the
   output grid's top row is set to gray (5).
2. If multiple colors share the highest frequency in the input grid, the
   output grid's anti-diagonal ([0,2], [1,1], [2,0]) is set to gray (5).
3. If a single color has the highest frequency, but the grid is not monochrome
   (frequency < 9), the output grid's main diagonal ([0,0], [1,1], [2,2]) is
   set to gray (5).
All other cells in the output grid remain white (0).
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms a 3x3 input grid based on color frequency analysis.

    Args:
        input_grid: A list of lists representing the 3x3 input grid.

    Returns:
        A list of lists representing the transformed 3x3 output grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Ensure input is 3x3 as per examples (though the logic might generalize)
    if rows != 3 or cols != 3:
        # Handle unexpected input size if necessary, for now assume 3x3
        print("Warning: Expected 3x3 input, received {}x{}".format(rows, cols))
        # Return a default or raise an error? Let's stick to the observed pattern.
        # If it's not 3x3, the diagonal/row logic might be ambiguous.
        # For now, let's proceed assuming 3x3 based on examples.
        pass

    # Initialize the 3x3 output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Flatten the input grid to easily count color occurrences
    flat_input = input_array.flatten()

    # Count the frequency of each color
    color_counts = Counter(flat_input)

    # Find the maximum frequency
    if not color_counts: # Handle empty input case if needed
         return output_grid.tolist()
    max_freq = max(color_counts.values())

    # Find all colors that have the maximum frequency
    majority_colors = [color for color, count in color_counts.items() if count == max_freq]

    # Apply the transformation rules based on frequency analysis
    if len(majority_colors) == 1:
        # Case 1: Single majority color
        if max_freq == 9:
            # Subcase 1a: Input is monochrome (entire grid is the majority color)
            # Set the top row to gray (5)
            output_grid[0, :] = 5
        else:
            # Subcase 1b: Single majority color, but not monochrome (max_freq < 9)
            # Set the main diagonal to gray (5)
            np.fill_diagonal(output_grid, 5)
            # Alternative implementation for main diagonal:
            # output_grid[0, 0] = 5
            # output_grid[1, 1] = 5
            # output_grid[2, 2] = 5
    else:
        # Case 2: Multiple colors tie for the maximum frequency
        # Set the anti-diagonal to gray (5)
        output_grid[0, 2] = 5
        output_grid[1, 1] = 5
        output_grid[2, 0] = 5

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
