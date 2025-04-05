"""
Transforms an input sequence of 12 space-separated integers by moving the 
first 4 elements to the end of the sequence. The input is expected as a 
string, and the output is returned as a string.
"""

import re
# No other specific math/science libraries are needed for this sequence manipulation.

def parse_input_string(input_str: str) -> list[int]:
    """
    Parses a space-separated string of integers into a list of integers.
    Uses regex to reliably find sequences of digits, handling various spacing.
    Raises ValueError if the input does not contain exactly 12 numbers.
    """
    # Find all sequences of digits in the input string
    numbers_str = re.findall(r'\d+', input_str)
    
    # Validate that exactly 12 numbers were found
    if len(numbers_str) != 12:
         raise ValueError(f"Input sequence must contain exactly 12 integers, found {len(numbers_str)} in '{input_str}'.")
         
    # Convert the found digit sequences to integers
    numbers_int = [int(n) for n in numbers_str]
    
    return numbers_int

def format_output_list(output_list: list[int]) -> str:
    """
    Formats a list of integers into a space-separated string.
    """
    return " ".join(map(str, output_list))

def transform(input_grid: str) -> str:
    """
    Applies the transformation rule: splits the sequence after the 4th element
    and moves the first part to the end.

    Args:
        input_grid: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """
    
    # Step 0: Ensure input is a string type, decode if necessary
    if isinstance(input_grid, bytes):
        input_str = input_grid.decode('utf-8')
    else:
        # Ensure it's treated as a string even if passed as another type (e.g., numpy array)
        input_str = str(input_grid) 

    # Step 1: Parse the input string into a list of 12 integer values.
    # Use a helper function for clarity and potential reuse.
    input_list = parse_input_string(input_str)

    # Step 2: Define the split point. The split occurs *after* the 4th element.
    split_index = 4

    # Step 3: Divide the list into two parts based on the split index.
    # The "first part" consists of the first 4 integers (indices 0-3).
    first_part = input_list[:split_index]
    # The "second part" consists of the remaining 8 integers (indices 4-11).
    second_part = input_list[split_index:]

    # Step 4: Create a new list by concatenating the "second part" followed by the "first part".
    # This performs the core rearrangement logic.
    output_list = second_part + first_part

    # Step 5: Format the new list back into a string of space-separated integers.
    # Use a helper function for formatting.
    output_grid = format_output_list(output_list) 

    # Step 6: Return the resulting string.
    return output_grid