```python
import numpy as np
import collections

"""
Transforms a sequence of 12 integers by counting the non-zero elements 
and creating an output sequence of 12 integers with that many '1's 
grouped at the end, preceded by '0's.
"""

def count_non_zero(input_list):
  """Counts the number of non-zero elements in a list or array."""
  return np.count_nonzero(input_list)

def transform(input_sequence):
    """
    Transforms an input sequence (list or array) of 12 integers based 
    on the count of non-zero elements.

    Args:
        input_sequence: A list or numpy array containing 12 integers.

    Returns:
        list: A list of 12 integers (0s and 1s) where the number of 1s
              equals the count of non-zero elements in the input, and the
              1s are grouped at the end of the list.
    """
    # Ensure input is treated as a list or array-like structure
    # (No need for explicit conversion if numpy array is passed)
    
    # Determine the length of the sequence
    sequence_length = len(input_sequence)
    
    # Count the non-zero elements in the input sequence
    non_zero_count = count_non_zero(input_sequence)

    # Calculate the number of zeros needed at the beginning
    zero_count = sequence_length - non_zero_count

    # Create the output list: sequence_length - non_zero_count zeros followed by non_zero_count ones
    output_list = [0] * zero_count + [1] * non_zero_count
        
    return output_list
```