import math

def parse_input_string(input_str: str) -> list[int]:
  """Parses a space-separated string of integers into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output_list(int_list: list[int]) -> str:
  """Formats a list of integers into a space-separated string."""
  return " ".join(map(str, int_list))

def find_first_zero_index(int_list: list[int]) -> int | None:
  """Finds the index of the first zero in the list. Returns None if not found."""
  try:
    return int_list.index(0)
  except ValueError:
    return None

def transform(input_str: str) -> str:
  """
  Transforms an input string representing a sequence of integers according to the following rule:
  1. The first line of the output is the input sequence itself.
  2. Subsequent lines are generated iteratively by replacing the leftmost '0'
     with the first digit of the original sequence.
  3. The number of replacement steps (R) performed is calculated as ceil(L / 3),
     where L is the length of the sequence. The total number of output lines is R + 1.
  """
  # 1. Read the input string and parse it into a list of integers
  current_sequence = parse_input_string(input_str)
  
  # 2. Determine the total length L of current_sequence
  L = len(current_sequence)
  if L == 0:
      return "" # Handle empty input case

  # 3. Calculate the number of replacement steps R
  # R = math.ceil(L / 3) # equivalent using integer division
  R = (L + 2) // 3 
  
  # 4. Identify the fill_digit (first element)
  fill_digit = current_sequence[0]
  
  # 5. Initialize a list to store the output sequences (as lists of integers)
  output_sequences = []
  
  # 6. Add the initial sequence to the output list
  output_sequences.append(list(current_sequence)) # Store a copy

  # 7. Repeat the replacement R times
  for _ in range(R):
    # a. Find the index of the first occurrence of 0 in the current_sequence
    index_zero = find_first_zero_index(current_sequence)
    
    # b. If a 0 is found
    if index_zero is not None:
      # i. Create a copy (important!)
      next_sequence = list(current_sequence) 
      # ii. Update the element at index_zero
      next_sequence[index_zero] = fill_digit
      # iii. Set current_sequence to this updated sequence for the next iteration
      current_sequence = next_sequence
      # iv. Add the new sequence to the output list
      output_sequences.append(current_sequence)
    else:
      # c. If no 0 is found, stop adding new lines (all zeros filled)
      break 
      
  # 8. Format the stored sequences into strings and join with newlines
  output_lines = [format_output_list(seq) for seq in output_sequences]
  return "\n".join(output_lines)

# Example usage (based on train_1):
# input_string = "8 8 8 8 0 0"
# output_string = transform(input_string)
# print(output_string)
# Expected Output:
# 8 8 8 8 0 0
# 8 8 8 8 8 0
# 8 8 8 8 8 8

# Example usage (based on train_2):
# input_string = "2 0 0 0 0 0 0 0"
# output_string = transform(input_string)
# print(output_string)
# Expected Output:
# 2 0 0 0 0 0 0 0
# 2 2 0 0 0 0 0 0
# 2 2 2 0 0 0 0 0
# 2 2 2 2 0 0 0 0