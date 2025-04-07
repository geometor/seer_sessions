```python
"""
Transforms an input list of integers according to the following rule:
1. The first line of the output represents the initial input list, formatted as a space-separated string.
2. Subsequent lines are generated iteratively by replacing the leftmost '0' in the current list state with the value of the first element of the original input list.
3. The number of replacement steps (R) performed is calculated as R = (L + 2) // 3 (integer division, equivalent to ceil(L / 3)), where L is the length of the input list.
4. The total number of output lines is R + 1. The process stops after R replacements or when no more zeros are found.
"""

import math # Although not strictly needed with integer division, kept for context
from typing import List, Union # Using Union for Python < 3.10 compatibility if needed

def format_sequence_to_string(int_list: List[int]) -> str:
  """Formats a list of integers into a space-separated string."""
  return " ".join(map(str, int_list))

def find_first_zero_index(int_list: List[int]) -> Union[int, None]:
  """Finds the index of the first zero in the list. Returns None if not found."""
  try:
    return int_list.index(0)
  except ValueError:
    return None

def transform(input_sequence: List[int]) -> str:
  """
  Applies the iterative zero-replacement transformation to the input list.

  Args:
    input_sequence: A list of integers.

  Returns:
    A string containing the initial state and subsequent states after each 
    replacement step, separated by newlines.
  """
  
  # Determine the total length L of the input_sequence
  L = len(input_sequence)
  if L == 0:
      return "" # Handle empty input case

  # Calculate the number of replacement steps R
  # R = math.ceil(L / 3) # equivalent using integer division
  R = (L + 2) // 3 
  
  # Identify the fill_digit (first element)
  # Ensure there's at least one element before accessing index 0
  # This is covered by the L==0 check above, but good practice
  fill_digit = input_sequence[0] 
  
  # Initialize a list to store the output sequences (as lists of integers)
  output_sequences_as_lists = []
  
  # Start with the initial sequence
  current_sequence = list(input_sequence) # Work with a copy
  
  # Add the initial sequence state to the output list
  output_sequences_as_lists.append(list(current_sequence)) # Store another copy for the output list

  # Repeat the replacement R times
  for _ in range(R):
    # Find the index of the first occurrence of 0 in the current_sequence
    index_zero = find_first_zero_index(current_sequence)
    
    # If a 0 is found
    if index_zero is not None:
      # Update the element at index_zero in the current_sequence *for the next iteration*
      current_sequence[index_zero] = fill_digit
      # Add the *new state* of the sequence to the output list
      output_sequences_as_lists.append(list(current_sequence)) # Store a copy of the new state
    else:
      # If no 0 is found, stop adding new lines (all zeros filled within R steps)
      break 
      
  # Format the stored sequences into strings
  output_lines = [format_sequence_to_string(seq) for seq in output_sequences_as_lists]
  
  # Join the lines with newlines for the final output
  return "\n".join(output_lines)

```