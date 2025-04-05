import numpy as np

"""
Transforms a 1D NumPy array by finding the unique non-zero integer value, 
locating its first and last occurrences, and filling the segment of the array 
between these occurrences (inclusive) with that non-zero value. Assumes the 
input array contains exactly two identical non-zero values and zeros elsewhere.
"""

def find_non_zero_value_and_indices(input_grid):
    """
    Finds the unique non-zero value and the indices of its occurrences.

    Args:
        input_grid (np.ndarray): The input 1D NumPy array.

    Returns:
        tuple: (non_zero_value, indices_array) or (None, None) if constraints are not met.
               indices_array is a 1D NumPy array of indices where non_zero_value is found.
    """
    # Find unique non-zero values
    unique_values = np.unique(input_grid)
    non_zero_values = unique_values[unique_values != 0]

    # Check if exactly one unique non-zero value exists
    if len(non_zero_values) != 1:
        # This case should not happen based on the problem description,
        # but returning None signals an issue.
        # print(f"Warning: Expected 1 unique non-zero value, found {len(non_zero_values)}")
        return None, None
    
    non_zero_val = non_zero_values[0]

    # Find indices of the non-zero value
    indices = np.where(input_grid == non_zero_val)[0]

    # Check if exactly two occurrences are found (as per problem description)
    if len(indices) != 2:
         # Handle edge cases like train_6 where indices might be adjacent
         # The logic works even if indices aren't exactly 2, but the problem implies it.
         # Let's allow cases with >= 2 indices and use min/max, covering the base case.
         # Revisit if stricter adherence to "exactly two" is needed.
         if len(indices) < 2:
            # print(f"Warning: Expected 2 occurrences of {non_zero_val}, found {len(indices)}")
            # If only one found, maybe it fills itself? But examples suggest two are needed.
            # Returning None indicates inability to process according to the main rule.
            return None, None # Cannot form a segment with less than 2 points implicitly

    return non_zero_val, indices


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation to the input NumPy array.

    Args:
        input_grid (np.ndarray): A 1D NumPy array containing integers,
                                 with exactly two identical non-zero values.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    # Find the non-zero value and its indices
    non_zero_val, indices = find_non_zero_value_and_indices(input_grid)

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Proceed only if a valid non-zero value and its indices were found
    if non_zero_val is not None and indices is not None and len(indices) >= 2:
        # Determine the start and end indices of the segment to fill
        start_index = np.min(indices)
        end_index = np.max(indices) # Use max to ensure correct order

        # Fill the segment from start_index to end_index (inclusive)
        # NumPy slice assignment handles this efficiently
        output_grid[start_index : end_index + 1] = non_zero_val
    # Else: if constraints weren't met (e.g., no non-zero, <2 occurrences),
    # return the unchanged copy of the input grid.

    return output_grid