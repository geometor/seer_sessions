```python
import math

"""
Transformation Rule:
1. Identify the contiguous block of identical non-zero integers in the input sequence.
2. Determine the value, length, and starting index of this block.
3. Calculate the shift distance, which is equal to the length of the block.
4. Calculate the new starting index for the block in the output sequence by adding the shift distance to the original starting index.
5. Construct the output sequence by creating a sequence of 12 zeros and placing the original block at the calculated new starting position.
"""

def find_block(grid):
    """
    Finds the contiguous block of identical non-zero numbers in the grid.

    Args:
        grid: A list of integers.

    Returns:
        A tuple containing:
        - value: The non-zero value of the block (int). Returns None if no block found.
        - start_index: The starting index of the block (int). Returns None if no block found.
        - length: The length of the block (int). Returns 0 if no block found.
    """
    start_index = -1
    value = None
    length = 0

    for i, num in enumerate(grid):
        if num != 0 and start_index == -1: # Start of a potential block
            start_index = i
            value = num
            length = 1
        elif num == value and start_index != -1: # Continuing the block
            length += 1
        elif num != value and start_index != -1: # End of the block
            break # Stop searching once the block is found and ends

    if start_index == -1: # No block found
        return None, None, 0

    return value, start_index, length

def transform(input_grid):
    """
    Shifts a contiguous block of non-zero numbers to the right by its own length.

    Args:
        input_grid: A list of 12 integers containing a single contiguous block
                    of identical non-zero numbers surrounded by zeros.

    Returns:
        A list of 12 integers representing the transformed grid.
    """
    # Find the non-zero block in the input grid
    block_value, start_index, block_length = find_block(input_grid)

    # If no block is found (shouldn't happen based on examples, but good practice)
    if block_value is None:
        return list(input_grid) # Return the original grid or an empty one? Examples imply always a block.

    # Calculate the shift distance (equal to the block length)
    shift_distance = block_length

    # Calculate the new starting index for the block
    new_start_index = start_index + shift_distance

    # Initialize the output grid with zeros
    output_grid = [0] * len(input_grid) # Assuming length is always 12 based on examples

    # Place the block in the output grid at the new position
    # Ensure the block doesn't go out of bounds (although examples suggest it won't)
    for i in range(block_length):
        output_index = new_start_index + i
        if 0 <= output_index < len(output_grid):
            output_grid[output_index] = block_value

    return output_grid
```