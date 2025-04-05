# tool_code
import numpy as np

def parse_input(input_str):
  """Converts the space-separated string to a list of integers."""
  return [int(x) for x in input_str.split()]

def find_block_metrics(grid_list):
  """Finds start, length, and value of the first non-zero block."""
  start_index = -1
  length = 0
  value = 0
  in_block = False
  for i, element in enumerate(grid_list):
    if element != 0 and not in_block:
      start_index = i
      value = element
      length = 1
      in_block = True
    elif element == value and in_block:
      length += 1
    elif element != value and in_block:
      break # End of block
  return start_index, length, value

def calculate_expected_output(input_str):
    """Calculates metrics and expected output list."""
    input_list = parse_input(input_str)
    start, length, value = find_block_metrics(input_list)
    if start == -1: # No block found
        return {'input': input_list, 'start': -1, 'length': 0, 'value': 0, 'new_start': -1, 'expected_output': [0]*len(input_list)}

    new_start = start - length
    output_list = [0] * len(input_list)
    # Ensure indices are valid before slicing/assignment
    if new_start >= 0 and new_start + length <= len(output_list):
        output_list[new_start : new_start + length] = [value] * length
    elif new_start < 0: # Handle shift past the beginning (though not seen in examples)
        effective_length = length + new_start # new_start is negative
        if effective_length > 0:
             output_list[0 : effective_length] = [value] * effective_length
    # If new_start is valid but block goes past end (not seen in examples)
    # The initial slicing output_list[new_start : new_start + length] handles truncation implicitly if needed.

    return {'input': input_list, 'start': start, 'length': length, 'value': value, 'new_start': new_start, 'expected_output': output_list}

# --- Training Data ---
train_inputs = [
    "0 0 0 0 0 0 6 6 6 0 0 0",
    "0 0 9 9 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 8 8 8 8",
    "0 0 0 3 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 2 2 0 0 0",
    "0 0 0 0 0 0 0 0 5 0 0 0",
    "0 0 0 0 0 0 6 6 6 6 6 0",
]

train_outputs = [
    "0 0 0 6 6 6 0 0 0 0 0 0",
    "9 9 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 8 8 8 8 0 0 0 0",
    "0 0 3 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 2 2 0 0 0 0 0",
    "0 0 0 0 0 0 0 5 0 0 0 0",
    "0 6 6 6 6 6 0 0 0 0 0 0",
]

metrics = []
for i, input_str in enumerate(train_inputs):
    result = calculate_expected_output(input_str)
    result['provided_output'] = parse_input(train_outputs[i])
    result['match'] = (result['expected_output'] == result['provided_output'])
    metrics.append(result)

# Print metrics in a readable format
for i, m in enumerate(metrics):
    print(f"--- Example {i+1} ---")
    print(f"Input: {m['input']}")
    print(f"Block: start={m['start']}, length={m['length']}, value={m['value']}")
    print(f"Calculation: new_start = {m['start']} - {m['length']} = {m['new_start']}")
    print(f"Expected Output: {m['expected_output']}")
    print(f"Provided Output: {m['provided_output']}")
    print(f"Match: {m['match']}")
    print("-" * 15)
