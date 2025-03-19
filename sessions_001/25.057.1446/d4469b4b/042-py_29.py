"""
1.  **Identify the green pixel:** Locate the single green pixel within the input grid.
2.  **Extract Subgrid:** Extract a 3x3 subgrid from the input grid. The green pixel should ideally be the center of this subgrid.
3.  **Handle Edge Cases:** If the green pixel is too close to the edge of the input grid, such that a full 3x3 subgrid cannot be extracted centered on it, then extract the grid that includes the edges and corners as much as possible (shift the center of the extracted grid to an optimal center).
4.  **Color Substitution:** Within the extracted 3x3 subgrid, change the green pixel (which is now the center pixel or, if it's not possible to be in center, close to the center) to grey. All the other pixels are white, and no color changes happen to them.
5. **Output:** Return this modified 3x3 subgrid as the output.
"""

import numpy as np

def find_green_pixel(grid):
    # Find the coordinates of the green pixel (value 3).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 3:
                return (i, j)
    return None  # Should not happen in this task, but good practice

def extract_subgrid(grid, center_row, center_col):
    # Extract a 3x3 subgrid centered at (center_row, center_col).
    rows, cols = grid.shape
    start_row = max(0, center_row - 1)
    end_row = min(rows, center_row + 2)  # +2 because slicing is exclusive
    start_col = max(0, center_col - 1)
    end_col = min(cols, center_col + 2) # +2 because slicing is exclusive
    
    subgrid = grid[start_row:end_row, start_col:end_col]

    # Create a new 3x3 grid and place subgrid inside of it.
    output_grid = np.zeros((3, 3), dtype=int)
    out_row_start = 1 - (center_row - start_row)
    out_col_start = 1 - (center_col - start_col)

    out_row_end = out_row_start + (end_row - start_row)
    out_col_end = out_col_start + (end_col - start_col)

    output_grid[out_row_start:out_row_end, out_col_start:out_col_end] = subgrid;
   
    return output_grid


def transform(input_grid):
    # Find the green pixel.
    green_pixel_coords = find_green_pixel(input_grid)

    if green_pixel_coords is None:
        return None # Should not happen based on problem definition

    # Extract the 3x3 subgrid.
    output_grid = extract_subgrid(input_grid, green_pixel_coords[0], green_pixel_coords[1])

    # Change the green pixel to grey. Iterate to cover case where it may not be center
    for i in range(3):
      for j in range(3):
        if output_grid[i,j] == 3:
            output_grid[i, j] = 5

    return output_grid