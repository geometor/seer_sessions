```python
"""
Transforms a 1D NumPy array of digits (0, 1, 2) by sorting its elements 
according to the specific order: all 2s first, followed by all 0s, 
then all 1s. The counts of each digit are preserved from the input 
to the output.
"""

import numpy as np

# Helper function to count specific values in a NumPy array
def count_value(arr: np.ndarray, value: int) -> int:
    """Counts the occurrences of a specific value in a NumPy array."""
    # Use np.sum with a boolean comparison for efficient counting
    return np.sum(arr == value)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the 2 > 0 > 1 sorting rule to the input NumPy array of digits.

    Args:
        input_grid: A 1D NumPy array containing integers (0, 1, or 2).

    Returns:
        A 1D NumPy array containing the sorted digits.
    """

    # 1. Count the number of times 2, 0, and 1 appear in the input array.
    count_2 = count_value(input_grid, 2)
    count_0 = count_value(input_grid, 0)
    count_1 = count_value(input_grid, 1)

    # 2. Construct the output sequence using the counts and the desired order (2, 0, 1).
    # Create lists/arrays for each number based on counts.
    output_part_2 = np.full(count_2, 2, dtype=input_grid.dtype)
    output_part_0 = np.full(count_0, 0, dtype=input_grid.dtype)
    output_part_1 = np.full(count_1, 1, dtype=input_grid.dtype)

    # 3. Concatenate the parts to form the final output array.
    output_grid = np.concatenate((output_part_2, output_part_0, output_part_1))

    # 4. Return the constructed output array.
    return output_grid
```