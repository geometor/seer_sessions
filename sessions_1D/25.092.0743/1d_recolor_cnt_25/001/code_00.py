"""
Transforms a 1D grid by changing the color of contiguous horizontal runs of yellow (4) pixels based on their length.
- Runs of length 1 become azure (8).
- Runs of length 2 become red (2).
- Runs of length 3 become magenta (6).
White (0) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a color transformation to runs of yellow pixels based on run length.

    Args:
        input_grid (list): A 1D list representing the input grid row.

    Returns:
        list: A 1D list representing the transformed output grid row.
    """
    # Ensure input is treated as a NumPy array for easier slicing if needed, though list operations are sufficient here.
    # Work with a copy to avoid modifying the original input during iteration
    output_grid = list(input_grid)
    n = len(input_grid)
    i = 0

    # Define the mapping from run length to output color
    length_to_color = {
        1: 8,  # azure
        2: 2,  # red
        3: 6   # magenta
    }
    target_color = 4 # yellow

    # Iterate through the grid
    while i < n:
        # Check if the current pixel is the target color (yellow)
        if input_grid[i] == target_color:
            # Find the end of the contiguous run of the target color
            j = i
            while j < n and input_grid[j] == target_color:
                j += 1

            # Calculate the length of the run
            run_length = j - i

            # Determine the replacement color based on the run length
            # Use get with a default to handle unexpected run lengths (though not present in examples)
            # If a run length isn't in the map, it keeps its original color (yellow)
            replacement_color = length_to_color.get(run_length, target_color)

            # Apply the transformation to the output grid for the entire run
            for k in range(i, j):
                output_grid[k] = replacement_color

            # Move the index past the processed run
            i = j
        else:
            # If not the target color, just move to the next pixel
            i += 1

    return output_grid
