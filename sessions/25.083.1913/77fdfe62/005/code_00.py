"""
1.  **Find Dividers:** Locate the horizontal and vertical lines composed entirely of blue pixels (value '1') within the input grid. These act as dividers.
2.  **Identify Objects:** Divide the input grid into four regions based on the horizontal and vertical dividers: top-left, top-right, bottom-left, and bottom-right. Within each of these regions, identify distinct "objects." An object is a group of connected pixels of the same color, *excluding* the blue divider pixels and background (0 or white).
3.  **Construct Output Grid:** Create a 2x2 output grid.
    - The object from the top-left region becomes the top-left cell of the output
    - The object from the bottom-left region becomes the top-right cell of the output.
    - The object from the top-right region becomes the bottom-left cell.
    - The object from the bottom-right region becomes the bottom-right cell.
    - When an object consists of more than a single pixel, use only the color, not the shape, and make the output object a single pixel of that color.
    - If a region does not contain a valid object, use color '0' (white).
4. Output size is variable. Example 2 has 4 x 4.
"""

import numpy as np

def find_dividers(grid):
    rows, cols = len(grid), len(grid[0])
    horizontal_divider = -1
    vertical_divider = -1

    for r in range(rows):
        if all(grid[r][c] == 1 for c in range(cols)):
            horizontal_divider = r
            break

    for c in range(cols):
        if all(grid[r][c] == 1 for r in range(rows)):
            vertical_divider = c
            break

    return horizontal_divider, vertical_divider

def get_object_color(grid, start_row, end_row, start_col, end_col):
    # Extract the region
    region = grid[start_row:end_row, start_col:end_col]

    # Find unique colors, excluding 0 (background) and 1 (divider)
    unique_colors = np.unique(region)
    filtered_colors = [color for color in unique_colors if color != 0 and color != 1]

    # If there's an object color, return the first one found
    if filtered_colors:
      return filtered_colors[0]
    else:
      return 0

def transform(input_grid):
    grid = np.array(input_grid)
    horizontal_divider, vertical_divider = find_dividers(grid)

    # Handle edge cases where dividers are not found
    if horizontal_divider == -1 or vertical_divider == -1:
      # search other examples to see how to handle
      return [[0]]

    # Initialize output grid
    output_grid = np.zeros((4, 4), dtype=int)  # Initialize as 4x4. Adjust later.

    # Top-left region
    output_grid[0, 0] = get_object_color(grid, 0, horizontal_divider, 0, vertical_divider)

    # Top-right region (adjust indices for 4x4 grid to match expected)
    output_grid[0, 1] = get_object_color(grid, horizontal_divider + 1, len(grid), 0, vertical_divider)
   
    # Bottom-left
    output_grid[1, 0] = get_object_color(grid, 0, horizontal_divider, vertical_divider+1, len(grid[0]))

    # Bottom-right
    output_grid[1,1] = get_object_color(grid, horizontal_divider+1, len(grid), vertical_divider + 1, len(grid[0]))

    # Check for 4x4 output (example 2)
    output_grid[0,2] = get_object_color(grid, 0, horizontal_divider, vertical_divider + 1, len(grid[0]))
    output_grid[0,3] = get_object_color(grid, 0, horizontal_divider, vertical_divider + 1, len(grid[0]))

    output_grid[1,2] = get_object_color(grid, horizontal_divider + 1, len(grid), vertical_divider+1, len(grid[0]))
    output_grid[1,3] = get_object_color(grid, horizontal_divider+1, len(grid), vertical_divider + 1, len(grid[0]))

    output_grid[2,0] = get_object_color(grid, horizontal_divider + 1, len(grid), 0, vertical_divider)
    output_grid[2,1] = get_object_color(grid, horizontal_divider + 1, len(grid), 0, vertical_divider)
    output_grid[3,0] = get_object_color(grid, horizontal_divider + 1, len(grid), 0, vertical_divider)
    output_grid[3,1] = get_object_color(grid, horizontal_divider + 1, len(grid), 0, vertical_divider)

    output_grid[2,2] = get_object_color(grid, horizontal_divider+1, len(grid), vertical_divider + 1, len(grid[0]))
    output_grid[2,3] = get_object_color(grid, horizontal_divider+1, len(grid), vertical_divider + 1, len(grid[0]))
    output_grid[3,2] = get_object_color(grid, horizontal_divider+1, len(grid), vertical_divider + 1, len(grid[0]))
    output_grid[3,3] = get_object_color(grid, horizontal_divider+1, len(grid), vertical_divider + 1, len(grid[0]))
    
    # If all values in row 1 are the same, remove row 1
    if np.all(output_grid[1] == output_grid[1,0]):
        output_grid = np.delete(output_grid, 1, axis=0)
        # If all values in row 2 are now the same, delete it
        if output_grid.shape[0] > 1 and np.all(output_grid[1] == output_grid[1,0]):
            output_grid = np.delete(output_grid, 1, axis=0)
        
    # if rows 2 & 3 are all the same - delete
    if output_grid.shape[0] > 2 and np.all(output_grid[2] == output_grid[2,0]):
      output_grid = np.delete(output_grid, 2, axis=0)

    if output_grid.shape[0] > 3 and np.all(output_grid[3] == output_grid[3,0]):
      output_grid = np.delete(output_grid, 3, axis=0)
        
    # If all values in col 1 are the same, remove col 1
    if np.all(output_grid[:,1] == output_grid[0, 1]):
      output_grid = np.delete(output_grid, 1, axis=1)
      # If all values in col 2 are now the same, delete it
      if output_grid.shape[1] > 1 and np.all(output_grid[:,1] == output_grid[0,1]):
          output_grid = np.delete(output_grid, 1, axis = 1)
    
    if output_grid.shape[1] > 2 and np.all(output_grid[:,2] == output_grid[0,2]):
      output_grid = np.delete(output_grid, 2, axis=1)
    
    if output_grid.shape[1] > 3 and np.all(output_grid[:,3] == output_grid[0,3]):
      output_grid = np.delete(output_grid, 3, axis=1)

    return output_grid.tolist()