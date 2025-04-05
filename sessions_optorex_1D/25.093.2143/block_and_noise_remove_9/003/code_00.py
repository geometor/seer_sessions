import numpy as np
import math # Not strictly needed for this logic, but available
# No other specific libraries seem required based on the task description

"""
Transformation Rule:
Accepts a 1D sequence (list or NumPy array) of integers. 
Identifies non-zero integers that do not have an adjacent neighbor (left or right) 
with the same value. Changes these "isolated" non-zero integers to 0. 
Leaves all other integers (zeros and non-zero integers with at least one identical neighbor) 
unchanged. Returns the modified sequence, likely as a NumPy array.
"""

def _is_isolated(arr: np.ndarray, index: int, size: int) -> bool:
    """
    Checks if the non-zero element at the given index in the array is isolated.
    An element is isolated if it's non-zero and neither its left nor right 
    neighbor (if they exist) has the same value.

    Args:
        arr: The input NumPy array.
        index: The index of the element to check.
        size: The total number of elements in the array.

    Returns:
        True if the element is non-zero and isolated, False otherwise.
    """
    current_value = arr[index]

    # Zeros are never isolated by this definition
    if current_value == 0:
        return False

    # Check left neighbor
    has_same_left = False
    if index > 0: # Check if a left neighbor exists
        if arr[index - 1] == current_value:
            has_same_left = True
            
    # Check right neighbor
    has_same_right = False
    if index < size - 1: # Check if a right neighbor exists
        if arr[index + 1] == current_value:
            has_same_right = True

    # An element is isolated if it's non-zero and has no identical neighbors
    return not has_same_left and not has_same_right


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid (assumed 1D NumPy array).
    Changes isolated non-zero digits to 0.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with isolated non-zero digits changed to 0.
    """
    # Ensure input is a NumPy array (it should be based on previous errors)
    if not isinstance(input_grid, np.ndarray):
        # Attempt conversion if it's list-like, though the environment likely provides ndarray
        try:
            input_grid = np.array(input_grid)
        except Exception as e:
            raise TypeError(f"Input grid must be a NumPy array or convertible. Error: {e}")

    # Handle potential multi-dimensional arrays by trying to flatten if simple 1D sequence expected
    # Based on examples, it looks 1D. If it might be (1, N) or (N, 1), flatten it.
    if input_grid.ndim > 1:
        if input_grid.shape[0] == 1 or input_grid.shape[1] == 1:
             original_shape = input_grid.shape # Store original shape if needed later, though output seems 1D
             input_grid = input_grid.flatten()
        else:
             # If it's truly multi-dimensional beyond a simple row/column vector,
             # the 'adjacency' definition might need refinement. Sticking to 1D interpretation for now.
             raise ValueError(f"Input grid has unexpected dimensions {input_grid.shape}. Expected 1D or flattenable to 1D.")

    # Get the size (length) of the 1D array
    n = input_grid.size 
    
    # Initialize output_grid as a copy of the input to modify
    output_grid = np.copy(input_grid) 

    # Iterate through the input grid elements
    for i in range(n):
        # Check if the element at index i is isolated using the helper function
        if _is_isolated(input_grid, i, n):
            # If it is isolated, change the corresponding element in the output grid to 0
            output_grid[i] = 0

    # Return the modified grid
    # If input was (1, N) or (N, 1), reshape back if required, but examples show 1D output string
    # Assuming 1D output is desired based on example format.
    return output_grid