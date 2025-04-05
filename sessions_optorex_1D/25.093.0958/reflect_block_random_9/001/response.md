```python
import math

"""
Reverses the contiguous sub-sequence of non-zero digits within a sequence of digits, 
leaving any leading or trailing zeros in their original positions.
"""

def find_first_non_zero_index(data):
    """Finds the index of the first non-zero element."""
    for i, x in enumerate(data):
        if x != 0:
            return i
    return -1 # Indicate no non-zero element found

def find_last_non_zero_index(data):
    """Finds the index of the last non-zero element."""
    for i in range(len(data) - 1, -1, -1):
        if data[i] != 0:
            return i
    return -1 # Indicate no non-zero element found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    1. Parse the input string into a list of integers.
    2. Find the start and end indices of the contiguous non-zero block.
    3. If no non-zero block exists, return the original string.
    4. Extract the leading zeros, the non-zero block, and the trailing zeros.
    5. Reverse the non-zero block.
    6. Reconstruct the list by combining the parts.
    7. Format the resulting list back into a space-separated string.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Find the start and end indices of the contiguous non-zero block.
    start_index = find_first_non_zero_index(input_list)
    
    # 3. If no non-zero block exists (all zeros), return the original string.
    if start_index == -1:
        return input_str
        
    end_index = find_last_non_zero_index(input_list)

    # 4. Extract the leading zeros, the non-zero block, and the trailing zeros.
    leading_zeros = input_list[:start_index]
    non_zero_block = input_list[start_index : end_index + 1]
    trailing_zeros = input_list[end_index + 1:]

    # 5. Reverse the non-zero block.
    reversed_non_zero_block = non_zero_block[::-1] # Python slicing for reversal

    # 6. Reconstruct the list by combining the parts.
    output_list = leading_zeros + reversed_non_zero_block + trailing_zeros

    # 7. Format the resulting list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str

```