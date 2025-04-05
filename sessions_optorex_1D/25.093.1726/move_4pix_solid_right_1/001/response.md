```python
"""
Identifies all non-zero elements (objects) in the input sequence.
Creates a new output sequence of the same length, initially filled with zeros.
For each non-zero element found at index `i` in the input, places that element's 
value into the output sequence at index `i + 4`, provided the new index is 
within the bounds of the sequence. The relative order of non-zero elements is preserved.
"""

import numpy as np # Although not strictly necessary for this list-based approach,
                   # numpy could be useful for more complex grid manipulations.

# No specific helper functions needed for this simple shift,
# but could be added for modularity (e.g., find_objects, shift_object).

def transform(input_grid: list[int]) -> list[int]:
    """
    Shifts all non-zero elements in the input list 4 positions to the right.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A new list of integers with non-zero elements shifted 4 positions right.
    """
    # Get the length of the input grid
    grid_length = len(input_grid)

    # Initialize the output grid with zeros, having the same length as the input
    output_grid = [0] * grid_length

    # Iterate through the input grid with index and value
    for i, val in enumerate(input_grid):
        # Check if the current element is non-zero (an object)
        if val != 0:
            # Calculate the new index by adding the shift amount (4)
            new_index = i + 4
            # Check if the new index is within the bounds of the grid
            if 0 <= new_index < grid_length:
                # Place the non-zero value at the new position in the output grid
                output_grid[new_index] = val

    # Return the transformed grid
    return output_grid

```