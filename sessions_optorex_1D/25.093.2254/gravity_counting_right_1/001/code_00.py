"""
Generates a binary sequence where the number of leading '1's corresponds 
to the count of non-zero digits in the input sequence, and the remaining 
positions are filled with '0's. The total length of the output sequence 
matches the input sequence length.
"""

import numpy as np

def count_non_zero(numbers):
  """Counts the number of non-zero elements in a list of numbers."""
  count = 0
  for num in numbers:
    if num != 0:
      count += 1
  return count

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated digits into a binary string.

    The transformation counts the non-zero digits in the input. The output
    string starts with that many '1's, followed by '0's to match the
    original length.

    Args:
        input_str: A string of space-separated digits (e.g., "4 0 6 0").

    Returns:
        A string of space-separated binary digits (e.g., "1 1 0 0").
    """
    # Parse the input string into a list of integers
    try:
        input_numbers = [int(digit) for digit in input_str.split()]
    except ValueError:
        # Handle cases where input might not be purely digits or spaces
        print(f"Error: Input string '{input_str}' contains non-digit characters.")
        # Decide on error handling: return None, raise exception, or return default
        return "" # Or raise ValueError("Invalid input format")

    # Get the total length of the input sequence
    total_length = len(input_numbers)

    # Count the number of non-zero elements
    non_zero_count = count_non_zero(input_numbers)
    # Alternatively using list comprehension:
    # non_zero_count = sum(1 for num in input_numbers if num != 0)

    # Create the output list
    output_list = []

    # Append '1's based on the non-zero count
    for _ in range(non_zero_count):
        output_list.append('1')

    # Append '0's for the remaining length
    for _ in range(total_length - non_zero_count):
        output_list.append('0')

    # Join the output list elements with spaces to form the final string
    output_str = " ".join(output_list)

    return output_str
