import numpy as np

"""
Locates the cells containing '7' and '4' in the input grid. 
In the output grid, the cell that originally contained '7' is changed to '1', 
and the cell that originally contained '4' is changed to '7'. 
All other cells remain unchanged.
"""

def find_value(grid, value):
  """
  Finds the coordinates (row, column) of the first occurrence of a given value in the grid.

  Args:
    grid: A numpy array representing the grid.
    value: The integer value to search for.

  Returns:
    A tuple (row, column) if the value is found, otherwise None.
  """
  coords = np.argwhere(grid == value)
  if len(coords) > 0:
    return tuple(coords[0]) # Return the coordinates of the first instance
  return None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid_np)

    # Find the location of the value 7
    location_of_seven = find_value(input_grid_np, 7)

    # Find the location of the value 4
    location_of_four = find_value(input_grid_np, 4)

    # Check if both values were found before attempting modification
    if location_of_seven is not None and location_of_four is not None:
        # Change the value at the original location of 7 to 1 in the output grid
        output_grid[location_of_seven] = 1

        # Change the value at the original location of 4 to 7 in the output grid
        output_grid[location_of_four] = 7
    # If either 7 or 4 is not found, the output grid remains a copy of the input.
    # This handles cases where the required numbers might be missing, although the
    # provided examples always contain them.

    return output_grid
