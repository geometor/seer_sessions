```python
"""
Transforms an input NumPy array of integers by identifying the segment 
containing all non-zero elements (from the first non-zero to the last 
non-zero) and shifting this segment 4 positions to the left within an 
array of the same shape, padding the remaining positions with zeros.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the segment-shifting transformation to the input NumPy array.

    Args:
        input_grid: The 1D input NumPy array of integers.

    Returns:
        A new 1D NumPy array of integers representing the transformed sequence.
    """
    # Define the fixed amount to shift the segment
    shift_amount = 4
    
    # Find the indices of all non-zero elements
    # np.nonzero returns a tuple of arrays, one for each dimension. 
    # Since it's a 1D array, we take the first element of the tuple.
    non_zero_indices = np.nonzero(input_grid)[0]

    # Initialize the output grid with zeros, having the same shape as the input
    output_grid = np.zeros_like(input_grid)

    # Check if there are any non-zero elements
    if non_zero_indices.size == 0:
        # If no non-zeros, the output is already correct (all zeros)
        return output_grid

    # Determine the index of the first non-zero element
    first_nz_idx = non_zero_indices[0]
    # Determine the index of the last non-zero element
    last_nz_idx = non_zero_indices[-1]

    # Extract the active segment from the input grid.
    # The slice includes the element at last_nz_idx.
    segment = input_grid[first_nz_idx : last_nz_idx + 1]
    segment_length = len(segment)

    # Calculate the target starting index for the segment in the output grid.
    # This is done by shifting the original start index to the left.
    target_start_idx = first_nz_idx - shift_amount

    # Calculate the target end index (exclusive) for slicing in the output grid.
    target_end_idx = target_start_idx + segment_length

    # Place the extracted segment into the output grid using array slicing.
    # Ensure the target start index is within the valid bounds (>= 0).
    if target_start_idx >= 0:
        # NumPy slicing handles assignment correctly. If target_end_idx exceeds
        # the array length, it will assign up to the boundary.
        # However, based on examples, the full segment always fits.
         output_grid[target_start_idx:target_end_idx] = segment
    # else:
        # If target_start_idx were negative, the segment starts partially or
        # fully off the left edge. In this specific problem, the shifted part
        # effectively disappears, and the part starting from index 0 would be placed.
        # The current check `target_start_idx >= 0` implicitly handles the case
        # where the entire segment shifts off-screen (output remains zeros).
        # If it shifted partially off, more complex slicing logic might be needed,
        # but that's not required by the observed examples.

    # Return the newly constructed output grid
    return output_grid
```