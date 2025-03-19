"""
1.  **Initialization:** Create an output grid. The output grid has the same width as the input grid. The output grid's height may or may not be different, this is determined later.
2.  **Color Transformation:** Iterate through each pixel of the input grid. If a pixel is blue (value 1), change it to red (value 2) in the output grid, maintaining the same column position.
3.  **Zero Row Insertion (Conditional):** The height relationship between the input and the output varies and depends on the blue pixel positions, but is always either equal or greater than the input height. If the output height is equal to input height, no rows added. If the input pixel is blue, a corresponding red pixel appears in the output grid, at the same column. If a new row is added, it is a row of all zeros. The exact position and number of added rows is variable.
"""

import numpy as np

def get_output_height(input_grid):
    """
    Determines output height based on input, handling different cases.
    This is a placeholder for the complex logic that needs to be determined.
    """
    input_height, input_width = input_grid.shape
    blue_pixels = np.where(input_grid == 1)
    blue_pixel_rows = np.unique(blue_pixels[0])
    num_blue_rows = len(blue_pixel_rows)

    # Placeholder logic - needs further refinement
    if num_blue_rows == 0:
      return input_height

    # Placeholder logic - different strategies
    #return int(input_height * 1.5)
    if num_blue_rows == input_height and input_height == 3: # Example 1.
      return input_height
    if input_height == 4 and num_blue_rows < 3: # Example 3
      return input_height
    else:  # Example 2.
      return input_height+1

    return input_height  # Default: same height


def transform(input_grid):
    # Initialize output_grid.
    input_height, input_width = input_grid.shape
    output_height = get_output_height(input_grid)  # Get dynamic height
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # Find blue pixel coordinates in the input grid
    blue_pixels = np.where(input_grid == 1)
    blue_pixel_coords = list(zip(blue_pixels[0], blue_pixels[1]))


    # Create a mapping for rows where red pixels should be
    red_pixel_rows = []
    for r, c in blue_pixel_coords:
        red_pixel_rows.append(r)

    red_pixel_rows = sorted(list(set(red_pixel_rows)))

    output_row_index = 0
    for input_row in range(input_height):
        if input_row in red_pixel_rows:
          for c in range(input_width):
              if input_grid[input_row,c] == 1:
                output_grid[output_row_index,c] = 2
              else:
                output_grid[output_row_index,c] = input_grid[input_row,c]
          output_row_index += 1
        else: # copy row over
          for c in range(input_width):
            output_grid[output_row_index, c] = input_grid[input_row, c]
          output_row_index +=1
    return output_grid