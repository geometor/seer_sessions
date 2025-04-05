```python
import math # math is available
import numpy as np # numpy is available
import collections # collections is available
import re # regular expressions is available


"""
Reorders a sequence of space-separated single-digit integers such that all zero 
elements appear first, followed by all non-zero elements. The relative order of 
the non-zero elements is preserved from the original input sequence.
"""

def transform(input_str: str) -> str:
    """
    Transforms a string of space-separated integers by moving all zeros 
    to the beginning while maintaining the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the reordered space-separated integers.
    """

    # 1. Parse the input string into a list of integers.
    # Split the input string by spaces and convert each part to an integer.
    try:
        numbers_int = [int(n) for n in input_str.split()]
    except ValueError:
        # Handle cases where input might not be valid integers
        print(f"Error: Input string '{input_str}' contains non-integer values.")
        return "" # Or raise an error, depending on desired behavior

    # 2. Create two new empty lists: one for zeros and one for non-zeros.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through the parsed list of integers.
    # Populate the lists based on whether the number is zero or non-zero.
    for num in numbers_int:
        if num == 0:
            # If the integer is 0, append it to the zeros_list.
            zeros_list.append(num)
        else:
            # If the integer is not 0, append it to the non_zeros_list.
            # This preserves the relative order of non-zeros.
            non_zeros_list.append(num)

    # 4. Concatenate the zeros_list and the non_zeros_list.
    # This forms the final ordered list of integers.
    result_list_int = zeros_list + non_zeros_list

    # 5. Convert the integers in the result list back to strings.
    result_list_str = [str(num) for num in result_list_int]

    # 6. Join the string representations with spaces.
    # Format the final list as a space-separated string for output.
    output_str = " ".join(result_list_str)

    # 7. Return the resulting string.
    return output_str

```