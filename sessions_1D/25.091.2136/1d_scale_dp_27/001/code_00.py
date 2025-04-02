import copy

"""
Identifies an initial contiguous block of non-white color starting from the left of a 1D row.
Finds the first azure (8) pixel to the right of this block.
Fills any white (0) pixels located between the initial block and the azure pixel with the color of the initial block.
Leaves the initial block, the azure pixel, and any pixels to its right unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid (list[list[int]]): A 1xN grid represented as a list containing one list of integers.

    Returns:
        list[list[int]]: The transformed 1xN grid.
    """

    # As the grid is 1D (1xN), operate on the first row
    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy
    row_length = len(input_row)

    fill_color = -1
    initial_block_end_index = -1
    azure_marker_index = -1

    # 1. Identify the initial contiguous block and its color
    if row_length > 0 and output_row[0] != 0:
        fill_color = output_row[0]
        for i in range(row_length):
            if output_row[i] == fill_color:
                initial_block_end_index = i
            else:
                # Found the end of the initial block
                break
    else:
        # Handle edge case: empty row or row starts with white (unexpected based on examples)
        # For now, assume valid input as per examples. If the block doesn't exist,
        # we won't find a fill_color, and subsequent steps won't modify anything.
        pass

    # 2. Find the index of the first azure (8) pixel after the initial block
    if initial_block_end_index != -1:
        for i in range(initial_block_end_index + 1, row_length):
            if output_row[i] == 8:
                azure_marker_index = i
                break

    # 3. & 4. Fill white pixels between the block and the marker
    # Ensure both the block and marker were found
    if fill_color != -1 and azure_marker_index != -1:
        # Iterate from the pixel *after* the initial block up to (but not including) the azure marker
        for i in range(initial_block_end_index + 1, azure_marker_index):
            # If the pixel is white (0), change its color
            if output_row[i] == 0:
                output_row[i] = fill_color

    # 5. Other pixels (initial block, azure marker, pixels to the right) are already correct
    #    as we started with a copy of the input row.

    # 6. Return the result in the 2D grid format
    return [output_row]