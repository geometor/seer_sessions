```python
import numpy as np # Although not strictly needed for list operations, keeping it for potential future grid tasks or consistency.

"""
Rearranges a sequence of 12 digits, provided as a space-separated string, 
by splitting the sequence into two parts after the 4th digit and swapping 
their order. The output is also a space-separated string.
"""

def parse_input_string(input_str):
  """ Parses a space-separated string of digits into a list of integers. """
  return [int(digit) for digit in input_str.split()]

def format_output_list(output_list):
  """ Formats a list of integers into a space-separated string. """
  return " ".join(map(str, output_list))

def transform(input_str):
    """
    Applies the split-and-swap transformation to the input string.

    Args:
        input_str: A string containing 12 space-separated single digits.

    Returns:
        A string containing the rearranged 12 space-separated single digits.
    """

    # 1. Parse the input string into a list of integers
    # Example: "6 9 5 0 0 0 0 0 0 1 8 6" -> [6, 9, 5, 0, 0, 0, 0, 0, 0, 1, 8, 6]
    integer_list = parse_input_string(input_str)

    # Check if parsing resulted in the expected number of elements (optional but good practice)
    if len(integer_list) != 12:
        # Handle error appropriately, e.g., raise an exception or return an error indicator
        # For this specific task based on examples, we assume valid input.
        print(f"Warning: Input did not parse to 12 elements: {input_str}") # Or raise ValueError

    # 2. Identify the two segments
    split_index = 4
    first_segment = integer_list[:split_index] # Elements from index 0 up to (not including) 4
    second_segment = integer_list[split_index:] # Elements from index 4 to the end

    # Example:
    # first_segment = [6, 9, 5, 0]
    # second_segment = [0, 0, 0, 0, 0, 1, 8, 6]

    # 3. Construct the rearranged list by concatenating segment 2 then segment 1
    rearranged_list = second_segment + first_segment
    # Example: rearranged_list = [0, 0, 0, 0, 0, 1, 8, 6] + [6, 9, 5, 0]
    #                      = [0, 0, 0, 0, 0, 1, 8, 6, 6, 9, 5, 0]

    # 4. Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)
    # Example: output_str = "0 0 0 0 0 1 8 6 6 9 5 0"

    # 5. Return the final string
    return output_str

```