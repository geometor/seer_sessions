```python
import math
# numpy is often available, but list operations are sufficient here
# import numpy as np 

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

def find_non_zero_indices(grid):
    """Finds the indices of all non-zero elements in the grid."""
    return [i for i, x in enumerate(grid) if x != 0]

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (list or array).
    """
    # Ensure input is a list for mutable operations, handle potential numpy array input
    input_list = list(input_grid) 
    
    # Initialize output_grid as a copy of the input
    output_grid = list(input_list)
    n = len(input_list)

    # Find the indices of all non-zero elements
    non_zero_indices = find_non_zero_indices(input_list)

    # Iterate through consecutive pairs of non-zero indices
    # We need at least two non-zero numbers to have a segment between them
    for idx in range(len(non_zero_indices) - 1):
        i = non_zero_indices[idx]
        j = non_zero_indices[idx + 1]

        # Check if there is at least one element between the non-zero elements (a gap)
        if j > i + 1:
            # Check if all elements between i and j are zeros in the original list
            # Slicing creates a sublist to check
            segment = input_list[i + 1 : j]
            is_zero_segment = all(x == 0 for x in segment)

            if is_zero_segment:
                # Get the values of the boundary elements
                left_val = input_list[i]
                right_val = input_list[j]

                # Determine the fill value based on the conditional logic
                fill_value = -1 # Default value indicating no fill needed
                if left_val == 2 and right_val != 2:
                    fill_value = right_val
                elif left_val != 2 and right_val == 2:
                    fill_value = left_val

                # If a fill value was determined, modify the output_grid
                if fill_value != -1:
                    for k in range(i + 1, j):
                        output_grid[k] = fill_value
                # Otherwise (both 2 or neither 2), do nothing, output_grid retains original zeros

    # Return the modified grid
    return output_grid
```