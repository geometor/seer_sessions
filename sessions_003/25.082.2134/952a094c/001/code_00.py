"""
1.  **Identify the horizontal line:** Find the longest horizontal line of contiguous pixels of the same color. Note its row index and color.

2.  **Identify single pixels:** Locate all single pixels (pixels not connected to any other non-black pixel).

3.  **Iterate through single pixels:** For each single pixel:
    *   Calculate mirrored column. Original columns position from the right edge, becomes the mirrored column position from the left edge.
    *   If original pixel row < horizontal_line row, then the pixel moves to `horizontal_line row - 1`.
    *   If original pixel row > horizontal_line row, then the pixel moves to `horizontal_line row + 1`.
    * The color of the moved pixel, remains unchanged.

4.  **Construct the output grid:** Create a new grid with the same dimensions as the input. Copy the identified horizontal line to its original position. Place the moved pixels in their new positions. All other cells in the output grid are black (0).
"""

import numpy as np

def find_horizontal_line(grid):
    """Finds the longest horizontal line of contiguous pixels of the same color."""
    rows, cols = grid.shape
    longest_line = []
    longest_line_row = -1
    longest_line_color = 0

    for r in range(rows):
        current_line = []
        for c in range(cols):
            if grid[r, c] != 0:
                current_line.append((r, c, grid[r,c]))
            else:
                if len(current_line) > len(longest_line):
                    longest_line = current_line
                    longest_line_row = r
                    if(len(current_line) > 0):
                        longest_line_color = current_line[0][2] #color
                current_line = []
        if len(current_line) > len(longest_line):
            longest_line = current_line
            longest_line_row = r
            if(len(current_line) > 0):
                longest_line_color = current_line[0][2]
    return longest_line, longest_line_row, longest_line_color

def is_single_pixel(grid, r, c):
    """Checks if a pixel is a single, isolated pixel (not part of a larger object)."""
    rows, cols = grid.shape
    if grid[r, c] == 0:
        return False

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != 0:
                return False  # Connected to another non-black pixel
    return True

def find_single_pixels(grid):
    """get a list of single pixels"""
    rows, cols = grid.shape
    single_pixels = []
    for r in range(rows):
        for c in range(cols):
            if is_single_pixel(grid, r, c):
                single_pixels.append( (r,c, grid[r,c]) )
    return single_pixels

def mirrored_column(c, cols):
    """calculate the mirrored column"""
    return cols - 1 - c

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # 1. Identify the horizontal line
    longest_line, line_row, line_color = find_horizontal_line(grid)
    for r, c, _ in longest_line:
        output_grid[r, c] = line_color

    # 2. Identify single pixels
    single_pixels = find_single_pixels(grid)
    
    # 3. Iterate through single pixels and move them
    for r, c, color in single_pixels:
        new_col = mirrored_column(c, cols)
        if r < line_row:
            new_row = line_row - 1
        else:
            new_row = line_row + 1

        if 0 <= new_row < rows and 0 <= new_col < cols:
            output_grid[new_row, new_col] = color

    return output_grid