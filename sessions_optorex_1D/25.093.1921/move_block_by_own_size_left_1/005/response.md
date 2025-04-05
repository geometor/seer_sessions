```python
import numpy as np
from typing import List, Tuple, Optional, Union

"""
Applies a transformation independently to each row of an input grid (represented as a 2D NumPy array).
For each row, it finds the first contiguous block of non-zero numbers and shifts this block 
to the left by a distance equal to its length. The space left empty by the shift and any 
space to the right of the block are filled with zeros. If a row contains no non-zero numbers, 
it remains a row of zeros.
"""

def _find_non_zero_block(row: np.ndarray) -> Tuple[Optional[np.ndarray], int, int]:
    """
    Finds the first contiguous block of non-zero numbers in a 1D NumPy array (row).

    Args:
        row: The input 1D NumPy array representing a row of the grid.

    Returns:
        A tuple containing:
        - The NumPy array segment representing the block (or None if no block is found).
        - The starting index of the block within the row (or -1 if not found).
        - The ending index of the block within the row (or -1 if not found).
    """
    start_index = -1
    end_index = -1
    n = len(row)

    # Find the start index of the first non-zero element
    non_zero_indices = np.nonzero(row)[0]
    if len(non_zero_indices) == 0:
        return None, -1, -1 # No non-zero elements
        
    start_index = non_zero_indices[0]

    # Find the end index of the first contiguous block
    end_index = start_index
    for i in range(start_index + 1, n):
        if row[i] != 0:
            end_index = i
        else:
            # Found the first zero after the block started
            break

    # Extract the block
    block = row[start_index : end_index + 1]

    return block, start_index, end_index

def _process_row(row: np.ndarray) -> np.ndarray:
    """
    Applies the shift transformation to a single row.

    Args:
        row: The 1D NumPy array representing the row to process.

    Returns:
        A new 1D NumPy array representing the transformed row.
    """
    n = len(row)
    output_row = np.zeros_like(row) # Initialize output row with zeros

    # 1. Find the non-zero block, its start index, and end index
    non_zero_block, start_index, end_index = _find_non_zero_block(row)

    # If no block is found, the output_row remains all zeros, which is correct
    if non_zero_block is not None:
        # 2. Calculate block length
        block_length = len(non_zero_block) # or end_index - start_index + 1

        # 3. Calculate shift amount (equal to block length)
        shift_amount = block_length

        # 4. Calculate new start index (clamped at 0)
        new_start_index = max(0, start_index - shift_amount)
        
        # 5. Calculate the new end index (exclusive) in the output row
        new_end_index = new_start_index + block_length

        # 6. Place the block in the output row, handling potential clipping if shifted left
        # Determine how much of the block fits in the output
        effective_block_length = min(block_length, n - new_start_index)
        
        if effective_block_length > 0:
             output_row[new_start_index : new_start_index + effective_block_length] = non_zero_block[:effective_block_length]

    return output_row


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by applying the row-wise shift operation.

    Args:
        input_grid: A 2D NumPy array of integers.

    Returns:
        A 2D NumPy array of integers with the transformation applied to each row.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Handle empty input grid case
    if input_grid.size == 0:
        return input_grid.copy()
        
    # Get grid dimensions
    rows, cols = input_grid.shape

    # Initialize output_grid with zeros (or copy structure if needed)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each row of the input grid
    for r in range(rows):
        # Get the current row
        current_row = input_grid[r, :]
        
        # Process the row using the helper function
        transformed_row = _process_row(current_row)
        
        # Place the transformed row into the output grid
        output_grid[r, :] = transformed_row

    return output_grid
```