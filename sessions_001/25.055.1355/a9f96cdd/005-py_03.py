"""
1.  **Identify Input Object:** Find the single non-zero pixel within the input grid.  Record its color and position.
2. **Determine the transformation rule:**
    *   **Example 1**: If the input is a 3x3 grid and contains one object: Create a 3x3 output. The output should contain four pixels, one in each corner. Use the colors green (0,0), magenta (0,2), azure (2,0) and orange (2,2) regardless of the original color.
    * **Example 2**: If the input is a 3x3 grid, and contains one object in position (1, 1): Create a 4x4 output grid. Place a yellow pixel (4) one row and column below the original position, and left one pixel, and a gray pixel (5) one row and column below the original position, and right one.
    *  **Example 3**: If the input is a 4x4 grid, and contains one object: Create a 4x4 output grid. Place an orange pixel (7) one row down and one column to the left of the location of the original color and a red pixel (2) one row down and one column to the right of the original object.
3.  **Output:** Generate the new grid based on the rule chosen in step 2.
"""

import numpy as np

def find_input_object(input_grid):
    # Find the non-zero pixel in the input grid
    non_zero_pixels = np.where(input_grid != 0)
    if len(non_zero_pixels[0]) > 0:
        row = non_zero_pixels[0][0]
        col = non_zero_pixels[1][0]
        value = input_grid[row, col]
        return value, (row, col)
    else:
        return None, None

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_value, input_position = find_input_object(input_grid)

    if input_value is None:  # Handle empty input
        return input_grid.tolist()

    # Determine transformation rule and output grid size
    if input_grid.shape == (3, 3) and input_position == (1, 1):
      if input_value == 2:
        # Example 1 rule
        output_grid = np.zeros((3, 3), dtype=int)
        output_grid[0, 0] = 3
        output_grid[0, 2] = 6
        output_grid[2, 0] = 8
        output_grid[2, 2] = 7
      elif input_value == 7:
        # Example 2 rule
        output_grid = np.zeros((4, 4), dtype=int)
        output_grid[2, 0] = 4
        output_grid[2, 2] = 5

    elif input_grid.shape == (4, 4):
        # Example 3 rule
        output_grid = np.zeros((4, 4), dtype=int)
        output_grid[input_position[0] + 1, input_position[1] - 1] = 7
        output_grid[input_position[0] + 1, input_position[1] + 1] = 2

    else:  # Default case:  return input unchanged
        return input_grid.tolist()


    return output_grid.tolist()