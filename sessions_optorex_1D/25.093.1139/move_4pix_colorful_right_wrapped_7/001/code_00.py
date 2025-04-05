import collections

def parse_input_sequence(input_str):
  """Converts a space-separated string of digits into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output_sequence(sequence):
  """Converts a list of integers into a space-separated string."""
  return ' '.join(map(str, sequence))

def split_sequence(sequence, split_index):
  """Splits a sequence into two parts at the given index."""
  if split_index < 0 or split_index > len(sequence):
      raise ValueError("Split index out of bounds")
  first_part = sequence[:split_index]
  second_part = sequence[split_index:]
  return first_part, second_part

def concatenate_sequences(seq1, seq2):
  """Concatenates two sequences."""
  return seq1 + seq2

def transform(input_str):
  """
  Transforms the input sequence by moving the last 4 elements to the 
  beginning and keeping the first 8 elements after them.
  
  1. Take the input sequence of 12 digits.
  2. Identify the last 4 digits of the input sequence.
  3. Identify the first 8 digits of the input sequence.
  4. Construct the output sequence by placing the identified last 4 digits 
     at the beginning, followed immediately by the identified first 8 digits.
  """
  # Parse the input string into a list of integers
  input_sequence = parse_input_sequence(input_str)
  
  # Define the split point (after the first 8 elements)
  split_point = 8
  
  # Split the sequence into the first 8 and last 4 elements
  # Note: The natural language program describes identifying the last 4 first,
  # but splitting at index 8 achieves the same segments.
  first_segment, second_segment = split_sequence(input_sequence, split_point)
  
  # Concatenate the segments in the specified order: last 4 then first 8
  output_sequence_list = concatenate_sequences(second_segment, first_segment)
  
  # Format the resulting list back into a space-separated string
  output_str = format_output_sequence(output_sequence_list)
  
  return output_str
