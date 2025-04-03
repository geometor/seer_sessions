"""
Transforms a 1xN input grid based on the properties of contiguous green blocks.
Specifically, it identifies contiguous horizontal blocks of green (3) pixels
in the single row of the input grid. It calculates the length of each block.
If a block's length is even, the corresponding pixels in the output grid are
changed to blue (1). If a block's length is odd, the pixels are changed to
gray (5). White (0) pixels remain unchanged. The output grid retains the 1xN
format.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the length parity of contiguous green blocks.

    Args:
        input_grid (list): A list containing a single list (the row) of integers.
                           Example: [[0, 3, 3, 0, 3, 0]]

    Returns:
        list: A list containing the single transformed row, in the same format.
              Example: [[0, 1, 1, 0, 5, 0]]
    """

    # Ensure input is in the expected format (list of lists)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Handle potential malformed input, though ARC standard ensures this format
        # For robustness, could raise an error or return input
        print("Warning: Input grid format unexpected.")
        return input_grid # Or raise ValueError("Input must be a list of lists.")

    # Extract the single row from the input grid
    input_row = input_grid[0]
    n = len(input_row)

    # Initialize the output row as a copy of the input row
    output_row = list(input_row) # Use list() to ensure it's a mutable copy

    # Define colors
    GREEN = 3
    BLUE = 1
    GRAY = 5
    WHITE = 0 # Not strictly needed for logic but good for clarity

    # Iterate through the input row to find and process green blocks
    i = 0
    while i < n:
        # Check if the current pixel is green
        if output_row[i] == GREEN:
            # Found the start of a potential green block
            start_index = i

            # Find the end of the contiguous block of green pixels
            j = i
            while j < n and output_row[j] == GREEN:
                j += 1
            end_index = j - 1 # Inclusive end index of the block

            # Calculate the length of the block
            length = end_index - start_index + 1

            # Determine the replacement color based on length parity
            if length % 2 == 0:  # Even length
                replacement_color = BLUE
            else:  # Odd length
                replacement_color = GRAY

            # Apply the replacement color to the block in the output row
            for k in range(start_index, end_index + 1):
                output_row[k] = replacement_color

            # Move the main index past the processed block
            i = j # Start next iteration from the pixel after the block
        else:
            # If the pixel is not green, just move to the next one
            i += 1

    # Wrap the transformed row back into a list to match the required output format
    output_grid = [output_row]

    return output_grid