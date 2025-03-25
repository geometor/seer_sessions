"""
Transforms an input grid into an output grid based on the position of a vertical line of '2's.
The output grid is primarily constructed from the portion of the input grid to the left of the '2' column, and the position of 9s on the right of the same line.
"""

import numpy as np

def find_red_line(grid):
    """Finds the column index of the vertical line of '2's."""
    rows, cols = grid.shape
    for j in range(cols):
        if all(grid[i, j] == 2 for i in range(rows)):
            return j
    return -1  # Return -1 if no red line is found

def most_repeated_value(column):
    """
    Finds most repeated value, prioritizing value 9 if it is present.

    Args:
        column: A numpy array representing the column

    Returns: most repeated value or the value 9 if present.
    """
    values, counts = np.unique(column, return_counts=True)
    max_index = np.argmax(counts)
    most_repeated = values[max_index]
    if 9 in values:
        return 9
    elif most_repeated == 0 and 4 in values:
        return 4
    else:
        return most_repeated

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    red_line_col = find_red_line(input_grid)
    
    if red_line_col == -1:
        return input_grid # or perhaps raise an exception or return an empty grid

    # initialize output_grid, we'll transpose and trim later.
    output_grid = []
    
    # Process the left side of the grid, up to and including the red line.
    for j in range(red_line_col + 1):
      output_grid.append(most_repeated_value(input_grid[:, j]))

    # Find '9's on the right and insert them by order
    for j in range(red_line_col+1, cols):
      for i in range(rows):
          if input_grid[i,j] == 9:
            output_grid.append(9)
            break

    return np.array(output_grid).reshape(rows, -1)