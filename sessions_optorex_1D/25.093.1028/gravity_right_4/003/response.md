```python
import numpy as np  # Import numpy, anticipating potential array inputs

"""
Rearranges a sequence of integers by moving all zero elements to the beginning 
of the sequence while preserving the relative order of the non-zero elements.
"""

def get_zeros(sequence):
  """Extracts all zero elements from the sequence."""
  return [element for element in sequence if element == 0]

def get_non_zeros(sequence):
  """Extracts all non-zero elements from the sequence, preserving relative order."""
  return [element for element in sequence if element != 0]

def transform(input_sequence: list[int] | np.ndarray) -> list[int]:
    """
    Moves all zero elements to the front of a sequence (list or 1D NumPy array) 
    of integers, preserving the relative order of non-zero elements.

    Args:
        input_sequence: A list or 1D NumPy array of integers.

    Returns:
        A new list with zeros moved to the front.
    """
    
    # 1. Extract all zero elements from the input sequence.
    #    The number of zeros determines the length of the leading zero block.
    zeros_list = get_zeros(input_sequence)
    
    # 2. Extract all non-zero elements, maintaining their original relative order.
    #    This sequence will form the trailing block in the output.
    non_zeros_list = get_non_zeros(input_sequence)
    
    # 3. Concatenate the list of zeros and the list of non-zeros.
    #    The zeros come first, followed by the non-zeros in their preserved order.
    output_sequence = zeros_list + non_zeros_list
    
    # 4. Return the resulting rearranged sequence.
    return output_sequence

```