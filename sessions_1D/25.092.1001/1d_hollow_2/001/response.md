```python
import numpy as np

"""
Transformation Rule:
Find the single contiguous block of non-white pixels in the input array.
Determine the start and end indices of this block.
If such a block exists and its length is greater than 2:
  Create the output array as a copy of the input array.
  Iterate from the index immediately after the start index up to (but not including) the end index.
  Set the color of each pixel in this range to white (0) in the output array.
If the block length is 1 or 2, the output is identical to the input (as there are no internal pixels to change).
If no non-white block exists, the output is identical to the input.
"""

def transform(input_grid):
    """
    Transforms the input grid by hollowing out the interior of a single
    contiguous non-white block, keeping only its boundary pixels.
    If the block length is less than 3, or no block exists, returns the input unchanged.

    Args:
        input_grid (np.array): A 1D numpy array representing the input grid row.

    Returns:
        np.array: The transformed 1D numpy array.
    """
    # Ensure input is a numpy array (it usually is in ARC)
    input_array = np.array(input_grid).flatten() # Work with a 1D array

    # Initialize output_grid as a copy of the input
    output_grid = input_array.copy()

    # Find indices of all non-white (non-zero) pixels
    non_white_indices = np.where(input_array != 0)[0]

    # Check if any non-white pixels were found
    if non_white_indices.size == 0:
        # No non-white pixels, return the original grid
        return output_grid

    # Find the start and end indices of the block
    # Since we assume a single contiguous block, these are the min and max indices
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)

    # Check if the block has internal pixels (length > 2)
    if end_index > start_index + 1:
        # Change the pixels between the start and end indices (exclusive) to white (0)
        output_grid[start_index + 1 : end_index] = 0
    # If length is 1 or 2 (end_index <= start_index + 1), no changes needed beyond the initial copy

    # Return the modified output grid
    # Reshape back to 1xN if the original input was technically 2D (1 row)
    if len(input_grid.shape) == 2 and input_grid.shape[0] == 1:
        return output_grid.reshape(1, -1)
    else: # Assuming it was 1D or needs to be returned as 1D
        return output_grid
```