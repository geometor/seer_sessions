```python
"""
Transforms a 1-dimensional NumPy array of integers by moving the first element 
to the end of the array, effectively performing a single left rotation.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Rotates the input 1D NumPy array one position to the left.

    1. Receive the input as a 1-dimensional NumPy array of integers.
    2. Extract the first element (at index 0) of the input array.
    3. Create a new array containing all elements from the input array 
       starting from the second element (index 1) to the end.
    4. Construct the output array by appending the extracted first element 
       to the end of the new array created in the previous step.
    5. Return the resulting NumPy array.
    """

    # Handle empty or single-element arrays (rotation has no effect or is trivial)
    if input_grid.size <= 1:
        return input_grid.copy() # Return a copy to avoid modifying the original

    # Extract the first element
    first_element = input_grid[0]

    # Extract the remaining elements (from index 1 onwards)
    remaining_elements = input_grid[1:]

    # Construct the output array by concatenating the remaining elements
    # with the first element appended. Note: np.append returns a *new* array.
    # Need to put the element to append in a list or array for concatenation.
    output_grid = np.append(remaining_elements, [first_element])

    return output_grid
```