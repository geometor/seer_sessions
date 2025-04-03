import numpy as np # common library, might be useful for array manipulation, though simple list ops suffice here

"""
Takes an input sequence of integers (represented as a space-separated string), 
moves the first two elements to the end of the sequence, and returns the 
modified sequence as a space-separated string. The relative order of the 
remaining elements (from index 2 onwards) is preserved.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule: moves the first two elements of the 
    input sequence to the end.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)

    # Handle cases where the list might have fewer than 2 elements (though examples suggest fixed length 12)
    if len(input_list) < 2:
        # If fewer than 2 elements, no change or define specific behavior
        # Based on examples, we assume at least 2 elements. Returning input as is for this edge case.
        return input_str 

    # Extract the elements from the third position (index 2) onwards
    remaining_elements = input_list[2:]

    # Extract the first element (index 0)
    first_element = input_list[0]

    # Extract the second element (index 1)
    second_element = input_list[1]

    # Construct the new list by appending the first two elements to the end
    output_list = remaining_elements + [first_element, second_element]

    # Format the resulting list back into a space-separated string
    output_str = format_output(output_list)

    return output_str
