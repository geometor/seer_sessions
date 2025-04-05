```python
import numpy as np

"""
Transforms an input 1D NumPy array of digits based on the following logic:
1. Convert the input NumPy array to a Python list.
2. Check if the list contains any non-zero digits.
   - If all digits are zero, convert the original list to a space-separated string and return it.
   - Otherwise, proceed to the next step.
3. Find the index of the first non-zero digit in the list.
4. Insert the integer 0 into the list at this found index.
5. Remove the last element from the modified list to maintain the original length.
6. Convert the final list back into a space-separated string.
7. Return the resulting string.
"""

def _find_first_non_zero_index(data_list):
    """Helper function to find the index of the first non-zero element."""
    for index, value in enumerate(data_list):
        if value != 0:
            return index
    return -1 # Indicate no non-zero element found

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array sequence.

    Args:
        input_grid: A 1D NumPy array containing single digits (0-9).

    Returns:
        A string representing the transformed sequence with digits separated by spaces.
    """
    # 1. Convert the input NumPy array to a Python list.
    input_list = input_grid.tolist()

    # 2. Check if the sequence contains only zeros.
    if all(digit == 0 for digit in input_list):
        # If all digits are zero, convert the list to a space-separated string and return.
        output_str = " ".join(map(str, input_list))
        return output_str

    # 3. Find the index of the first non-zero digit.
    first_nz_idx = _find_first_non_zero_index(input_list)

    # Initialize output_list as a copy of input_list
    output_list = list(input_list)

    # Proceed only if a non-zero digit was found (ensured by step 2 check)
    if first_nz_idx != -1:
        # 4. Insert the integer 0 into the list at the found index.
        output_list.insert(first_nz_idx, 0)

        # 5. Remove the last element from the modified list to maintain original length.
        output_list.pop()
    # else case is implicitly handled as output_list remains a copy if no non-zero found,
    # though the all-zero check should prevent reaching here without a valid first_nz_idx.

    # 6. Convert the final list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    # 7. Return the resulting string.
    return output_str
```