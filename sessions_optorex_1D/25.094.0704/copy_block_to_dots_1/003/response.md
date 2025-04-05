```python
"""
Transforms an input sequence (1D NumPy array of integers) by identifying patterns where a non-zero digit 'X' is surrounded by zeros ('[0, X, 0]') and replacing the adjacent zeros with 'X' in the output array to form '[X, X, X]'. Elements not part of such a pattern are copied unchanged from input to output.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the '[0, X, 0]' to '[X, X, X]' transformation rule to a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers representing the input sequence.

    Returns:
        A 1D NumPy array of integers representing the transformed sequence.
    """
    # 1. Get the length of the input array.
    n = len(input_grid)

    # 2. Create a copy of the input array to serve as the basis for the output array.
    #    This ensures modifications don't affect the checking conditions based on the original input.
    output_grid = np.copy(input_grid)

    # 3. Iterate through the input array from the second element (index 1)
    #    up to the second-to-last element (index n - 2). We need to check neighbors.
    for i in range(1, n - 1):
        # 4. For each element at index i:
        #    a. Get the value of the element at index i in the *input* array.
        center_val = input_grid[i]
        #    b. Get the value of the element at index i-1 in the *input* array.
        left_val = input_grid[i-1]
        #    c. Get the value of the element at index i+1 in the *input* array.
        right_val = input_grid[i+1]

        #    d. Check if the pattern [0, X, 0] exists (X is non-zero).
        if center_val != 0 and left_val == 0 and right_val == 0:
            # e. If the pattern is found, update the elements at indices i-1 and i+1
            #    in the *output* array to the value of the center element (X).
            output_grid[i-1] = center_val
            output_grid[i+1] = center_val
            # The element at index i (center_val) is already correct in the copy.

    # 5. Return the modified output array.
    return output_grid
```