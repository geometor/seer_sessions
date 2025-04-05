"""
The transformation rule takes a sequence of 12 integers, provided as a space-separated string, and performs a circular left rotation by 3 positions. The first 3 elements of the sequence are moved to the end, and the elements from index 3 onwards are shifted to the beginning. The result is returned as a space-separated string.
"""

from typing import List

def parse_string_to_int_list(input_str: str) -> List[int]:
    """ Parses a space-separated string of integers into a list of integers. """
    return [int(x) for x in input_str.split()]

def format_int_list_to_string(int_list: List[int]) -> str:
    """ Formats a list of integers into a space-separated string. """
    return " ".join(map(str, int_list))

def rotate_list_left(sequence: List[int], positions: int) -> List[int]:
    """ Performs a circular left rotation on a list by the specified number of positions. """
    # Check if the list is empty or rotation amount is zero or a multiple of length
    if not sequence or positions % len(sequence) == 0:
        return sequence
    
    # Calculate effective shift amount (handle negative positions or positions > length)
    shift = positions % len(sequence) 
    
    # Perform rotation using slicing
    rotated_sequence = sequence[shift:] + sequence[:shift]
    return rotated_sequence

def transform(input_str: str) -> str:
    """
    Applies a circular left shift of 3 positions to a sequence of 12 integers
    represented as a space-separated string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed 12 space-separated integers.
    """
    
    # Define the number of positions for the circular left shift
    shift_amount = 3
    expected_length = 12

    # Step 1: Parse the input string into a list of integers
    input_list = parse_string_to_int_list(input_str)

    # Optional: Validate input length (can be useful for robustness)
    if len(input_list) != expected_length:
        # In a real application, might raise an error or return a specific format
        # For this context, we assume valid input based on examples
        print(f"Warning: Input list length is {len(input_list)}, expected {expected_length}.")
        # Decide how to handle: raise error, return original, or attempt transformation?
        # Let's attempt transformation, assuming the core logic is the focus.
        # If strict validation is needed, uncomment the below line:
        # raise ValueError(f"Input sequence must contain exactly {expected_length} integers.")

    # Step 2: Perform the circular left rotation by the specified amount
    rotated_list = rotate_list_left(input_list, shift_amount)

    # Step 3: Format the resulting list back into a space-separated string
    output_str = format_int_list_to_string(rotated_list)

    # Step 4: Return the transformed string
    return output_str