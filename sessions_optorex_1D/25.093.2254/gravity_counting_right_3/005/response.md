```python
import numpy as np
import math

"""
Transforms an input sequence of integers into a binary sequence (1s and 0s) of the same length. 
The number of 1s in the output equals the count of non-zero integers in the input, 
with 1s appearing first, followed by 0s to fill the remaining length.
"""

def count_non_zeros(sequence):
  """Counts the number of non-zero integers in a sequence (list or array)."""
  count = 0
  for element in sequence:
    # Check if the element is not equal to zero
    if element != 0:
      count += 1
  return count

def transform(input_sequence):
    """
    Transforms an input sequence of integers based on the count of non-zero elements.

    Args:
        input_sequence: A list or numpy array of integers. 
                         (Parameter name 'input_grid' kept for template consistency, 
                          but it represents a 1D sequence in this task).

    Returns:
        A list of integers containing 1s followed by 0s.
    """
    
    # 1. Ensure input is usable as a sequence (e.g., convert NumPy array to list if needed, 
    #    though direct iteration often works). For simplicity, we can work directly if it's iterable.
    #    If the input is guaranteed to be list or np.ndarray, direct iteration is fine.
    
    # 2. Determine the total number of elements in the input sequence.
    sequence_length = len(input_sequence)
    
    # 3. Count the number of elements that are not equal to zero using a helper function.
    non_zero_count = count_non_zeros(input_sequence)
    
    # 4. Calculate the number of zeros needed.
    zero_count = sequence_length - non_zero_count
    
    # 5. Create the output sequence: N ones followed by Z zeros.
    # Using list multiplication for concise construction.
    output_sequence = [1] * non_zero_count + [0] * zero_count
    
    # 6. Return the generated output sequence.
    return output_sequence

```