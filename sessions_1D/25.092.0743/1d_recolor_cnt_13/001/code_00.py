import numpy as np

"""
Recolors contiguous horizontal blocks of green pixels (3) based on their length.
- Blocks of length 1 become blue (1).
- Blocks of length 2 become red (2).
- Blocks of length 3 become gray (5).
Other pixels remain unchanged (white, 0).
"""

def transform(input_grid):
    """
    Transforms the input grid by recoloring horizontal green blocks based on length.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    # This preserves dimensions and background pixels.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define the color mapping based on block length.
    color_map = {
        1: 1,  # length 1 -> blue
        2: 2,  # length 2 -> red
        3: 5   # length 3 -> gray
    }

    # Iterate through each row of the grid.
    # Although examples are 1D, this handles potential 2D cases.
    for r in range(rows):
        current_block_start = -1
        current_block_length = 0

        # Iterate through each column in the current row.
        for c in range(cols):
            # Check if the current pixel is green (3).
            if input_grid[r, c] == 3:
                # If this is the start of a new green block, record its start index.
                if current_block_length == 0:
                    current_block_start = c
                # Increment the length of the current green block.
                current_block_length += 1
            else:
                # If the current pixel is not green, check if we just finished a green block.
                if current_block_length > 0:
                    # Determine the new color based on the block length using the map.
                    # Use .get() with a default (e.g., 0 or the original color) if unexpected lengths occur.
                    new_color = color_map.get(current_block_length)
                    # If a valid mapping exists for the length, recolor the block in the output grid.
                    if new_color is not None:
                        output_grid[r, current_block_start : current_block_start + current_block_length] = new_color
                    # Reset the block tracking variables.
                    current_block_start = -1
                    current_block_length = 0

        # After iterating through all columns, handle the case where a green block ends at the last column.
        if current_block_length > 0:
            new_color = color_map.get(current_block_length)
            if new_color is not None:
                output_grid[r, current_block_start : current_block_start + current_block_length] = new_color

    # Return the modified output grid.
    return output_grid