```python
import re

"""
Transforms a string of space-separated digits by replacing every non-zero digit with '5' and leaving '0' digits unchanged.
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
    for digit in input_digits:
        # Check if the digit is '0'
        if digit == '0':
            # If it's '0', keep it as '0'
            output_digits.append('0')
        else:
            # If it's any non-zero digit ('1' through '9'), replace it with '5'
            output_digits.append('5')

    # Join the processed list of digit strings back into a single string, separated by spaces
    output_str = ' '.join(output_digits)

    # Return the resulting string
    return output_str

```