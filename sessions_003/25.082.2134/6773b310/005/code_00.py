"""
1.  **Identify Sections:** The input grid is divided into three horizontal sections based on the presence of a horizontal line composed entirely of azure (8) pixels. If such a line exists, the sections are:
    *   **Top Section:** All rows *above* the azure line.
    *   **Middle Section:** The row containing the azure line.
    *   **Bottom Section:** All rows *below* the azure line.
    If no such azure line exists then we assign sections with these rules:
    *   **Top Section:** All rows *before* row index = floor(number of rows / 3)
    *   **Middle Section:** All rows *after* Top Section and *before* row index = floor(number of rows * 2 / 3)
    *   **Bottom Section:** All rows after Middle section.

2.  **Find Magenta Pixels:** Locate all magenta (6) pixels within the input grid.

3.  **Determine Output Row and Column:** For *each* magenta pixel:
    *   The output *row* is determined by which *section* the magenta pixel is in: 0 for the top section, 1 for the middle section, and 2 for the bottom section.
    *   The output *column* is determined by the column index of the magenta pixel within the input grid, divided into three equal ranges:
        *   If the magenta pixel's column index is less than (input grid width / 3), the output column is 0.
        *   If the magenta pixel's column index is greater than or equal to (input grid width / 3) and less than (2 * input grid width / 3), the output column is 1.
        *   If the magenta pixel's column index is greater than or equal to (2 * input grid width / 3), the output column is 2.

4.  **Populate Output Grid:** Create a 3x3 output grid. For each magenta pixel found, set the cell at the corresponding output row and column (determined in step 3) to 1 (blue). All other cells in the output grid remain 0. If no magenta pixel is found for a given section then that row in the output grid should be all zeros.
"""

import numpy as np

def get_sections(input_grid):
    """Divides the input grid into three sections based on the horizontal line of 8s or row indices."""
    rows, cols = input_grid.shape
    horizontal_line_row = -1
    for r in range(rows):
        if np.all(input_grid[r] == 8):
            horizontal_line_row = r
            break

    if horizontal_line_row != -1:
        top_section = input_grid[:horizontal_line_row]
        middle_section = input_grid[horizontal_line_row:horizontal_line_row+1]
        bottom_section = input_grid[horizontal_line_row+1:]
    else:
        # No horizontal line found, divide based on row indices
        top_row_end = rows // 3
        middle_row_end = 2 * rows // 3
        top_section = input_grid[:top_row_end]
        middle_section = input_grid[top_row_end:middle_row_end]
        bottom_section = input_grid[middle_row_end:]

    return top_section, middle_section, bottom_section

def find_magenta_pixels(input_grid):
    """Finds the coordinates of all magenta pixels in the input grid."""
    magenta_pixels = []
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 6:
                magenta_pixels.append((r, c))
    return magenta_pixels

def get_output_row_col(magenta_pixel, input_width, top_section, middle_section, bottom_section):
  """Determine the output row and column based on section and input width."""
  row, col = magenta_pixel
  
  #Determine section and thus output row
  output_row = -1
  if row < top_section.shape[0]:
    output_row = 0
  elif row < top_section.shape[0] + middle_section.shape[0]:
    output_row = 1
  elif row < top_section.shape[0] + middle_section.shape[0] + bottom_section.shape[0]:
      output_row = 2

  #Determine output column
  output_col = 0 if col < (input_width / 3) else (1 if col < (2 * (input_width / 3)) else 2)

  return output_row, output_col

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # 1. Identify Sections
    top_section, middle_section, bottom_section = get_sections(input_grid)

    # 2. Find Magenta Pixels
    magenta_pixels = find_magenta_pixels(input_grid)

    # 3. & 4. Determine output row/col and populate
    output_grid = np.zeros((3, 3), dtype=int)
    input_width = input_grid.shape[1]

    for pixel in magenta_pixels:
      output_row, output_col = get_output_row_col(pixel, input_width, top_section, middle_section, bottom_section)
      if output_row != -1: #should always be true
        output_grid[output_row, output_col] = 1

    return output_grid