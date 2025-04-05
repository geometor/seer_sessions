"""
Performs a right circular shift on a 1D NumPy array. The last element of the input array is moved to the first position, and all other elements are shifted one position to the right.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a right circular shift to a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array.

    Returns:
        A new 1D NumPy array with elements shifted right circularly.
    """

    # 1. Receive the input 1D NumPy array (input_grid).

    # 2. Determine the number of elements (N) in the input array.
    num_elements = input_grid.size

    # 3. If N is less than or equal to 1, return the input array unchanged.
    if num_elements <= 1:
        return input_grid # No shift needed, return the original array

    # 4. Extract the last element of the input array (at index N-1).
    # Slicing with [-1:] ensures it remains a 1D array, suitable for concatenation.
    last_element = input_grid[-1:]

    # 5. Extract the sub-array containing all elements *except* the last one (from index 0 to N-2).
    remaining_elements = input_grid[:-1]

    # 6. Construct the output array by concatenating the extracted last element
    # (now at the beginning) followed by the extracted sub-array.
    output_grid = np.concatenate((last_element, remaining_elements))

    # 7. Return the constructed output NumPy array.
    return output_grid

# Example usage (simulated from train_1)
# input_example = np.array([6, 0, 2, 6, 1, 4, 5, 8, 9, 7, 3, 4])
# output_example = transform(input_example)
# print(f"Input: {input_example}")
# print(f"Output: {output_example}")
# Expected Output: [4 6 0 2 6 1 4 5 8 9 7 3]

# Example usage (simulated from train_7)
# input_example_2 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7])
# output_example_2 = transform(input_example_2)
# print(f"Input: {input_example_2}")
# print(f"Output: {output_example_2}")
# Expected Output: [7 0 0 0 0 0 0 0 0 0 0 6]

# Example usage (single element)
# input_example_3 = np.array([5])
# output_example_3 = transform(input_example_3)
# print(f"Input: {input_example_3}")
# print(f"Output: {output_example_3}")
# Expected Output: [5]

# Example usage (empty array)
# input_example_4 = np.array([])
# output_example_4 = transform(input_example_4)
# print(f"Input: {input_example_4}")
# print(f"Output: {output_example_4}")
# Expected Output: []