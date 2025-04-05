import collections

def parse_input(input_str):
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.strip().split()]

def format_output(output_list):
  """Formats the list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str):
  """
  Sorts a sequence of space-separated integers (0, 1, 2) in non-decreasing order.
  """
  # Parse the input string into a list of integers
  int_list = parse_input(input_str)

  # Sort the list of integers in ascending order
  int_list.sort()

  # Format the sorted list back into a space-separated string
  output_str = format_output(int_list)

  # Return the sorted string
  return output_str
