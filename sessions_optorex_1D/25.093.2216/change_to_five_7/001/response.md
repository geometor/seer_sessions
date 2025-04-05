```python
import re

"""
Transform a sequence of digits element-wise: if the input digit is 0, the output digit is 0; otherwise (if the input digit is 1-9), the output digit is 5.
"""

def transform(input_str: str) -> str:
    """
    Transforms a space-separated string of digits according to the rule:
    0 maps to 0, non-zero maps to 5.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string containing the transformed space-separated single digits.
    """
    # Split the input string into individual digit strings
    input_digits_str = input_str.split()

    # Convert digit strings to integers
    input_digits_int = [int(d) for d in input_digits_str]

    # Initialize an empty list to store the output digits
    output_digits_int = []

    # Iterate through each input digit
    for digit in input_digits_int:
        # Apply the transformation rule
        if digit == 0:
            # If the digit is 0, append 0 to the output list
            output_digits_int.append(0)
        else:
            # If the digit is non-zero, append 5 to the output list
            output_digits_int.append(5)

    # Convert the output integers back to strings
    output_digits_str = [str(d) for d in output_digits_int]

    # Join the output digit strings with spaces
    output_str = " ".join(output_digits_str)

    return output_str

```