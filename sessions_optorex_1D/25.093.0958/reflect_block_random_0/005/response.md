```python
import numpy as np

"""
Reverses the sub-sequence of elements located between the first and last non-zero elements (inclusive) in the input NumPy array, while preserving the position of any leading or trailing zeros. If there are zero or one non-zero elements, the array remains unchanged.
"""

def _find_non_zero_indices(arr: np.ndarray) -> np.ndarray:
    """Finds the indices of all non-zero elements."""
    # np.nonzero returns a tuple of arrays, one for each dimension.
    # For a 1D array, we take the first element of the tuple.
    return np.nonzero(arr)[0]

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array according to the described rule.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """

    # 1. Identify the indices of all non-zero digits.
    non_zero_indices = _find_non_zero_indices(input_array)

    # 2. Check the number of non-zero digits found.
    # If there are fewer than two non-zero digits, return the original array.
    if len(non_zero_indices) < 2:
        return input_array

    # 3. Determine the start and end indices of the sub-sequence to reverse.
    # This corresponds to the first and last non-zero element positions.
    start_index = non_zero_indices.min()
    end_index = non_zero_indices.max()

    # 4. Extract three segments from the input array:
    # The leading_part: elements before start_index.
    leading_part = input_array[:start_index]
    # The middle_part: elements from start_index to end_index (inclusive).
    middle_part = input_array[start_index : end_index + 1]
    # The trailing_part: elements after end_index.
    trailing_part = input_array[end_index + 1:]

    # 5. Reverse the order of the elements within the middle_part.
    # Slicing with [::-1] creates a reversed copy.
    reversed_middle_part = middle_part[::-1]

    # 6. Construct the final output array by concatenating the parts.
    # Ensure all parts are NumPy arrays for concatenation.
    output_array = np.concatenate((leading_part, reversed_middle_part, trailing_part))

    # 7. Return the constructed output array.
    return output_array

```