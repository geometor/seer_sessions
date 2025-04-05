"""
Transforms an input sequence of space-separated integers (provided as a string) by moving the first 3 integers to the end of the sequence, while preserving the relative order of both the moved elements and the remaining elements. Returns the transformed sequence as a space-separated string.
"""

import re # Although not strictly needed for split(), might be useful for more complex parsing if requirements changed.

# Helper function to parse the input string
def parse_input_string(input_str: str) -> list[str]:
    """Parses a space-separated string into a list of strings."""
    return input_str.split(' ')

# Helper function to format the output list
def format_output_list(output_list: list[str]) -> str:
    """Formats a list of strings into a space-separated string."""
    return ' '.join(output_list)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule: move the first 3 elements to the end.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed sequence of space-separated integers.
    """
    
    # Parse the input string into a list of its elements (as strings)
    input_list = parse_input_string(input_str)
    
    # Define the number of elements to move from the start to the end
    n_to_move = 3
    
    # Check if the list is long enough to perform the move
    # Based on examples, length is always 12, so this check is robust for the given data.
    if len(input_list) <= n_to_move:
        # If the list has n or fewer elements, return it unchanged 
        # (or handle as an error, though not needed for provided examples).
        return input_str 

    # Split the list into two parts:
    # head_segment: The first n_to_move elements
    head_segment = input_list[:n_to_move]
    
    # tail_segment: The remaining elements starting from index n_to_move
    tail_segment = input_list[n_to_move:]
    
    # Concatenate the tail followed by the head to form the new sequence
    output_list = tail_segment + head_segment
    
    # Format the resulting list back into a space-separated string
    output_str = format_output_list(output_list)
    
    # Return the transformed string
    return output_str
