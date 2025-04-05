import collections

"""
Transforms an input sequence of numbers by performing a left rotation.
The first element (at index 0) of the input sequence is moved to the last position, 
and all other elements are shifted one position to the left.
"""

def transform(input_sequence):
    """
    Rotates the elements of the input sequence one position to the left.

    Args:
        input_sequence: A list of numbers.

    Returns:
        A new list representing the left-rotated sequence.
    """
    # Check if the input sequence is empty or has only one element, 
    # in which case rotation has no effect.
    if not input_sequence or len(input_sequence) < 2:
        return list(input_sequence) # Return a copy to avoid modifying the original if needed

    # Create a deque for efficient rotation
    # A deque (double-ended queue) supports adding and removing elements 
    # from either end in O(1) time.
    d = collections.deque(input_sequence)
    
    # Perform one left rotation: 
    # Removes the leftmost element and appends it to the right.
    d.rotate(-1) 
    
    # Convert the deque back to a list to match the expected output format.
    output_sequence = list(d)

    return output_sequence
