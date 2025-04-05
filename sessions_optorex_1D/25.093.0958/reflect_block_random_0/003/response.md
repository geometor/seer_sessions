```python
"""
Reverses the sub-sequence of elements located between the first and last non-zero elements (inclusive) in the input NumPy array, while preserving the position of any leading or trailing zeros. If there are zero or one non-zero elements, the array remains unchanged.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array according to the described rule.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """

    # 1. Find the indices of all non-zero elements.
    # np.nonzero returns a tuple of arrays, one for each dimension.
    # For a 1D array, we take the first element of the tuple.
    non_zero_indices = np.nonzero(input_array)[0]

    # 2. Check if there are fewer than two non-zero elements.
    if len(non_zero_indices) < 2:
        # If 0 or 1 non-zero elements, return the original array.
        return input_array

    # 3. Determine the start and end indices of the sub-sequence to reverse.
    start_index = non_zero_indices.min()
    end_index = non_zero_indices.max()

    # 4. Extract the parts of the array: leading, middle (to be reversed), trailing.
    leading_part = input_array[:start_index]
    middle_part = input_array[start_index : end_index + 1]
    trailing_part = input_array[end_index + 1:]

    # 5. Reverse the middle part.
    # Slicing with [::-1] creates a reversed copy.
    reversed_middle_part = middle_part[::-1]

    # 6. Concatenate the parts to form the output array.
    # Ensure all parts are NumPy arrays for concatenation.
    output_array = np.concatenate((leading_part, reversed_middle_part, trailing_part))

    # 7. Return the constructed output array.
    return output_array
```