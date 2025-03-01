"""
1.  **Identify Red Shape:** Find all contiguous pixels in the input grid with a color value of 2 (red). This forms the "red_shape".
2.  **Determine Bounding Box:** Calculate the smallest rectangular region (bounding box) that completely encloses the "red_shape".
3. **Create a new grid** with the dimensions of the bounding box.
4.  **Extract and Recolor:**
    *   Iterate though the bounding box coordinates on the input grid
    *   If the pixel in the input grid is red (2), set the corresponding output grid coordinate to gray (5).
    *   Otherwise, if the input grid is not red (2), set the corresponding pixel in the output grid to white (0). Because the new output is initialized to white, this step is unnecessary.
5.  **Output:** Return the resulting grid, where the original "red_shape" is now represented in gray, and all other pixels are white.
"""

import numpy as np

def find_red_shape_bounding_box(grid):
    # Find red pixels
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None

    # Calculate bounding box
    min_row = np.min(red_pixels[:, 0])
    max_row = np.max(red_pixels[:, 0])
    min_col = np.min(red_pixels[:, 1])
    max_col = np.max(red_pixels[:, 1])
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the bounding box of the red shape
    bounding_box = find_red_shape_bounding_box(input_grid)
    if bounding_box is None:
      return []

    min_row, max_row, min_col, max_col = bounding_box

    # Create output grid
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # map values
    for r in range(output_height):
        for c in range(output_width):
            if input_grid[min_row + r, min_col + c] == 2:
                output_grid[r, c] = 5

    return output_grid.tolist()