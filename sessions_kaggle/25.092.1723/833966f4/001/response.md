```python
import math
from typing import List, Tuple, Any

"""
Transforms an input list by swapping adjacent elements in pairs.
Iterates through the input list with a step of 2. For each pair of indices (i, i+1), 
it appends the element at index i+1 followed by the element at index i to the output list. 
If the list has an odd number of elements, the last element is appended without swapping.
"""

def transform(input_list: List[int]) -> List[int]:
    """
    Swaps adjacent pairs of elements in the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A new list with adjacent elements swapped.
    """
    # Initialize an empty list to store the transformed elements
    output_list = []
    
    # Initialize the index for iteration
    i = 0
    n = len(input_list)

    # Iterate through the list with a step of 2
    while i < n:
        # Check if there is a next element to form a pair
        if i + 1 < n:
            # If a pair exists, swap them and append to the output list
            # Append the element at index i+1 first
            output_list.append(input_list[i+1])
            # Append the element at index i second
            output_list.append(input_list[i])
        else:
            # If it's the last element in an odd-length list, append it directly
            output_list.append(input_list[i])
            
        # Move to the next pair (or the position after the single last element)
        i += 2
        
    # Return the newly created list with swapped pairs
    return output_list

```