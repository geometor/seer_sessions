import numpy as np
import math # math and numpy are available

"""
Transformation Rule:
1.  Receive the input sequence as a NumPy array of integers. Record its original length (number of elements), N.
2.  Convert the input NumPy array into a Python list of integers.
3.  Iterate through the list from the beginning (index 0) to find the index of the first integer that is not equal to 0. Let this index be `insertion_index`. If no non-zero integer is found, set `insertion_index` to 0.
4.  Create a new list by inserting the integer 0 into the list (from step 2) at the `insertion_index`.
5.  Take the first N elements from the list created in step 4.
6.  Convert this final list of N integers into a single string where each integer is separated by a space. This string is the output.
"""

def find_first_non_zero_index(digit_list):
    """
    Finds the index of the first non-zero digit in a list or 1D numpy array.
    Returns 0 if all digits are zero or the list/array is empty.
    """
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    # If no non-zero digit is found, default to index 0
    return 0

def transform(input_grid: np.ndarray) -> str:
    """
    Transforms the input numpy array of digits by inserting a '0'
    at the index of the first non-zero digit and truncating the result to the
    original length, returning a space-separated string.
    """
    # 1. Record original length (number of elements)
    original_length = len(input_grid)

    # Handle empty input case
    if original_length == 0:
        return ""

    # 2. Convert the input NumPy array into a Python list of integers.
    # (Conversion needed because numpy arrays don't have an insert method like lists)
    input_list = input_grid.tolist()

    # 3. Find the index of the first non-zero digit.
    insertion_index = find_first_non_zero_index(input_list)

    # 4. Create a new list by inserting 0 at the insertion_index.
    # Make a copy first if you need to preserve the original list for other operations
    # modified_list = input_list[:] # Use slicing for copying if needed
    # modified_list.insert(insertion_index, 0)
    # Or directly modify if the original list isn't needed afterwards:
    modified_list = input_list # Reassigning name, list is mutable
    modified_list.insert(insertion_index, 0)


    # 5. Take the first N elements from the modified list (truncate).
    output_list = modified_list[:original_length]

    # 6. Convert the final list of integers back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str