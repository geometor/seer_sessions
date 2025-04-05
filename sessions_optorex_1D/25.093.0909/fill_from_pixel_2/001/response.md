```python
import math
import re # Using re for potential string parsing if needed, although assuming list input for now

"""
Transforms the input list by conditionally filling leading/trailing zeros.
Zeros at the start are filled with the value of the first non-zero element 
if its value differs from the second non-zero element (or if only one non-zero element exists).
Zeros at the end are filled with the value of the last non-zero element 
if its value differs from the second-to-last non-zero element (or if only one non-zero element exists).
"""

def find_non_zeros(data_list):
    """
    Identifies all non-zero elements and their indices in a list.

    Args:
        data_list: A list of numbers.

    Returns:
        A list of tuples, where each tuple is (value, index) for a non-zero element.
        Returns an empty list if no non-zero elements are found.
    """
    non_zeros = []
    for index, value in enumerate(data_list):
        if value != 0:
            non_zeros.append((value, index))
    return non_zeros

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input list.

    Args:
        input_grid: A list of integers (0-9).

    Returns:
        A new list of integers representing the transformed output.
    """
    # initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find all non-zero elements and their indices
    non_zeros = find_non_zeros(input_grid)

    # If there are no non-zero elements, return the original list
    if not non_zeros:
        return output_grid

    num_non_zeros = len(non_zeros)

    # --- Left Fill Check ---
    # Get the first non-zero element
    v1, i1 = non_zeros[0]
    
    # Determine if the left side (leading zeros) should be filled
    fill_left = False
    if num_non_zeros == 1:
        # If there's only one non-zero number, always fill the left
        fill_left = True
    else:
        # If there are multiple non-zeros, compare the first two
        v2, i2 = non_zeros[1]
        if v1 != v2:
            fill_left = True

    # Perform the left fill if the condition is met
    if fill_left:
        for i in range(i1): # Iterate from index 0 up to (but not including) i1
            if output_grid[i] == 0: # Only fill existing zeros
                 output_grid[i] = v1

    # --- Right Fill Check ---
    # Get the last non-zero element
    vL, iL = non_zeros[-1]

    # Determine if the right side (trailing zeros) should be filled
    fill_right = False
    if num_non_zeros == 1:
         # If there's only one non-zero number, always fill the right
        fill_right = True
    else:
        # If there are multiple non-zeros, compare the last two
        vL_minus_1, iL_minus_1 = non_zeros[-2]
        if vL != vL_minus_1:
            fill_right = True

    # Perform the right fill if the condition is met
    if fill_right:
        for i in range(iL + 1, len(output_grid)): # Iterate from index iL + 1 to the end
             if output_grid[i] == 0: # Only fill existing zeros
                output_grid[i] = vL

    return output_grid

# Example Usage (parsing string input as seen in examples)
def parse_input_string(s: str) -> list[int]:
    return [int(x) for x in s.split()]

def format_output_list(lst: list[int]) -> str:
    return " ".join(map(str, lst))

# Test cases from the problem description
train_examples = [
    ("0 0 0 0 0 1 8 8 8 0 0 0", "1 1 1 1 1 1 8 8 8 0 0 0"),
    ("0 0 6 8 8 8 8 0 0 0 0 0", "6 6 6 8 8 8 8 0 0 0 0 0"),
    ("0 0 1 1 1 1 3 0 0 0 0 0", "0 0 1 1 1 1 3 3 3 3 3 3"),
    ("0 0 2 5 5 5 0 0 0 0 0 0", "2 2 2 5 5 5 0 0 0 0 0 0"),
    ("9 4 4 4 4 0 0 0 0 0 0 0", "9 4 4 4 4 0 0 0 0 0 0 0"), # No change expected here
    ("0 0 8 1 1 1 1 0 0 0 0 0", "8 8 8 1 1 1 1 0 0 0 0 0"),
    ("0 0 0 0 7 7 7 2 0 0 0 0", "0 0 0 0 7 7 7 2 2 2 2 2"),
]

# print("Testing transform function:")
# for i, (input_str, expected_output_str) in enumerate(train_examples):
#     input_list = parse_input_string(input_str)
#     output_list = transform(input_list)
#     output_str = format_output_list(output_list)
#     print(f"Train {i+1}:")
#     print(f"  Input:    {input_str}")
#     print(f"  Output:   {output_str}")
#     print(f"  Expected: {expected_output_str}")
#     print(f"  Match:    {output_str == expected_output_str}")
#     print("-" * 10)
```