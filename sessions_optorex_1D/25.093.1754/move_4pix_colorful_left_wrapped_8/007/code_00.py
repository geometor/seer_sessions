import re # Although not strictly necessary for split/join, good practice if pattern matching was needed.

"""
Transforms an input string of 12 space-separated numbers by splitting it 
after the 4th element and swapping the positions of the resulting two segments 
(first 4 elements and last 8 elements).
"""

def parse_input_string(input_str: str) -> list[str]:
    """Parses a space-separated string of numbers into a list of strings."""
    # Split the input string by spaces to get individual number strings
    elements = input_str.split(' ')
    # Filter out any potential empty strings if there are multiple spaces
    # (Although examples suggest clean spacing, this makes it more robust)
    elements = [el for el in elements if el] 
    return elements

def format_output_list(output_list: list[str]) -> str:
    """Formats a list of number strings into a single space-separated string."""
    # Join the elements of the list with a single space
    return ' '.join(output_list)

def transform(input_str: str) -> str:
    """
    Applies the split-and-swap transformation to the input string.

    Args:
        input_str: A string containing 12 space-separated numbers.

    Returns:
        A string containing the transformed sequence of 12 space-separated numbers.
    """
    
    # 1 & 2: Take the input string and split it by spaces into a list of elements.
    numbers = parse_input_string(input_str)
    
    # Define the split point (index 4, as we split *after* the 4th element)
    # Python slicing is [start:end], where 'end' is exclusive.
    split_index = 4

    # 3: Isolate the first segment (indices 0 through 3).
    first_segment = numbers[:split_index] 

    # 4: Isolate the second segment (indices 4 through 11).
    second_segment = numbers[split_index:] 

    # 5: Create a new list by placing the second segment first, followed by the first segment.
    transformed_list = second_segment + first_segment

    # 6: Join the elements of this new list back into a single space-separated string.
    output_str = format_output_list(transformed_list)

    # 7: Return the resulting string.
    return output_str