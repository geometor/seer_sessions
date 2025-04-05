```python
import math
import numpy as np
import re # Using re for potentially splitting strings if needed, though simple split is likely sufficient

"""
Transformation Rule:
Accepts a sequence of space-separated digits. Converts any non-zero digit to 0 if it is not adjacent (horizontally) to another digit of the same value. Otherwise, the digit remains unchanged. Zeros always remain zero. Returns the modified sequence as a space-separated string.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    Changes isolated non-zero digits to 0.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    n = len(input_list)
    
    # Initialize the output list as a copy of the input list
    output_list = list(input_list) 

    # Iterate through the input list to identify isolated non-zero digits
    for i in range(n):
        current_value = input_list[i]

        # Skip if the current digit is zero
        if current_value == 0:
            continue

        # Check the left neighbor
        has_same_left_neighbor = False
        if i > 0: # Check if a left neighbor exists
            if input_list[i-1] == current_value:
                has_same_left_neighbor = True
                
        # Check the right neighbor
        has_same_right_neighbor = False
        if i < n - 1: # Check if a right neighbor exists
            if input_list[i+1] == current_value:
                has_same_right_neighbor = True

        # If neither neighbor has the same value, it's isolated
        if not has_same_left_neighbor and not has_same_right_neighbor:
            # Change the corresponding digit in the output list to 0
            output_list[i] = 0

    # Format the output list back into a space-separated string
    output_str = format_output(output_list)
    
    return output_str

```