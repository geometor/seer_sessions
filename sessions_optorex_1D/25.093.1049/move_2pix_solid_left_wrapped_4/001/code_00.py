import math

"""
Transforms an input sequence of numbers by performing a cyclic shift (rotation) 
of all elements in the sequence two positions to the left.
The element originally at index i moves to index (i - 2) mod L, where L is 
the length of the sequence.
"""

def transform(input_grid: str) -> str:
    """
    Applies a left cyclic shift of 2 positions to the input sequence.

    Args:
        input_grid: A string representing a space-separated sequence of integers.

    Returns:
        A string representing the transformed space-separated sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_grid.split()]
    
    # Get the length of the sequence
    length = len(input_list)
    
    # Handle empty input case
    if length == 0:
        return ""
        
    # Initialize the output list with the same length
    output_list = [0] * length 
    
    # Perform the cyclic shift
    for i in range(length):
        # Calculate the new index after shifting 2 positions left, wrapping around
        # The modulo operator handles the wrap-around logic correctly
        new_index = (i - 2) % length 
        
        # Place the element from the original index i into the new index
        output_list[new_index] = input_list[i]
        
    # Convert the output list back into a space-separated string
    output_grid = " ".join(map(str, output_list))
    
    return output_grid
