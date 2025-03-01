# 5daaa586 • 008 • refine_coder

---
```python
"""
1.  **Identify:** Locate the vertical green line, the vertical azure line, and all red pixels within the input grid.
2.  **Select:**
    *   Select the entire green line.
    *   Select the entire azure line.
    *   Select all red pixels that are located to the *right* of the azure line.
3.  **Crop:**
    *   Determine the highest row index and the lowest row index among all selected pixels (green line, azure line, and selected red pixels).
    *   Remove all rows above the highest row index and all rows below the lowest row index.
4.  **Create Output Grid:**
    *   Create a new grid with a height equal to (lowest row index - highest row index + 1).
    *   The width of the output will vary.
    *   The first column will always be the selected green line.
5.  **Place Objects:**
    *   Place the selected green line in the first column (column 0) of the output grid.
    *    Place the selected azure line in the *last* column of the output grid.
6. **Place Red:**
 * Create a new column for each unique x offset of selected red pixels.
 * Place the selected red pixels in the output grid, maintaining their original vertical positions (row indices) relative to the cropped region (adjusting for the removed rows).
 * Place each in their corresponding column.
7.  **Fill Background:** Fill any remaining empty cells in the output grid with white (0).
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds the starting row and column index of a vertical line of the specified color."""
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if it's a vertical line
                if i + 1 < rows and grid[i + 1, j] == color:
                    return i, j
    return None, None

def get_vertical_line_pixels(grid, col, color):
     """Extracts the pixels of vertical line"""
     rows = grid.shape[0]
     pixels = []
     for i in range(rows):
        if grid[i, col] == color:
            pixels.append((i, col))
     return pixels
    

def find_red_pixels(grid):
    """Finds all red pixels in the grid."""
    rows, cols = grid.shape
    red_pixels = []
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2:
                red_pixels.append((i, j))
    return red_pixels

def transform(input_grid):
    # Find the green line
    green_start_row, green_col = find_vertical_line(input_grid, 3)
    green_pixels = get_vertical_line_pixels(input_grid, green_col, 3)

    # Find the azure line
    azure_start_row, azure_col = find_vertical_line(input_grid, 8)
    azure_pixels = get_vertical_line_pixels(input_grid, azure_col, 8)

    # Find red pixels
    red_pixels = find_red_pixels(input_grid)

    # Select red pixels to the *right* of the azure line
    selected_red_pixels = [p for p in red_pixels if p[1] > azure_col]
    
    # Determine the output grid dimensions based on selected pixels only
    min_row = min(min(p[0] for p in green_pixels), min(p[0] for p in azure_pixels), min(p[0] for p in selected_red_pixels if p))
    max_row = max(max(p[0] for p in green_pixels), max(p[0] for p in azure_pixels), max(p[0] for p in selected_red_pixels if p))

    output_height = max_row - min_row + 1
    output_width = 2  # Initialize with width for green and azure lines

    # Initialize the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the green line in the first column
    for i in range(len(green_pixels)):
        row_in_grid = green_pixels[i][0]
        output_grid[row_in_grid - min_row, 0] = 3

    # Place the azure line in the last column
    for i in range(len(azure_pixels)):
      row_in_grid = azure_pixels[i][0]
      output_grid[row_in_grid - min_row, output_width - 1] = 8

    # If there are red pixels *right of the azure line, add columns and fill them*
    if len(selected_red_pixels) > 0:
        #resize, adding columns for each *unique x-offset* of red pixel
        output_width += len(set([p[1] for p in selected_red_pixels]))
        output_grid = np.zeros((output_height, output_width), dtype=int)

        #re-add green line
        for i in range(len(green_pixels)):
          row_in_grid = green_pixels[i][0]
          output_grid[row_in_grid - min_row, 0] = 3

        #re-add azure
        for i in range(len(azure_pixels)):
          row_in_grid = azure_pixels[i][0]
          output_grid[row_in_grid - min_row, output_width - 1] = 8

        #fill red, starting at column 1
        red_col_offset = 1
        #get *unique* and sorted red columns
        red_cols = sorted(list(set([p[1] for p in selected_red_pixels])))

        for col in red_cols:
          for pixel in selected_red_pixels:
            if pixel[1] == col:
               output_grid[pixel[0] - min_row, red_col_offset] = 2
          red_col_offset+=1 #increment each time a column of reds has been added

    return output_grid
```
