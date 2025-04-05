import collections
import math  # Available, but not used in this specific solution
import numpy as np # Available, but not used in this specific solution

"""
Transforms an input sequence of digits by identifying contiguous subsequences (islands) 
of non-zero digits. Within each island, it finds the most frequently occurring 
digit (the dominant digit). All digits within that island in the input sequence 
are then replaced by this dominant digit in the output sequence. Zero digits act 
as separators between islands and remain unchanged in the output.
"""

def find_dominant_digit(island_digits):
  """
  Finds the most frequent digit in a list of non-zero digits.
  If there's a tie, the behavior might depend on the underlying Counter implementation,
  but based on examples, a single dominant digit seems expected.
  
  Args:
    island_digits: A list of integers representing the digits in an island.

  Returns:
    The integer digit that appears most frequently in the list. Returns None if 
    the list is empty (though this shouldn't happen with valid islands).
  """
  if not island_digits:
    return None 
  # Count occurrences of each digit
  counts = collections.Counter(island_digits)
  # Find the digit with the highest count. most_common(1) returns a list like [ (digit, count) ]
  dominant_digit = counts.most_common(1)[0][0]
  return dominant_digit

def transform(input_str: str) -> str:
    """
    Applies the island dominance transformation to the input string sequence.

    Args:
      input_str: A string of space-separated digits.

    Returns:
      A string of space-separated digits representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers.
    input_digits = [int(d) for d in input_str.split()]
    n = len(input_digits)
    # Initialize the output sequence as a copy of the input. 
    # This ensures zeros are preserved unless overwritten by an island rule.
    output_digits = list(input_digits) 

    # 2. Iterate through the input sequence to identify islands.
    i = 0
    while i < n:
      # Check if the current digit is non-zero, indicating a potential start of an island.
      if input_digits[i] != 0:
        start_index = i
        current_island_digits = []
        # 3. Find the extent of the current island (all consecutive non-zero digits).
        while i < n and input_digits[i] != 0:
          current_island_digits.append(input_digits[i])
          i += 1
        # The loop exits when a zero is found or the end of the sequence is reached.
        # The last non-zero digit was at index i-1.
        end_index = i - 1 

        # 4a. Determine the dominant digit for the identified island.
        dominant_digit = find_dominant_digit(current_island_digits)

        # 4c. Update the output sequence: Replace all digits in the island's range
        #     with the dominant digit.
        for j in range(start_index, end_index + 1):
          output_digits[j] = dominant_digit
      else:
        # 5. If the current digit is zero, it's a separator. 
        #    It's already correctly placed in output_digits (initialized as a copy).
        #    Simply move to the next position.
        i += 1

    # 6. Join the digits in the output sequence back into a space-separated string.
    output_str = " ".join(map(str, output_digits))
    return output_str
