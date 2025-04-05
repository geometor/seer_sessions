"""
Parses an input string representing a list of digits (0, 1, or 2) enclosed in 
square brackets and separated by spaces (e.g., '[2 2 0 1 ...]'). It then sorts 
these digits in descending order (2s first, then 1s, then 0s) and returns the 
result as a space-separated string.
"""

import re # Used for robust splitting in case of multiple spaces

def parse_input_string_to_list(input_str: str) -> list[int]:
    """
    Parses the specific input string format '[d d ...]' into a list of integers.
    
    Args:
        input_str: The input string, e.g., '[2 2 0 1 0 2 2 0 2 2 0 0]'.
        
    Returns:
        A list of integers extracted from the string.
    """
    # 1. Remove leading '[' and trailing ']'
    #    Use strip('[]') to handle potential whitespace around brackets as well.
    content = input_str.strip().strip('[]')
    
    # 2. Handle empty case (like '[]' which becomes '')
    if not content:
        return []
        
    # 3. Split the remaining string by spaces (handle multiple spaces)
    #    Use re.split to handle one or more spaces as delimiters.
    digit_strings = re.split(r'\s+', content.strip())
    
    # 4. Convert each part to an integer
    digits = [int(d) for d in digit_strings]
    
    return digits

def format_list_to_output_string(digit_list: list[int]) -> str:
    """
    Formats a list of digits into a space-separated string.
    
    Args:
        digit_list: A list of integers (0, 1, or 2).
        
    Returns:
        A string representation, e.g., '2 2 1 0 0'.
    """
    # 1. Convert each integer back to a string
    string_digits = [str(d) for d in digit_list]
    
    # 2. Join with spaces
    output_str = " ".join(string_digits)
    
    return output_str

def transform(input_str: str) -> str:
    """
    Transforms the input string representation of a digit list by sorting the 
    digits in descending order.

    Args:
        input_str: A string like '[2 2 0 1 0 2 2 0 2 2 0 0]' containing 12 digits
                   (0, 1, or 2) separated by spaces within brackets.

    Returns:
        A string containing the same digits sorted in descending order,
        separated by spaces, e.g., '2 2 2 2 2 2 1 0 0 0 0 0'.
    """
    
    # 1. Parse the input string into a list of integers.
    #    Handles removal of brackets, splitting, and conversion to int.
    digits = parse_input_string_to_list(input_str)
    
    # 2. Sort the list of digits in descending order (2 > 1 > 0).
    #    The sort() method modifies the list in-place.
    digits.sort(reverse=True)
    
    # 3. Format the sorted list back into the required output string format.
    #    Converts integers to strings and joins them with spaces.
    output_str = format_list_to_output_string(digits)
    
    # 4. Return the resulting string.
    return output_str
