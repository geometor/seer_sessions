```python
import numpy as np
from typing import List, Union

"""
Transforms a sequence of 0s and 1s based on adjacency rules.
A 0 in the sequence is changed to a 3 if it is immediately preceded
by the sub-sequence [1, 1] OR immediately succeeded by the sub-sequence [1, 1].
All other elements remain unchanged. The input is expected to be a 
list or NumPy array of integers, and the output will be a NumPy array.
"""

def transform(input_sequence: Union[List[int], np.ndarray]) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 0s and 1s.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence, dtype=int)
    
    # Initialize the output array as a copy of the input
    output_array = np.copy(input_array)
    n = len(input_array)

    # Iterate through each element of the input sequence by index
    for i in range(n):
        # Check if the current element is 0
        if input_array[i] == 0:
            # Check condition 1: Preceded by [1, 1]
            # Ensure index i is at least 2 to check i-1 and i-2
            precedes_11 = False
            if i >= 2 and input_array[i-2] == 1 and input_array[i-1] == 1:
                precedes_11 = True

            # Check condition 2: Succeeded by [1, 1]
            # Ensure index i is at most n-3 to check i+1 and i+2
            succeeds_11 = False
            if i <= n - 3 and input_array[i+1] == 1 and input_array[i+2] == 1:
                succeeds_11 = True

            # If either condition is met, change the corresponding output element to 3
            if precedes_11 or succeeds_11:
                output_array[i] = 3

    # Return the modified output array
    return output_array
```