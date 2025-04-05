```python
import math
import numpy as np
import re # Using re for potentially more complex parsing if needed later, though split is sufficient now.

"""
Transforms a sequence of digits based on the following rule:
1. Identify all non-zero digits and their positions in the sequence.
2. Examine each contiguous segment of zeros that is located strictly *between* two non-zero digits.
3. Let the non-zero digit to the left of the zero segment be 'left_val' at index 'i', and the non-zero digit to the right be 'right_val' at index 'j'.
4. If 'left_val' is 2 and 'right_val' is *not* 2, fill the zero segment (elements from index i+1 to j-1) with 'right_val'.
5. If 'left_val' is *not* 2 and 'right_val' is 2, fill the zero segment (elements from index i+1 to j-1) with 'left_val'.
6. In all other cases (both are 2, neither is 2, or the segment is not composed entirely of zeros), the segment remains unchanged.
7. Zeros at the beginning or end of the sequence, or adjacent to only one non-zero number, are not modified.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.strip().split(' ')]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return ' '.join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    
    # Create a copy of the input list to modify for the output
    output_list = list(input_list) # Use list() or [:] for a copy
    n = len(input_list)

    # Find the indices of all non-zero elements
    non_zero_indices = [i for i, x in enumerate(input_list) if x != 0]

    # Iterate through consecutive pairs of non-zero indices
    # We need at least two non-zero numbers to have a segment between them
    for idx in range(len(non_zero_indices) - 1):
        i = non_zero_indices[idx]
        j = non_zero_indices[idx + 1]

        # Check if there is at least one element between the non-zero elements
        if j > i + 1:
            # Check if all elements between i and j are zeros in the original list
            is_zero_segment = all(input_list[k] == 0 for k in range(i + 1, j))

            if is_zero_segment:
                # Get the values of the boundary elements
                left_val = input_list[i]
                right_val = input_list[j]

                # Apply the filling logic based on the boundary values
                if left_val == 2 and right_val != 2:
                    # Fill the segment with the right boundary value
                    fill_value = right_val
                    for k in range(i + 1, j):
                        output_list[k] = fill_value
                elif left_val != 2 and right_val == 2:
                    # Fill the segment with the left boundary value
                    fill_value = left_val
                    for k in range(i + 1, j):
                        output_list[k] = fill_value
                # Otherwise (both 2 or neither 2), do nothing, the segment remains zeros

    # Format the transformed list back into a space-separated string
    return format_output(output_list)

```