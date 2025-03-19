"""
1.  **Identify the Blue Object:** Locate the contiguous blue (1) rectangle within the input grid. Note its dimensions (height and width) and its top-left corner's position.
2.  **Determine Added Rows:** Calculate the difference in the number of rows between the output grid and the input grid.
3.  **Create Red Background:** Create a red (2) rectangle. The height will equal to the number of rows added. The width of the red rectangle is the same as the width of the input grid.
4. **Append Red Background:** Place the generated red block below the original input.
"""

import numpy as np

def find_blue_rectangle(grid):
    blue_positions = np.argwhere(grid == 1)
    if blue_positions.size == 0:
        return None, None, None, None  # No blue rectangle found

    min_row = np.min(blue_positions[:, 0])
    max_row = np.max(blue_positions[:, 0])
    min_col = np.min(blue_positions[:, 1])
    max_col = np.max(blue_positions[:, 1])

    height = max_row - min_row + 1
    width = max_col - min_col + 1
    top_left = (min_row, min_col)

    return height, width, top_left

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the Blue Object
    blue_height, blue_width, blue_top_left = find_blue_rectangle(input_grid)

    # If no blue rectangle is found, return the original grid (or handle as needed)
    if blue_height is None:
        return input_grid

    # 2. Determine Added Rows (This step isn't strictly necessary here,
    #    but it's kept for consistency with the NLP and in case we need
    #    to validate against the output grid in the future).
    # For this implementation, we'll directly calculate the added rows based
    # on the examples.  The examples show a consistent relationship
    # between blue rectangle's height and added rows.
    if blue_height>0:
      added_rows = blue_height * 2
    else:
      added_rows = 0

    # 3. Create Red Background and Append
    output_grid = input_grid.copy()

    if added_rows > 0:
      red_block = np.full((added_rows, input_grid.shape[1]), 2)
      output_grid = np.vstack([output_grid, red_block])

    return output_grid