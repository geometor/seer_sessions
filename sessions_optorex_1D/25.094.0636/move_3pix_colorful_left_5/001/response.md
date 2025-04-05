```python
import math # common math library available

"""
Identify the contiguous segment in the input list that starts with the first non-zero digit 
and ends with the last non-zero digit. Shift this entire segment 3 positions to the left, 
handling boundary conditions (cannot shift past index 0). Create an output list of the 
same length as the input, filled with zeros, and place the shifted segment into it.
If the input list contains only zeros, return a list of zeros of the same length.
"""

def find_first_nonzero_index(data):
    """Finds the index of the first non-zero element."""
    for i, val in enumerate(data):
        if val != 0:
            return i
    return -1 # Indicate no non-zero element found

def find_last_nonzero_index(data):
    """Finds the index of the last non-zero element."""
    for i in range(len(data) - 1, -1, -1):
        if data[i] != 0:
            return i
    return -1 # Indicate no non-zero element found

def transform(input_list):
    """
    Transforms the input list by identifying the core non-zero segment
    and shifting it 3 positions to the left within a zero-padded list
    of the same original length.
    """
    n = len(input_list)
    
    # Initialize the output list with zeros
    output_list = [0] * n

    # Find the start and end indices of the segment containing non-zero numbers
    start_index = find_first_nonzero_index(input_list)
    end_index = find_last_nonzero_index(input_list)

    # If no non-zero elements exist, the output is identical to the input (all zeros)
    if start_index == -1:
        return output_list # Already initialized as all zeros

    # Extract the segment (including any zeros within the non-zero boundaries)
    segment = input_list[start_index : end_index + 1]
    segment_len = len(segment)

    # Calculate the target start index for the segment in the output
    # Shift amount is 3 to the left, ensuring it doesn't go below index 0
    target_start_index = max(0, start_index - 3)

    # Place the segment into the output list at the target position
    # Ensure the segment doesn't write past the end of the output list
    # (Although not strictly needed based on examples, good practice)
    end_placement_index = min(target_start_index + segment_len, n)
    elements_to_place = end_placement_index - target_start_index
    
    for i in range(elements_to_place):
        output_list[target_start_index + i] = segment[i]

    return output_list

```