import re

"""
Take the input sequence of 12 numbers. Split the sequence into two parts: the first part consists of the first 4 elements, and the second part consists of the remaining 8 elements (from the 5th element to the 12th). Create the output sequence by concatenating the second part followed by the first part.
"""

def transform(input_str: str) -> str:
    """
    Transforms an input string sequence by splitting it into two parts and swapping them.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """

    # Parse the input string into a list of integers
    # Use regular expression to find all sequences of digits, handling potential multiple spaces
    elements = [int(x) for x in re.findall(r'\d+', input_str)]

    # Define the split point
    split_index = 4

    # Ensure the input has the expected length (optional but good practice)
    if len(elements) != 12:
        raise ValueError("Input sequence must contain exactly 12 numbers.")

    # Split the sequence into two parts
    first_part = elements[:split_index]
    second_part = elements[split_index:]

    # Concatenate the second part followed by the first part
    output_elements = second_part + first_part

    # Convert the output elements back to strings
    output_str_elements = [str(x) for x in output_elements]

    # Join the string elements with spaces to form the output string
    output_str = " ".join(output_str_elements)

    return output_str
