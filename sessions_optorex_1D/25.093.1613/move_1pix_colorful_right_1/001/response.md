```python
import math
import numpy as np
import re

"""
Transformation Rule:
1.  Receive the input sequence of digits (as a string). Record its original length (number of digits).
2.  Convert the input string into a list of integers.
3.  Find the index of the first digit in the list that is not equal to 0.
    - If no non-zero digit is found (i.e., all digits are 0), use index 0 as the insertion point.
4.  Create a new list by inserting the integer 0 into the list at the found index.
5.  Take the first N elements from the modified list, where N is the original length recorded in step 1.
6.  Convert this final list of integers back into a space-separated string. This is the output.
"""

def find_first_non_zero_index(digit_list):
    """
    Finds the index of the first non-zero digit in a list of integers.
    Returns 0 if all digits are zero or the list is empty.
    """
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    # If no non-zero digit is found, default to index 0
    return 0

def transform(input_str: str) -> str:
    """
    Transforms the input string of space-separated digits by inserting a '0'
    at the index of the first non-zero digit and truncating the result to the
    original length.
    """
    # 1. Parse the input string and record original length (as number of elements)
    input_digits_str = input_str.split()
    original_length = len(input_digits_str)
    
    # Handle empty input case
    if original_length == 0:
        return ""

    # 2. Convert the input string list into a list of integers.
    input_digits_int = [int(d) for d in input_digits_str]

    # 3. Find the index of the first non-zero digit.
    insertion_index = find_first_non_zero_index(input_digits_int)

    # 4. Create a new list by inserting 0 at the insertion_index.
    # Make a copy to avoid modifying the original list if it were needed elsewhere
    modified_digits_int = input_digits_int[:] 
    modified_digits_int.insert(insertion_index, 0)

    # 5. Take the first N elements from the modified list (truncate).
    output_digits_int = modified_digits_int[:original_length]

    # 6. Convert the final list of integers back into a space-separated string.
    output_str = " ".join(map(str, output_digits_int))

    return output_str

```