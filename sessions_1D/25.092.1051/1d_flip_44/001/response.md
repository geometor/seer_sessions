```python
import numpy as np

"""
Identifies a contiguous sequence of non-white pixels in a 1D input grid.
This sequence consists of a single 'head' pixel followed by a block of 'body' pixels of a different color.
The transformation swaps the position of the head pixel and the body block within the sequence's original location, leaving the surrounding white pixels unchanged.
"""

def find_non_white_sequence(grid_row):
    """
    Finds the start and end indices of the first contiguous non-white sequence.

    Args:
        grid_row (np.array): A 1D numpy array representing the grid row.

    Returns:
        tuple: (start_index, end_index) or (None, None) if no sequence is found.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel != 0 and start_index == -1:
            start_index = i
        if pixel == 0 and start_index != -1:
            end_index = i - 1
            break
    # If the sequence goes to the end of the row
    if start_index != -1 and end_index == -1:
        end_index = len(grid_row) - 1

    if start_index != -1 and end_index != -1:
        return start_index, end_index
    else:
        return None, None


def transform(input_grid):
    """
    Transforms the input grid by reversing the order of the head pixel and the
    body block within the non-white sequence.

    Args:
        input_grid (list[list[int]]): The input grid (represented as a list of lists).

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input grid to numpy array for easier manipulation
    # Since the examples are 1xN, we take the first row.
    input_row = np.array(input_grid[0])
    
    # Initialize output_grid as a copy of the input grid's row
    output_row = np.copy(input_row)

    # 1. Identify the contiguous sequence of non-white pixels
    start_index, end_index = find_non_white_sequence(input_row)

    # Check if a sequence was found
    if start_index is not None and end_index is not None:
        # 2. Identify the head and body within the sequence
        head_pixel = input_row[start_index]
        # Ensure there's actually a body (sequence length > 1)
        if start_index < end_index:
            body_block = input_row[start_index + 1 : end_index + 1]
            
            # 3. Create the new rearranged sequence
            rearranged_sequence = np.concatenate((body_block, [head_pixel]))

            # 4. Construct the output grid row by replacing the original sequence
            output_row[start_index : end_index + 1] = rearranged_sequence
        # If sequence length is 1, head is the whole sequence, no change needed.
        # But based on examples, this case doesn't occur where transformation is needed.

    # Convert the output row back to the list of lists format
    output_grid = [output_row.tolist()]

    return output_grid
```