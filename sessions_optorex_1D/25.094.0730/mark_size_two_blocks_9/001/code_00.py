import re

def parse_input(input_str):
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.strip().split()]

def format_output(output_list):
  """Formats the list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str):
  """
  Transforms the input sequence by changing 0s adjacent to blocks of exactly two 1s to 3s.
  1. Iterate through the input sequence to find blocks of exactly two 1s ('1 1').
  2. For each '1 1' block found:
     a. Check the element immediately before the block. If it's a 0, change it to 3 in the output.
     b. Check the element immediately after the block. If it's a 0, change it to 3 in the output.
  3. Keep all other elements (1s and 0s not adjacent to '1 1' blocks) the same.
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)
  n = len(input_list)
  
  # Initialize output_list as a copy of input_list
  output_list = list(input_list)

  # Iterate through the list to find blocks of '1 1'
  # We only need to check up to n-2 because we need pairs input_list[i] and input_list[i+1]
  for i in range(n - 1):
      # Check if the current element and the next element form a '1 1' block
      if input_list[i] == 1 and input_list[i+1] == 1:
          # Ensure it's *exactly* two 1s. 
          # Check before the block
          is_start_of_block = (i == 0 or input_list[i-1] != 1)
          # Check after the block
          is_end_of_block = (i + 2 >= n or input_list[i+2] != 1)

          if is_start_of_block and is_end_of_block:
              # Modify the element *before* the block if it's a 0 and within bounds
              if i > 0 and input_list[i-1] == 0:
                  output_list[i-1] = 3
              
              # Modify the element *after* the block if it's a 0 and within bounds
              if i + 2 < n and input_list[i+2] == 0:
                  output_list[i+2] = 3

  # Format the output list back into a string
  return format_output(output_list)
