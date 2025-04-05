import math

"""
Transforms a sequence of integers by replacing contiguous groups of '5's. 
The replacement values are sourced sequentially from the non-zero numbers 
present in the original input sequence. Numbers other than '5' remain unchanged.
"""

def _parse_input_string(input_str):
  """Converts a space-separated string of digits into a list of integers."""
  return [int(x) for x in input_str.split()]

def _format_output_list(output_list):
  """Converts a list of integers back into a space-separated string."""
  return " ".join(map(str, output_list))

def _extract_replacement_numbers(input_list):
  """Extracts all non-zero numbers from the input list, preserving order."""
  return [num for num in input_list if num != 0]

def transform(input_str):
  """
    Applies the transformation rule to the input sequence string.

    1. Parses the input string into a list of integers.
    2. Extracts the non-zero numbers to be used as replacements.
    3. Iterates through the input list:
        - If the number is not 5, copies it to the output.
        - If the number is 5, determines the correct replacement value 
          (based on the sequence of non-zero numbers and whether it's a new group of 5s) 
          and appends it to the output.
    4. Formats the resulting list back into a space-separated string.
    """

  # 1. Parse the input string
  input_list = _parse_input_string(input_str)
  
  # 2. Extract replacement numbers
  replacement_numbers = _extract_replacement_numbers(input_list)
  
  # Initialize output list and index for replacement numbers
  output_list = []
  replacement_idx = 0
  current_replacement = -1 # Initialize with a value that won't be in the replacements

  # 3. Iterate through the input list and transform
  for i, num in enumerate(input_list):
    if num != 5:
      # If the number is not 5, append it directly
      output_list.append(num)
    else:
      # If the number is 5, check if it's the start of a new group
      is_new_group = (i == 0 or input_list[i-1] != 5)
      
      if is_new_group:
          # If it's a new group, get the next replacement number
          if replacement_idx < len(replacement_numbers):
              current_replacement = replacement_numbers[replacement_idx]
              replacement_idx += 1
          else:
              # Handle potential edge case: more groups of 5 than replacement numbers
              # Based on examples, this shouldn't happen, but we could default or raise error.
              # For now, let's assume valid inputs based on examples and reuse the last one or error.
              # Let's reuse the last one for now, though this might need adjustment.
              if replacement_numbers:
                  current_replacement = replacement_numbers[-1] 
              else:
                  # No replacement numbers found at all - maybe replace with 0 or error
                  current_replacement = 0 # Placeholder if no non-zeros were in input
                  
      # Append the determined replacement number
      output_list.append(current_replacement)

  # 4. Format the output list back to a string
  return _format_output_list(output_list)
