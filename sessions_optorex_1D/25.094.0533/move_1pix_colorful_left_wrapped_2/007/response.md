```python
"""
Conditionally transforms a 1D NumPy array of digits based on its first element.
If the first element is non-zero, performs a left cyclic shift (moves the first element to the end).
If the first element is zero, removes the first occurrence of zero from the array and appends a zero to the end.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a conditional transformation to the input 1D NumPy array.

    Args:
        input_grid: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array representing the transformed sequence.
    """

    # Handle edge cases where no transformation is possible or needed.
    if input_grid.size <= 1:
        return input_grid.copy()

    # 1. Read the input sequence (NumPy array). (Implicit via argument)
    # 2. Examine the first digit (at index 0) of the sequence.
    first_element = input_grid[0]

    # 3. If the first digit is *not* zero:
    if first_element != 0:
        # a. Store the first digit. (already stored in first_element)
        # b. Create a new sequence containing all digits from the second position to the end.
        remaining_elements = input_grid[1:]
        # c. Append the stored first digit to the end of this new sequence.
        output_grid = np.concatenate((remaining_elements, [first_element]))

    # 4. Else (if the first digit *is* zero):
    else:
        # a. Find the index of the *first* occurrence of the digit '0' in the sequence.
        # np.where returns a tuple of arrays; for a 1D array, we take the first element of the tuple,
        # and then the first index from that array.
        try:
            zero_indices = np.where(input_grid == 0)[0]
            if len(zero_indices) > 0:
                 first_zero_index = zero_indices[0]
                 # b. Create a new sequence by removing the digit at that found index.
                 grid_without_first_zero = np.delete(input_grid, first_zero_index)
                 # c. Append the digit '0' to the end of this modified sequence.
                 output_grid = np.append(grid_without_first_zero, 0)
            else:
                 # This case shouldn't happen based on the logic (first element is 0),
                 # but handle defensively: return the original grid if no zero found.
                 output_grid = input_grid.copy()

        except IndexError:
             # This handles the case where np.where(input_grid == 0)[0] is empty,
             # which again, shouldn't happen if input_grid[0] == 0, but is safe to include.
             output_grid = input_grid.copy()


    # 5. Output the resulting sequence.
    return output_grid
```