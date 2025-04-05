```python
import collections
import itertools
import math
import re # Use regular expression to parse the input string

"""
Transforms a sequence of integers into a binary sequence of the same length, 
where the number of 1s corresponds to the count of non-zero elements in the input.
"""

# No external libraries are strictly needed for this specific logic, 
# but including common ones for potential future iterations.
import numpy as np 

def count_non_zeros(int_list):
  """Counts the number of non-zero integers in a list."""
  count = 0
  for num in int_list:
    if num != 0:
      count += 1
  return count

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated integers into an output string 
    of space-separated 1s and 0s. The number of 1s in the output matches the 
    count of non-zero numbers in the input. The total length remains the same.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing space-separated 1s and 0s.
    """
    # 1. Receive the input sequence of integers.
    # Use regex to find all sequences of digits (handling potential multiple spaces)
    # and convert them to integers.
    input_numbers = [int(x) for x in re.findall(r'\d+', input_str)]
    
    # 2. Count how many numbers in the input sequence are not zero.
    non_zero_count = count_non_zeros(input_numbers)
    
    # 3. Determine the total length of the input sequence.
    total_length = len(input_numbers)
    
    # 4. Generate an output sequence consisting of N ones followed by L - N zeros.
    # Calculate the number of zeros needed.
    zero_count = total_length - non_zero_count
    
    # Create the output list.
    output_numbers = [1] * non_zero_count + [0] * zero_count
    
    # 5. Format the generated sequence as a space-separated string for the final output.
    output_str = " ".join(map(str, output_numbers))
    
    return output_str

```