```python
import numpy as np
from typing import Optional, Tuple

"""
Transforms a 1D NumPy array of single-digit integers. The transformation hinges on 
the location of the integer 2. If 2 is present, the algorithm scans left and right 
from the position of 2 for the *first* non-zero integer encountered. All zero elements 
situated strictly *between* the 2 and the found non-zero element are replaced with 
the value of that non-zero element, but only if the non-zero element is not 
immediately adjacent to the 2. If 2 is not present, or if no non-zero element 
exists to the left/right, or if the nearest non-zero element is immediately 
adjacent to 2, no filling occurs on that side.
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
        end_index: The ending index for the scan (exclusive for step=1, inclusive for step=-1). 
                   Note: range needs careful handling for numpy.
        step: The step direction (-1 for left, 1 for right).

    Returns:
        A tuple (value, index) of the first non-zero element found, or None.
    """
    if step == 1:
        # Scan right: start_index to end_index (exclusive)
        indices = np.arange(start_index, end_index)
    elif step == -1:
        # Scan left: start_index down to end_index (inclusive)
        # We want to check indices from start_index down to 0 if end_index is -1
        actual_end = end_index # should be -1 for full left scan
        indices = np.arange(start_index, actual_end, step) 
    else:
        return None # Should not happen

    for i in indices:
        # Check bounds explicitly for safety, although range should handle it
        if 0 <= i < len(data): 
            if data[i] != 0:
                return data[i], i
    return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation based on the position of '2'.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    n = len(output_grid)

    # 1. Find the index of the number 2
    index_of_2 = _find_first_occurrence_np(input_grid, 2)

    # 2. If 2 is not present, return the original sequence unchanged
    if index_of_2 is None:
        return output_grid

    # 3. Left Fill Scan & Fill
    # Scan leftwards from the index immediately preceding 2 down to index 0
    left_scan_result = _scan_and_find_non_zero_np(input_grid, index_of_2 - 1, -1, -1)
    if left_scan_result is not None:
        left_fill_value, left_fill_index = left_scan_result
        # Check if the found non-zero is not adjacent to 2
        if left_fill_index < index_of_2 - 1:
            # Replace elements from non-zero index + 1 up to (but not including) 2's index
            # Only replace if the element is currently 0 (redundant check if logic correct, but safe)
            fill_slice = output_grid[left_fill_index + 1 : index_of_2]
            fill_slice[fill_slice == 0] = left_fill_value # Apply fill only to zeros in the slice


    # 4. Right Fill Scan & Fill
    # Scan rightwards from the index immediately following 2 up to the end
    right_scan_result = _scan_and_find_non_zero_np(input_grid, index_of_2 + 1, n, 1)
    if right_scan_result is not None:
        right_fill_value, right_fill_index = right_scan_result
        # Check if the found non-zero is not adjacent to 2
        if right_fill_index > index_of_2 + 1:
            # Replace elements from 2's index + 1 up to (but not including) non-zero index
            # Only replace if the element is currently 0
            fill_slice = output_grid[index_of_2 + 1 : right_fill_index]
            fill_slice[fill_slice == 0] = right_fill_value # Apply fill only to zeros in the slice


    # 5. Return the modified output grid
    return output_grid
```