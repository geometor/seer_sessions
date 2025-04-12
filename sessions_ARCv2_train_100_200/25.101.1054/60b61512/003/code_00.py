"""
Transforms the input grid by changing specific white (0) pixels to orange (7)
based on the configuration of adjacent yellow (4) pixels.
The primary rule identified is: if a white pixel is part of a 2x2 block
in the input grid that contains exactly three yellow pixels, that white pixel
is changed to orange in the output.
Other conditions might exist to explain all changes in the training examples,
but this 2x2 rule covers the most consistent pattern. All other pixels,
including the original yellow pixels, retain their color.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

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

    # Define the key colors
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

            # Condition 1: Check if the count is exactly 3
            if target_count == 3:
                # Find the location(s) of the non-target_color pixel(s) within the 2x2 block.
                # We are specifically interested if one of them is the background color.
                non_target_indices = np.where(block != target_color)

                # Ensure there is exactly one non-target pixel (which implies the 3 target pixels)
                if len(non_target_indices[0]) == 1:
                    # Get the relative row and column index within the 2x2 block
                    rel_r, rel_c = non_target_indices[0][0], non_target_indices[1][0]

                    # Check if this non-target pixel is actually the background color
                    if block[rel_r, rel_c] == background_color:
                        # Calculate the absolute row and column index in the full grid
                        abs_r, abs_c = r + rel_r, c + rel_c
                        # Change the corresponding pixel in the output grid to the fill_color (orange)
                        output_np[abs_r, abs_c] = fill_color

    # Note: The analysis indicated that the 2x2 rule above does not cover all
    # transformations seen in the training examples (e.g., input1[6,5], input1[6,7],
    # input2[3,0], input2[3,1]). A more complex rule or additional conditions
    # might be needed for a perfect match, but those conditions were not clearly
    # generalizable from the examples provided. This implementation only includes
    # the identified 2x2 rule.

    # Convert the final NumPy array back to a list of lists for the return value
    output_grid = output_np.tolist()
    return output_grid
