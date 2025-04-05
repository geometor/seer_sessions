import numpy as np
import collections

"""
Transforms a 1D NumPy array of integers by identifying the contiguous subsequence 
of non-zero integers, finding the most frequent integer (mode) within that 
subsequence, and replacing all integers in that subsequence with the mode. 
Leading and trailing zeros are preserved.
"""

def _find_non_zero_boundaries(arr: np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the start and end indices of the contiguous non-zero block.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) inclusive, or (None, None) if 
        no non-zero elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(arr != 0)[0]
    
    # Handle case where there are no non-zero elements
    if non_zero_indices.size == 0:
        return None, None
        
    # The start index is the minimum non-zero index
    start_index = np.min(non_zero_indices)
    # The end index is the maximum non-zero index
    end_index = np.max(non_zero_indices)
    
    return start_index, end_index

def _calculate_mode(arr_slice: np.ndarray) -> int | None:
    """
    Calculates the mode (most frequent element) of a NumPy array slice.
    If there are ties, returns the element that appears first among the modes 
    as per collections.Counter behavior.
    If the slice is empty, returns None.

    Args:
        arr_slice: A 1D NumPy array slice.

    Returns:
        The most frequent integer or None if the slice is empty.
    """
    # Handle empty slice case
    if arr_slice.size == 0:
        return None
        
    # Count occurrences of each element
    counts = collections.Counter(arr_slice)
    
    # Find the element with the highest count
    # most_common(1) returns a list like [(element, count)]
    mode, _ = counts.most_common(1)[0] 
    
    return mode

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied.
    """
    
    # Find the boundaries of the contiguous non-zero subsequence
    start_index, end_index = _find_non_zero_boundaries(input_grid)
    
    # If no non-zero elements exist, return a copy of the original grid
    if start_index is None:
        return input_grid.copy()
        
    # Extract the non-zero subsequence (inclusive slicing)
    non_zero_subsequence = input_grid[start_index : end_index + 1]
    
    # Calculate the mode of the non-zero subsequence
    # Note: _find_non_zero_boundaries ensures the subsequence is not empty if start_index is not None
    mode = _calculate_mode(non_zero_subsequence)
    
    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()
    
    # Replace the elements within the non-zero subsequence boundaries with the mode
    output_grid[start_index : end_index + 1] = mode
    
    return output_grid