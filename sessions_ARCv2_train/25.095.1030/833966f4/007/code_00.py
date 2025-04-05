import math

"""
Transforms a multi-line string input by parsing it into a list of lines (elements). 
It then iterates through the list. If the index `i` of an element is a multiple of 3 
(0, 3, 6, ...), the element at index `i` and the element at index `i+1` are swapped, 
provided `i+1` is a valid index. Finally, the modified list is joined back into a 
multi-line string.
"""

def transform(input_str: str) -> str:
    """
    Parses a multi-line string, swaps adjacent elements if the starting index
    is a multiple of 3, and formats the result back to a multi-line string.

    Args:
        input_str: A multi-line string where each line is an element.

    Returns:
        A multi-line string with specific adjacent elements swapped.
    """
    # Parse the input multi-line string into a list of lines (elements)
    lines = input_str.splitlines()
    
    # Create a mutable copy of the list to modify
    # (though modifying in place is fine for this structure)
    output_lines = list(lines)
    
    # Get the number of elements
    n = len(output_lines)
    
    # Iterate through the indices `i` of the list, up to n-2 to ensure `i+1` is valid
    for i in range(n - 1):
        # Check if the current index `i` is a multiple of 3
        if i % 3 == 0:
            # Swap the element at the current index (i) with the element at the next index (i+1)
            output_lines[i], output_lines[i+1] = output_lines[i+1], output_lines[i]
            
    # Format the modified list back into a multi-line string
    output_str = "\n".join(output_lines)
    
    # Return the resulting multi-line string
    return output_str
