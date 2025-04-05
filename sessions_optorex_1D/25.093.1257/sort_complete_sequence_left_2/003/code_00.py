"""
Parses an input string containing 12 space-separated integers.
Identifies the integer at index 4 (the fifth element) as the dominant digit 'X'.
Constructs and returns a new string representing a list of 12 integers 
following the pattern [0, 0, 0, 0, X, X, X, 0, X, X, 0, X].
"""

import numpy as np
import math

# Helper function to parse the input string into a list of integers
def parse_input(input_str):
  """Converts a space-separated string of integers into a list of integers."""
  try:
    return [int(x) for x in input_str.split()]
  except ValueError:
    # Handle cases where the string might not contain valid integers
    print(f"Warning: Could not parse input string into integers: {input_str}")
    return [] # Or raise an error

# Helper function to get the dominant digit
def get_dominant_digit(sequence):
  """Extracts the digit at index 4."""
  if len(sequence) > 4:
    return sequence[4]
  else:
    # Handle potential edge case if parsed input is unexpectedly short
    print("Warning: Parsed sequence shorter than expected.")
    # Returning 0 might be a safe default if the pattern needs an integer
    return 0 

# Helper function to construct the target sequence
def construct_target_sequence(dominant_digit):
  """Constructs the target sequence list based on the dominant digit."""
  X = dominant_digit
  # Define the fixed pattern structure
  pattern_structure = [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
  return pattern_structure

# Helper function to format the output list back into a string
def format_output(output_list):
  """Converts a list of integers back into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str):
    """
    Transforms an input string of 12 integers based on the digit at index 4.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string representing a list of 12 integers following the pattern 
        [0, 0, 0, 0, X, X, X, 0, X, X, 0, X], where X is the integer 
        at index 4 of the parsed input. Returns an empty string or a default
        pattern string if input parsing fails.
    """
    
    # 1. Parse the input string into a list of integers
    input_sequence = parse_input(input_str)
    
    # Handle potential parsing errors
    if not input_sequence or len(input_sequence) != 12:
        print(f"Error: Input string '{input_str}' could not be parsed correctly or has incorrect length.")
        # Return a default or empty value based on requirements
        # Let's return an empty string for now
        return "" 

    # 2. Identify the dominant non-zero digit 'X' (value at index 4)
    dominant_digit = get_dominant_digit(input_sequence)
    
    # 3. Construct the target output sequence list using the fixed pattern and 'X'
    output_sequence_list = construct_target_sequence(dominant_digit)

    # 4. Format the output list back into a space-separated string
    output_str = format_output(output_sequence_list)

    # 5. Return the newly constructed string
    return output_str