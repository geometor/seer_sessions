```python
import re

"""
Insert a '0' digit into the input sequence immediately before the first non-zero digit.
"""

def find_first_non_zero_index(sequence):
  """
  Finds the index of the first non-zero digit in a sequence.

  Args:
    sequence: A list of integers or strings representing digits.

  Returns:
    The index of the first non-zero digit, or the length of the sequence 
    if all digits are zero (although this case doesn't appear in examples).
    Returns 0 if the sequence is empty.
  """
  if not sequence:
      return 0
      
  for i, digit in enumerate(sequence):
    # Convert to int for comparison, handling potential string input
    if int(digit) != 0:
      return i
  # If no non-zero digit is found, return the length (insertion at the end)
  # Based on the examples, there's always a non-zero digit,
  # so insertion should occur *before* it. If all were zero, 
  # inserting at index 0 seems most consistent with the pattern of
  # pushing digits right. Let's default to index 0 if only zeros are found,
  # though the provided examples don't cover this. Reconsidering the rule:
  # "before the first non-zero digit". If none exists, the most logical place
  # based on shifting is before the *first* digit regardless, which is index 0.
  # However, let's stick strictly to the rule observed: find the first non-zero.
  # If none exists, the rule isn't directly applicable. Let's return the index 
  # where the first non-zero *would* be if it existed, matching its position.
  # In the all-zero case, this still points logically to index 0 for consistency.
  # Let's refine: Find the first element > 0. If found, return its index.
  # If not found (all zeros or empty), return 0.
  for i, digit in enumerate(sequence):
      if int(digit) > 0:
          return i
  return 0 # Default index if no non-zero digit found or sequence is empty

def transform(input_str):
    """
    Transforms the input string of digits by inserting a '0' before the first non-zero digit.

    Args:
      input_str: A string containing space-separated single digits.

    Returns:
      A string containing space-separated single digits with a '0' inserted.
    """
    # Parse the input string into a list of digit strings
    # Use regex to handle potentially variable spacing
    input_digits = re.findall(r'\d', input_str) 
    
    # Find the index where the '0' should be inserted
    insertion_index = find_first_non_zero_index(input_digits)

    # Create the output list by inserting '0'
    # Make a copy to avoid modifying the original list if it's needed elsewhere
    output_digits = list(input_digits) 
    output_digits.insert(insertion_index, '0')

    # Join the list back into a space-separated string
    output_str = " ".join(output_digits)

    return output_str
```