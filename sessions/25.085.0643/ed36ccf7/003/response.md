```python
"""
Rotate the input grid 90 degrees counter-clockwise.
"""

import copy
import numpy as np # Using numpy for convenience, but can be done with nested loops too.

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The rotated grid.
    """
    # Convert the input list of lists to a numpy array for easier rotation
    np_grid = np.array(input_grid, dtype=int)

    # Handle empty grid case
    if np_grid.size == 0:
        # If input is completely empty [], return []
        if len(input_grid) == 0:
             return []
        # If input is like [[]], return [[]]
        elif len(input_grid[0]) == 0:
             # The output should have dimensions swapped, 
             # so if input is Hx0, output is 0xH.
             # np.rot90 handles this correctly returning an empty array of shape (0, H)
             # but we need to return a list of lists.
             # Since width is 0, the new height is 0. Output is []
             return []
        # This case shouldn't happen based on ARC constraints (1x1 min) but good to consider
        else:
            return [] # Or raise an error

    # Perform the 90-degree counter-clockwise rotation using numpy.rot90
    # k=1 specifies one counter-clockwise rotation.
    rotated_grid_np = np.rot90(np_grid, k=1)

    # Convert the resulting numpy array back to a list of lists
    output_grid = rotated_grid_np.tolist()

    return output_grid

# Example usage with manual calculation for verification:
# Input:
# [[0, 0, 9],
#  [0, 0, 9],
#  [9, 9, 9]]
# H=3, W=3
# (r=0, c=0) value 0 -> (new_r = 3-1-0=2, new_c = 0) -> output[2][0] = 0
# (r=0, c=1) value 0 -> (new_r = 3-1-1=1, new_c = 0) -> output[1][0] = 0
# (r=0, c=2) value 9 -> (new_r = 3-1-2=0, new_c = 0) -> output[0][0] = 9
# (r=1, c=0) value 0 -> (new_r = 3-1-0=2, new_c = 1) -> output[2][1] = 0
# (r=1, c=1) value 0 -> (new_r = 3-1-1=1, new_c = 1) -> output[1][1] = 0
# (r=1, c=2) value 9 -> (new_r = 3-1-2=0, new_c = 1) -> output[0][1] = 9
# (r=2, c=0) value 9 -> (new_r = 3-1-0=2, new_c = 2) -> output[2][2] = 9
# (r=2, c=1) value 9 -> (new_r = 3-1-1=1, new_c = 2) -> output[1][2] = 9
# (r=2, c=2) value 9 -> (new_r = 3-1-2=0, new_c = 2) -> output[0][2] = 9
# Output:
# [[9, 9, 9],
#  [0, 0, 9],
#  [0, 0, 9]] - Matches expected output for Example 1.

```