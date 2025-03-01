"""
1.  **Identify** the central, vertical column of gray (5) pixels.
2.  **Identify** the colored shapes (non-black, non-gray) that are directly adjacent to the gray column.
3.  **Remove** the entire gray column.
4.  **Remove** any non-black colors adjacent to the gray column.
5. **Retain** other non-black/gray colors, adjusting indices due to removed column.
6. The output is a new grid.
"""

import numpy as np

def find_gray_column(grid):
    # Find the column index of the gray (5) pixels.
    for j in range(grid.shape[1]):
        if np.any(grid[:, j] == 5):
            return j
    return -1

def get_colored_shapes(grid, gray_column_index):
  # extracts colored shapes adjacent to gray column
    colored_pixels = []
    for i in range(grid.shape[0]):
        if grid[i, gray_column_index] == 5:
            # Check left neighbor
            if gray_column_index > 0 and grid[i, gray_column_index - 1] != 0 and grid[i, gray_column_index - 1] != 5:
                colored_pixels.append((i, gray_column_index - 1, grid[i, gray_column_index - 1]))
            # Check right neighbor
            if gray_column_index < grid.shape[1] - 1 and grid[i, gray_column_index + 1] != 0 and grid[i, gray_column_index+1] != 5:
                colored_pixels.append((i, gray_column_index + 1, grid[i, gray_column_index + 1]))
    return colored_pixels

def get_all_colored_shapes(grid, gray_column_index):
    # Find all non-black, and non-gray colors
    colored_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] != 0 and grid[r,c] != 5:
                colored_pixels.append((r,c,grid[r,c]))
    return colored_pixels

def transform(input_grid):
    # Find central gray column index
    gray_column_index = find_gray_column(input_grid)

    # Get all non-black/gray colored shape pixels
    colored_pixels = get_all_colored_shapes(input_grid, gray_column_index)

    # Get adjacent pixels to gray
    adjacent_pixels = get_colored_shapes(input_grid, gray_column_index)
    # determine columns to keep, and to remove
    
    # remove adjacent pixels
    final_pixels = [p for p in colored_pixels if p not in adjacent_pixels]

    # keep track of removed columns
    removed_count = 0
    if gray_column_index != -1:
        removed_count = 1

    # Calculate the new column indices after removing the gray column and adjacent
    for i in range(len(final_pixels)):
        r, c, color = final_pixels[i]
        if c > gray_column_index:
            final_pixels[i] = (r, c-removed_count, color)

    # find new width
    new_width = 0
    for (r,c,v) in final_pixels:
        new_width = max(new_width, c)
    new_width = new_width + 1 # since 0 based

    # initialize output_grid
    output_grid = np.zeros((input_grid.shape[0], new_width), dtype=int)

    # copy pixels to output grid
    for x, y, color in final_pixels:
        output_grid[x, y] = color
    
    return output_grid