```python
import math

"""
Parses the input multi-line string into a list of lines. 
Iterates through the list, swapping adjacent pairs of elements (index i and i+1). 
If the list has an odd number of elements, the last element remains in its place relative to the swapped pairs.
Formats the modified list back into a multi-line string.
"""

def transform(input_str: str) -> str:
    """
    Swaps adjacent elements in a list derived from a multi-line input string.

    Args:
        input_str: A multi-line string where each line represents an element.

    Returns:
        A multi-line string with adjacent elements swapped.
    """
    # Parse the input multi-line string into a list of elements (lines)
    lines = input_str.splitlines()
    
    # Get the number of elements in the list
    n = len(lines)
    
    # Iterate through the list with a step of 2
    i = 0
    while i < n - 1: # Ensure there's a next element to swap with
        # Swap the element at the current index (i) with the element at the next index (i+1)
        lines[i], lines[i+1] = lines[i+1], lines[i]
        # Increment by 2 to move to the next pair
        i += 2
        
    # Format the resulting list back into a multi-line string
    output_str = "\n".join(lines)
    
    # Return the formatted string
    return output_str

```