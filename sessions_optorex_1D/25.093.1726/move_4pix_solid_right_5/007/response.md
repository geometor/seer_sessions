```python
"""
Transforms a 1D sequence of 12 integers by identifying the unique contiguous 
block of identical non-zero digits and shifting this block 4 positions to the 
right. The rest of the sequence is filled with zeros.
"""

import numpy as np

def find_contiguous_block(data: np.ndarray):
    """
    Finds the unique contiguous block of identical non-zero digits in a 1D NumPy array.

    Args:
        data: The input 1D NumPy array of integers.

    Returns:
        A tuple containing (start_index, length, value) of the block.
        Returns (-1, 0, 0) if no such block is found or the array is empty.
        start_index is -1 if no block was found.
    """
    start_index = -1
    length = 0
    value = 0
    n = data.size
    if n == 0:
        return -1, 0, 0

    # Iterate through the array to find the start of the block
    for i in range(n):
        # Check if the current element is non-zero and we haven't started a block yet
        # Use item() for robust scalar comparison
        current_val = data[i].item() if isinstance(data[i], np.generic) else data[i]
        
        if current_val != 0 and start_index == -1:
            start_index = i
            value = current_val
            length = 1
            # Look ahead from the next element to find the end of the block
            for j in range(i + 1, n):
                next_val = data[j].item() if isinstance(data[j], np.generic) else data[j]
                if next_val == value:
                    length += 1
                else:
                    # Block ended before the end of the array
                    return start_index, length, value
            # If the inner loop completed, the block extends to the end of the array
            return start_index, length, value

    # If the loop completes without finding any non-zero element
    return -1, 0, 0


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid: A 1D NumPy array of 12 integers.

    Returns:
        A new 1D NumPy array with the block shifted 4 positions right.
    """
    # Ensure input is treated as a 1D array
    if input_grid.ndim > 1:
         # Assuming input format is consistent with examples (e.g., shape (1, 12))
         # Flatten it to 1D for processing
         input_grid = input_grid.flatten()
    
    grid_length = input_grid.shape[0]
    
    # Initialize output_grid with zeros, matching input size and data type
    output_grid = np.zeros_like(input_grid)

    # Find the contiguous block in the input grid
    start_index, length, value = find_contiguous_block(input_grid)

    # Proceed only if a valid block was found (start_index is not -1)
    if start_index != -1:
        # Calculate the new starting index for the block by adding 4
        new_start_index = start_index + 4

        # Define the end index for slicing/filling in the output grid
        # Ensure the end index does not exceed the grid length
        new_end_index = min(new_start_index + length, grid_length)
        
        # Place the block into the output grid at the new position
        # Ensure the start index is within bounds before slicing/filling
        if new_start_index < grid_length:
             # Fill the segment in the output grid with the block's value
             # Only fill indices that are valid (>= new_start_index and < new_end_index)
             output_grid[new_start_index:new_end_index] = value

    # Return the modified output grid
    return output_grid
```