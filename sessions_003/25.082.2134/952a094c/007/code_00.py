"""
1.  **Find the Longest Horizontal Line:** Examine the input grid to identify the longest horizontal line. A horizontal line is defined as a contiguous sequence of pixels of the same color in a single row. If there are multiple lines of the same maximum length, *any* of them is acceptable. Record the row index, color, starting column, and length of this line.

2.  **Identify Pixels for Reflection:** Identify all pixels in the input grid that *do not* belong to the longest horizontal line found in step 1, and are not black (color 0).

3.  **Reflect Pixels:** For each pixel identified in step 2:
    *   **Vertical Reflection:** Calculate the new row index. The new row will be the same distance from the horizontal line's row as the original pixel, but on the opposite side.  If the pixel is above the line, the reflected pixel will be below. If the pixel is below the line, the reflected pixel is above it.
    *   **Horizontal Reflection:** Calculate the new column index. The new column will be mirrored across the vertical center of the grid.  This is calculated as `grid_width - 1 - original_column`.
    *   **Boundary Check:** If the new row or column index falls outside the grid boundaries (less than 0 or greater than or equal to the grid's height or width, respectively), *ignore* that pixel; it is not reflected.

4.  **Create Output Grid:** Create a new grid of the same dimensions as the input grid, initially filled with black (0) pixels.

5.  **Place Horizontal Line:** Copy the longest horizontal line found in step 1 to the output grid, preserving its original row, color, starting column, and length.

6.  **Place Reflected Pixels:** For each reflected pixel (those not ignored due to boundary checks), place it in the output grid at its new row and column, using its original color.
"""

import numpy as np

def find_longest_horizontal_line(grid):
    """Finds the longest horizontal line of contiguous pixels of the same color."""
    rows, cols = grid.shape
    longest_line_row = -1
    longest_line_color = 0
    longest_line_start_col = -1
    longest_line_length = 0

    for r in range(rows):
        current_length = 0
        current_color = 0
        current_start_col = -1
        for c in range(cols):
            if grid[r, c] != 0:
                if current_length == 0:
                    current_start_col = c
                    current_color = grid[r,c]
                current_length += 1
            else:
                if current_length > longest_line_length:
                    longest_line_length = current_length
                    longest_line_row = r
                    longest_line_color = current_color
                    longest_line_start_col = current_start_col
                current_length = 0
                current_start_col = -1

        # Check at the end of the row
        if current_length > longest_line_length:
            longest_line_length = current_length
            longest_line_row = r
            longest_line_color = current_color
            longest_line_start_col = current_start_col

    return longest_line_row, longest_line_color, longest_line_start_col, longest_line_length

def find_pixels_for_reflection(grid, longest_line_row, longest_line_start_col, longest_line_length):
    """Find all non-black pixels that are NOT part of the longest horizontal line"""
    rows, cols = grid.shape
    pixels_to_reflect = []
    
    for r in range(rows):
        for c in range(cols):
            is_part_of_line = (
                r == longest_line_row and
                c >= longest_line_start_col and
                c < longest_line_start_col + longest_line_length
            )
            if grid[r,c] != 0 and not is_part_of_line:
                pixels_to_reflect.append( (r, c, grid[r,c]) )  # Store row, col, and color
    return pixels_to_reflect
    

def mirrored_column(c, cols):
    """calculate the mirrored column"""
    return cols - 1 - c

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # 1. Find the Longest Horizontal Line
    line_row, line_color, line_start_col, line_length = find_longest_horizontal_line(grid)

    # 2. Find Pixels for Reflection
    pixels_to_reflect = find_pixels_for_reflection(grid, line_row, line_start_col, line_length)


    # 3. Reflect Pixels and 4. Create/Fill Output Grid
    # 5. Place Horizontal line
    if line_row != -1:  # Ensure a line was found
      for i in range(line_length):
          output_grid[line_row, line_start_col + i] = line_color

    # 6. Place Reflected Pixels
    for r, c, color in pixels_to_reflect:
        # Vertical Reflection
        new_row = line_row - (r - line_row)

        # Horizontal Reflection
        new_col = mirrored_column(c, cols)

        # Boundary Check
        if 0 <= new_row < rows and 0 <= new_col < cols:
            output_grid[new_row, new_col] = color

    return output_grid