```python
import numpy as np
from typing import Optional, Tuple

"""
Transforms a 1D NumPy array of single-digit integers. The transformation hinges on 
the location of the integer 2. If 2 is present, the algorithm scans left and right 
from the position of 2 for the *first* non-zero integer encountered. All zero elements 
situated strictly *between* the 2 and the found non-zero element are replaced with 
the value of that non-zero element, but only if the non-zero element is not 
immediately adjacent to the 2 (i.e., there is at least one zero between them). 
If 2 is not present, or if no non-zero element exists to the left/right, or if the 
nearest non-zero element is immediately adjacent to 2, no filling occurs on that side.
"""

def _find_first_occurrence_np(data: np.ndarray, value: int) -> Optional[int]:
    """Finds the index of the first occurrence of a value in a NumPy array."""
    indices = np.where(data == value)[0]
    if indices.size > 0:
        return indices[0]
    else:
        return None

def _scan_and_find_non_zero_np(data: np.ndarray, start_index: int, end_index: int, step: int) -> Optional[Tuple[int, int]]:
    """
    Scans a portion of the NumPy array for the first non-zero element.

    Args:
        data: The NumPy array to scan.
        start_index: The starting index for the scan (inclusive).
        end_index: The ending index boundary (exclusive for step=1, lower bound for step=-1).
        step: The step direction (-1 for left, 1 for right).

    Returns:
        A tuple (value, index) of the first non-zero element found, or None.
    """
    # Define the range of indices to check based on the direction (step)
    if step == 1:
        # Scan right: from start_index up to (but not including) end_index
        indices = np.arange(start_index, end_index)
    elif step == -1:
        # Scan left: from start_index down to 0 (inclusive if end_index is -1 or less)
        # Correctly handle the inclusive nature of the lower bound for negative step
        actual_end = max(-1, end_index) # Ensure the stop point is at least -1 for arange
        indices = np.arange(start_index, actual_end, step)
    else:
        # Invalid step value
        return None

    # Iterate through the generated indices
    for i in indices:
        # Basic bounds check (although arange should handle most cases)
        if 0 <= i < len(data): 
            if data[i] != 0:
                # Found the first non-zero element
                return data[i], i
    # No non-zero element found in the specified range
    return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation based on the position of '2'.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Initialize output_grid as a copy of input_grid to avoid modifying the original
    output_grid = np.copy(input_grid)
    n = len(output_grid)

    # 1. Locate the marker element '2'
    index_of_2 = _find_first_occurrence_np(input_grid, 2)

    # 2. If '2' is not found, return the original grid unchanged
    if index_of_2 is None:
        return output_grid

    # 3. Perform Left Scan and Fill
    # Scan leftwards from the index immediately preceding '2' down to index 0
    left_scan_result = _scan_and_find_non_zero_np(input_grid, index_of_2 - 1, -1, -1)
    
    # Check if a non-zero element was found to the left
    if left_scan_result is not None:
        left_fill_value, left_fill_index = left_scan_result
        
        # Condition: Fill only if the found element is NOT adjacent to '2'
        if left_fill_index < index_of_2 - 1:
            # Identify the slice of elements strictly between the found non-zero and '2'
            # Note: Slicing is [start:end], end is exclusive.
            start_fill = left_fill_index + 1
            end_fill = index_of_2
            
            # Check if the slice is valid (start < end)
            if start_fill < end_fill:
                 # Create a boolean mask for zeros within the target slice
                mask = output_grid[start_fill:end_fill] == 0
                # Apply the fill value where the mask is True
                output_grid[start_fill:end_fill][mask] = left_fill_value


    # 4. Perform Right Scan and Fill
    # Scan rightwards from the index immediately following '2' up to the end of the array
    right_scan_result = _scan_and_find_non_zero_np(input_grid, index_of_2 + 1, n, 1)

    # Check if a non-zero element was found to the right
    if right_scan_result is not None:
        right_fill_value, right_fill_index = right_scan_result

        # Condition: Fill only if the found element is NOT adjacent to '2'
        if right_fill_index > index_of_2 + 1:
            # Identify the slice of elements strictly between '2' and the found non-zero
            start_fill = index_of_2 + 1
            end_fill = right_fill_index # Slicing end is exclusive, which is correct here

            # Check if the slice is valid (start < end)
            if start_fill < end_fill:
                # Create a boolean mask for zeros within the target slice
                mask = output_grid[start_fill:end_fill] == 0
                # Apply the fill value where the mask is True
                output_grid[start_fill:end_fill][mask] = right_fill_value

    # 5. Return the modified grid
    return output_grid
```