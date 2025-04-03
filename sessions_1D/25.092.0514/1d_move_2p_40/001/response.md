```python
import numpy as np

def find_non_white_block(row):
    """
    Finds the first contiguous block of non-white pixels in a 1D row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A tuple (start_index, end_index, color) if a block is found,
        otherwise None. end_index is exclusive (like Python slicing).
    """
    start_index = -1
    color = -1
    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1:  # Start of a new block
                start_index = i
                color = pixel
            elif pixel != color: # Should not happen based on task description, but good practice
                 # This is the end of the block if the color changes (unexpected case)
                 return start_index, i, color
        elif start_index != -1:  # Found a white pixel after a block started
            # This is the end of the block
            return start_index, i, color

    # If the block extends to the end of the row
    if start_index != -1:
        return start_index, len(row), color

    return None # No non-white block found

def transform(input_grid):
    """
    Transforms the input grid by shifting the single contiguous block of
    non-white pixels two positions to the right.

    1. Identify the single contiguous block of non-white pixels in the input row.
    2. Note its color, length, and starting position.
    3. Calculate the new starting position by adding 2.
    4. Create a new output row of the same length, filled with white (0).
    5. Place the identified block at the new position in the output row.
    """
    # The input is expected as a list of lists (e.g., [[1, 1, 0]]),
    # extract the single row.
    input_row = input_grid[0]
    row_length = len(input_row)

    # Find the non-white block details
    block_info = find_non_white_block(input_row)

    if block_info is None:
        # If there's no block, return the input as is (or an all-white row)
        # Based on examples, there's always a block. Let's return all white.
        output_row = [0] * row_length
        return [output_row] # Return as list of lists

    start_index, end_index, color = block_info
    block_length = end_index - start_index

    # Calculate the new starting position
    new_start_index = start_index + 2

    # Initialize the output row with white pixels (0)
    output_row = [0] * row_length

    # Place the block in the new position
    # Ensure the block fits within the bounds
    new_end_index = new_start_index + block_length
    if new_end_index <= row_length:
        for i in range(block_length):
            output_row[new_start_index + i] = color
    else:
        # Handle cases where the shift would push the block out of bounds
        # Based on examples, this doesn't seem to happen, but it's good practice.
        # Option 1: Truncate the block (less likely based on ARC)
        # Option 2: Wrap around (unlikely)
        # Option 3: Assume valid shift as per examples. If it goes out,
        #           place what fits. Let's implement this.
        pixels_to_place = row_length - new_start_index
        for i in range(pixels_to_place):
             if new_start_index + i < row_length: # Double check index
                 output_row[new_start_index + i] = color


    # Return the output row wrapped in a list
    return [output_row]

```