"""
Transforms an input NumPy array of digits (0, 1, 2) by sorting them according to a specific order: 
all 2s first, followed by all 0s, then all 1s. The counts of each digit are preserved 
from the input to the output. The output is also a NumPy array.
"""

import numpy as np
import collections

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the 2 > 0 > 1 sorting rule to the input NumPy array of digits.

    Args:
        input_grid: A NumPy array containing integers (0, 1, or 2).

    Returns:
        A NumPy array containing the sorted digits.
    """

    # 1. Count the occurrences of each digit (0, 1, 2) in the input array.
    # The input is already a sequence of numbers (NumPy array), so no parsing is needed.
    counts = collections.Counter(input_grid)
    count_2 = counts.get(2, 0)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)

    # 2. Create a new list to build the output sequence.
    # Initialize an empty list.
    output_list = []

    # 3. Append the integer 2 to the output list based on its count.
    output_list.extend([2] * count_2)

    # 4. Append the integer 0 to the output list based on its count.
    output_list.extend([0] * count_0)

    # 5. Append the integer 1 to the output list based on its count.
    output_list.extend([1] * count_1)

    # 6. Convert the constructed list into a NumPy array.
    output_grid = np.array(output_list, dtype=input_grid.dtype) # Preserve original dtype if needed

    # 7. Return the final sorted NumPy array.
    return output_grid
