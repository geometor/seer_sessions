import copy

"""
Transforms a 1D input grid (represented as a list of lists with one row) based on the length of contiguous horizontal blocks of blue pixels (1).
- White pixels (0) remain unchanged.
- Blue pixels (1) are replaced by a new color depending on the length of the contiguous block they belong to:
  - Blocks of length 1 become red (2).
  - Blocks of length 2 become maroon (9).
  - Blocks of length 3 become gray (5).
"""

def transform(input_grid):
    """
    Applies the color transformation rule based on block length.

    Args:
        input_grid: A list containing a single list of integers (representing a 1xN grid).

    Returns:
        A list containing a single list of integers representing the transformed 1xN grid.
    """
    # Ensure input is treated as a single row
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        # Handle potential malformed input, though ARC format usually guarantees list of lists
        # For this specific task based on examples, we expect a single row.
        # If input might be just a flat list, adjust accordingly.
        # Let's assume it follows the standard [[row1], [row2], ...] format, even for 1 row.
        raise ValueError("Input grid should be a list containing at least one list (row).")

    input_row = input_grid[0]
    output_row = copy.deepcopy(input_row) # Start with a copy, 0s are already correct
    n = len(input_row)
    i = 0

    # Iterate through the input row
    while i < n:
        # Check if the current pixel is blue (1)
        if input_row[i] == 1:
            # Find the length of the contiguous block of blue pixels
            block_length = 0
            j = i
            while j < n and input_row[j] == 1:
                block_length += 1
                j += 1

            # Determine the output color based on block length
            output_color = -1 # Default/error value
            if block_length == 1:
                output_color = 2 # Red
            elif block_length == 2:
                output_color = 9 # Maroon
            elif block_length == 3:
                output_color = 5 # Gray
            # Note: The examples don't cover lengths other than 1, 2, 3.
            # If other lengths are possible, the rule needs clarification.
            # Assuming only these lengths map to specific colors and others might remain unchanged or follow a different rule.
            # Based strictly on examples, we only handle 1, 2, 3.

            # Apply the output color to the block in the output row
            if output_color != -1:
                for k in range(i, i + block_length):
                    output_row[k] = output_color

            # Advance the index past the processed block
            i += block_length
        else:
            # If the pixel is not blue (it must be white based on examples),
            # keep the original value (already copied) and move to the next pixel.
            i += 1

    # Return the transformed row wrapped in a list
    return [output_row]
