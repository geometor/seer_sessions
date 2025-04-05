```python
"""
Identify the dominant non-zero digit 'X' from the input sequence at index 4.
Construct and return a new 12-element sequence following the fixed pattern:
[0, 0, 0, 0, X, X, X, 0, X, X, 0, X].
"""

import numpy as np
import math # Include common math libraries just in case, though not needed for this specific logic

# Helper functions (not strictly necessary for this simple task, but good practice)
def get_dominant_digit(sequence):
  """Extracts the digit at index 4."""
  if len(sequence) > 4:
    return sequence[4]
  else:
    # Handle potential edge case if input is unexpectedly short
    # Based on the examples, this shouldn't happen, but defensive coding is good.
    # Returning 0 or raising an error might be options depending on requirements.
    # Let's return 0 as a default, assuming it fits the pattern logic if no X is found.
    print("Warning: Input sequence shorter than expected.")
    return 0 

def construct_target_sequence(dominant_digit):
  """Constructs the target sequence based on the dominant digit."""
  X = dominant_digit
  # Define the fixed pattern structure
  pattern_structure = [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
  return pattern_structure

def transform(input_sequence):
    """
    Transforms the input sequence based on the digit at index 4.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list of 12 integers following the pattern [0, 0, 0, 0, X, X, X, 0, X, X, 0, X],
        where X is the digit from input_sequence[4].
    """
    
    # 1. Identify the dominant non-zero digit 'X' (value at index 4)
    dominant_digit = get_dominant_digit(input_sequence)
    
    # 2. Construct the target output sequence using the fixed pattern and 'X'
    output_sequence = construct_target_sequence(dominant_digit)

    # 3. Return the newly constructed sequence
    return output_sequence

```