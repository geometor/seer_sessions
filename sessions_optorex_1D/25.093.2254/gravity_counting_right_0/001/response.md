```python
import numpy as np

def parse_input(input_str):
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Formats the list of integers into a space-separated string."""
  return ' '.join(map(str, output_list))

def count_non_zeros(int_list):
  """Counts the number of non-zero elements in a list of integers."""
  count = 0
  for num in int_list:
    if num != 0:
      count += 1
  return count

def transform(input_str):
  """
  Transforms an input sequence of space-separated integers based on the count of non-zero elements.

  The transformation rule is:
  1. Count the number of non-zero elements in the input sequence (N).
  2. Determine the total length of the input sequence (L).
  3. Construct an output sequence containing N ones followed by (L - N) zeros.
  4. Return the output sequence as a space-separated string.
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)

  # Get the total length of the input list
  total_length = len(input_list)

  # Count the number of non-zero elements
  non_zero_count = count_non_zeros(input_list)

  # Calculate the number of zeros needed
  zero_count = total_length - non_zero_count

  # Construct the output list: N ones followed by (L - N) zeros
  output_list = [1] * non_zero_count + [0] * zero_count

  # Format the output list into a space-separated string
  output_str = format_output(output_list)

  return output_str

# Example usage (based on train_1):
input_example = "1 0 0 0 7 0 5 0 0 9 0 7"
output_example = transform(input_example)
print(f"Input: {input_example}")
print(f"Output: {output_example}")

# Example usage (based on train_3):
input_example_2 = "0 0 0 0 0 4 0 0 9 7 3 0"
output_example_2 = transform(input_example_2)
print(f"Input: {input_example_2}")
print(f"Output: {output_example_2}")
```