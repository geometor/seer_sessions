```python
import numpy as np
from typing import List

"""
Transformation Rule:
1. Identify the first non-background (non-zero) pixel in the input row. This is the 'Marker Pixel'.
2. Identify the contiguous sequence of pixels immediately following the 'Marker Pixel' that share the same color, which is different from the 'Marker Pixel' color and not the background color. This is the 'Block Object'.
3. Swap the positions of the 'Marker Pixel' and the 'Block Object'. The relative order of pixels within the 'Block Object' is maintained.
4. Background pixels remain unchanged.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Swaps the first non-background pixel ('Marker') with the immediately
    following contiguous block of pixels of a different non-background color ('Block').

    Args:
        input_grid: A list containing a single list representing the input row.

    Returns:
        A list containing a single list representing the transformed row.
    """
    # Ensure input is treated as a 1D array for simplicity
    # Use numpy for easier slicing and modification
    input_row = np.array(input_grid[0], dtype=np.int8)
    output_row = input_row.copy()
    row_length = len(input_row)

    # --- Find Marker Pixel ---
    marker_index = -1
    marker_color = -1
    for i in range(row_length):
        if input_row[i] != 0:  # 0 is the background color
            marker_index = i
            marker_color = input_row[i]
            break

    # If no marker pixel is found (e.g., all background), return the original grid
    if marker_index == -1:
        return input_grid

    # --- Find Block Object ---
    block_start_index = marker_index + 1
    block_color = -1
    block_end_index = -1

    # Check if there is a pixel immediately after the marker
    if block_start_index < row_length:
        potential_block_color = input_row[block_start_index]
        # Check if the potential block start is non-background and different from marker
        if potential_block_color != 0 and potential_block_color != marker_color:
            block_color = potential_block_color
            block_end_index = block_start_index
            # Extend the block as long as the color matches
            while (block_end_index + 1 < row_length and
                   input_row[block_end_index + 1] == block_color):
                block_end_index += 1
        else:
             # Pixel after marker is background or same color, no valid block starts here
             pass
    else:
        # Marker is at the very end, no space for a block
        pass


    # If no valid block was found adjacent to the marker, return the original grid
    if block_color == -1:
        return input_grid

    # Calculate block length
    block_length = block_end_index - block_start_index + 1

    # --- Perform Swap in Output Grid ---
    # Place the block's color into the output starting at the marker's original position
    output_row[marker_index : marker_index + block_length] = block_color

    # Place the marker's color into the output immediately after the newly placed block
    output_row[marker_index + block_length] = marker_color

    # --- Return Result ---
    # Convert the numpy array back to the required list of lists format
    return [output_row.tolist()]
```