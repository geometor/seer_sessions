import math
import numpy as np

"""
Transforms a sequence of digits based on the following rule:
Iterate through the input sequence starting from the second digit. 
If a digit is '2' and the preceding digit is also '2', replace the current digit with '8'. 
Otherwise, keep the digit as it is. The first digit is never changed.
The output is the transformed sequence of digits, joined by spaces.
"""

def parse_input(input_str):
  """Converts the input string into a list of strings (digits)."""
  return input_str.split(' ')

def format_output(output_list):
  """Converts the list of output digits back into a space-separated string."""
  return ' '.join(output_list)

def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string of space-separated digits.

    Returns:
        A string representing the transformed sequence.
    """
    # Parse the input string into a list of digits (as strings)
    input_digits = parse_input(input_str)
    
    # Handle empty or single-element input
    if not input_digits or len(input_digits) == 0:
        return ""
    if len(input_digits) == 1:
        return input_digits[0]

    # Initialize the output list with the first digit (it never changes)
    output_digits = [input_digits[0]]

    # Iterate through the input digits starting from the second one (index 1)
    for i in range(1, len(input_digits)):
        # Get the current digit and the previous digit
        current_digit = input_digits[i]
        previous_digit = input_digits[i-1]

        # Check the transformation condition: current is '2' and previous is '2'
        if current_digit == '2' and previous_digit == '2':
            # If the condition is met, append '8' to the output
            output_digits.append('8')
        else:
            # Otherwise, append the original current digit to the output
            output_digits.append(current_digit)

    # Format the output list back into a space-separated string
    output_str = format_output(output_digits)

    return output_str