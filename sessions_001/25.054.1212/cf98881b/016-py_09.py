"""
1.  **Identify Target Colors:** The target colors are 4 (yellow) and 9 (maroon).
2.  **Find Centroid of Color 9:** Find an approximate "centroid" of the color 9 pixels.  Not a true centroid, but a representative point.
3.  **Determine Quadrant:**  Divide the input grid conceptually into four quadrants based on the overall input grid dimensions (not the color 9 centroid).
4.  **Select Input Quadrant:** Select the quadrant of the input grid that contains the "centroid" of color 9.
5.  **Extract 4x4 Subgrid:** From the selected quadrant, extract a 4x4 subgrid. The top-left corner of this subgrid is determined as follows:
    - If the "centroid" of color 9 falls within the 4x4 area from the top-left of its quadrant, take the quadrant's top-left as the subgrid origin.
    - Consider the subgrid around the instances of 9.
    - Consider mirroring the subgrid based on the original prediction being the mirror of the correct output.
6. **compose output:** construct output_grid from the selected subgrid.
"""

import numpy as np

def get_color_centroid(grid, color):
    # finds approximate "centroid" of a color - the first instance
    grid = np.array(grid)
    rows, cols = np.where(grid == color)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def get_quadrant(grid, row, col):
    # determines which quadrant a given row,col falls into
    grid_height, grid_width = len(grid), len(grid[0])
    mid_row = grid_height // 2
    mid_col = grid_width // 2

    if row < mid_row and col < mid_col:
        return 0  # Top-left
    elif row < mid_row and col >= mid_col:
        return 1  # Top-right
    elif row >= mid_row and col < mid_col:
        return 2  # Bottom-left
    else:
        return 3  # Bottom-right

def get_4x4_subgrid(grid, row_start, col_start):
    # safely extracts a 4x4 subgrid, padding with 0 if necessary
    grid = np.array(grid)
    rows, cols = grid.shape
    subgrid = np.zeros((4, 4), dtype=int)

    for r in range(4):
        for c in range(4):
            grid_row = row_start + r
            grid_col = col_start + c
            if 0 <= grid_row < rows and 0 <= grid_col < cols:
                subgrid[r, c] = grid[grid_row, grid_col]

    return subgrid

def transform(input_grid):
    # make input a numpy array
    input_grid = np.array(input_grid)

    # get centroid of color 9
    centroid_9 = get_color_centroid(input_grid, 9)

    if centroid_9 is None:
        # if color 9 not, return all zeros - this needs to change in future
        #  iterations
        return np.zeros((4, 4), dtype=int).tolist()

    centroid_row, centroid_col = centroid_9

    # determine the quadrant of the centroid
    quadrant = get_quadrant(input_grid, centroid_row, centroid_col)

    # determine the starting point of the quadrant
    grid_height, grid_width = input_grid.shape
    quadrant_row_start = 0 if quadrant in (0, 1) else grid_height // 2
    quadrant_col_start = 0 if quadrant in (0, 2) else grid_width // 2
    
    # check and adjust the extraction to include all 9 instances, but at most 4x4
    rows, cols = np.where(input_grid == 9)
    min_row, max_row = min(rows), min(rows + 4, input_grid.shape[0]) #limit rows to original bounds
    min_col, max_col = min(cols), min(cols + 4, input_grid.shape[1])#limit cols to original bounds
        
    output_grid = get_4x4_subgrid(input_grid, min_row, min_col)

    # flip rows and then flip cols
    output_grid = np.flip(output_grid, axis=0)
    output_grid = np.flip(output_grid, axis=1)

    return output_grid.tolist()