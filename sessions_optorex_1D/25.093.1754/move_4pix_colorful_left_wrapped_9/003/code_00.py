import re
import numpy as np # Although not strictly needed for this task, it's often available

"""
Transforms an input sequence of 12 space-separated integers by moving the 
first 4 elements to the end of the sequence. 
The input is expected as a string, and the output is returned as a string.
"""

def parse_input_string(input_str: str) -> list[int]:
    """
    Parses a space-separated string of integers into a list of integers.
    Handles potential leading/trailing whitespace.
    """
    # Use regex to find all sequences of digits
    # Handles potential multiple spaces or non-digit characters gracefully, 
    # focusing only on extracting numbers.
    numbers_str = re.findall(r'\d+', input_str)
    if not numbers_str:
        raise ValueError("Input string does not contain any numbers.")
        
    numbers_int = [int(n) for n in numbers_str]
    
    if len(numbers_int) != 12:
         raise ValueError(f"Input sequence must contain exactly 12 integers, found {len(numbers_int)}.")

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
                    (Note: The name input_grid is per template, but it's treated as a string here).

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """
    
    # The input is expected as a string based on examples.
    # The previous error suggested bytes might be passed in the execution environment.
    # Add a check and decode if necessary.
    if isinstance(input_grid, bytes):
        input_str = input_grid.decode('utf-8')
    else:
        input_str = str(input_grid) # Ensure it's a string

    # 1. Parse the input string into a list of integers
    input_list = parse_input_string(input_str)

    # 2. Define the split point
    split_index = 4

    # 3. Identify the first part (elements 0 through split_index - 1)
    first_part = input_list[:split_index]

    # 4. Identify the second part (elements split_index through the end)
    second_part = input_list[split_index:]

    # 5. Construct the output list by concatenating second part + first part
    output_list = second_part + first_part

    # 6. Format the output list back into a space-separated string
    output_grid = format_output_list(output_list) # Using output_grid name per template

    return output_grid