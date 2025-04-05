import re

"""
Transforms a sequence of space-separated digits by replacing each non-zero digit with '5' and leaving '0' digits unchanged.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """
    # Split the input string into a list of individual digit strings
    input_digits = input_str.split(' ')

    # Initialize an empty list to store the output digits
    output_digits = []

    # Iterate through each digit string in the input list
    for digit_str in input_digits:
        # Check if the digit string is '0'
        if digit_str == '0':
            # If it's '0', append '0' to the output list
            output_digits.append('0')
        else:
            # If it's not '0' (any digit from '1' to '9'), append '5'
            output_digits.append('5')

    # Join the output digits back into a space-separated string
    output_str = ' '.join(output_digits)

    # Return the transformed string
    return output_str
