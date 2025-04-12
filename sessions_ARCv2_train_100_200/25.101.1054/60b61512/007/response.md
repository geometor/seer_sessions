```python
"""
The primary transformation rule identifies 2x2 blocks within the input grid.
If a 2x2 block consists of exactly three yellow (4) pixels and one white (0) pixel,
the white pixel's location in the output grid is changed to orange (7).
All other pixels retain their original color from the input grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the 2x2 pattern fill transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)
    # Get grid dimensions
    height, width = input_np.shape

    # Define key colors
    target_color = 4  # yellow
    background_color = 0 # white
    fill_color = 7     # orange

    # Iterate through each possible top-left corner (r, c) of a 2x2 block
    # We iterate up to height-2 and width-2 because a 2x2 block spans indices
    # r to r+1 and c to c+1.
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract the 2x2 block from the input grid
            block = input_np[r:r+2, c:c+2]

            # Count the number of target_color (yellow) pixels in the block
            target_count = np.count_nonzero(block == target_color)
            # Count the number of background_color (white) pixels in the block
            background_count = np.count_nonzero(block == background_color)

            # Check if the condition (3 yellow and 1 white) is met
            if target_count == 3 and background_count == 1:
                # Find the relative location(s) of the background pixel within the 2x2 block.
                # np.where returns indices where the condition is true.
                background_indices = np.where(block == background_color)

                # There should be exactly one background pixel if the counts are correct
                if len(background_indices[0]) == 1:
                    # Get the relative row and column index within the 2x2 block
                    rel_r, rel_c = background_indices[0][0], background_indices[1][0]

                    # Calculate the absolute row and column index in the full grid
                    abs_r, abs_c = r + rel_r, c + rel_c

                    # Change the corresponding pixel in the output grid to the fill_color (orange)
                    output_np[abs_r, abs_c] = fill_color

    # Convert the final NumPy array back to a list of lists for the return value
    output_grid = output_np.tolist()
    return output_grid
```