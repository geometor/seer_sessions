```python
"""
Find the lowest, right-most 2. If there is a zero diagonally below and to the right, change the zero to a one. Otherwise, change the two to a one.
"""

import numpy as np

def find_lower_rightmost_two(grid):
    # Find the indices of all '2's
    two_indices = np.argwhere(grid == 2)

    # If no '2's are found, return None
    if len(two_indices) == 0:
        return None

    # Find the lowest row index
    lowest_row = np.max(two_indices[:, 0])

    # Filter '2's that are in the lowest row
    lowest_twos = two_indices[two_indices[:, 0] == lowest_row]
    
    # Find rightmost column
    rightmost_column = np.max(lowest_twos[:,1])
    
    # Filter for rightmost two
    rightmost_twos = lowest_twos[lowest_twos[:,1] == rightmost_column]

    # Return the coordinates of the lower-rightmost '2'
    return tuple(rightmost_twos[0])

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the lower-rightmost '2'
    target_coords = find_lower_rightmost_two(output_grid)

    # If no '2' is found, return the original grid
    if target_coords is None:
        return output_grid

    row, col = target_coords

    # Check for '0' diagonally down and to the right
    if row + 1 < rows and col + 1 < cols and output_grid[row + 1, col + 1] == 0:
        output_grid[row + 1, col + 1] = 1
    elif col + 1 < cols and output_grid[row,col+1] == 0:
        output_grid[row,col+1] = 1
    else:
        # Otherwise, replace the '2' with '1'
        output_grid[row, col] = 1

    return output_grid
```