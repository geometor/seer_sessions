import numpy as np

"""
Transforms an input grid by filling columns based on marker locations and blue boundaries.

1.  **Initialize:** Create the output grid as a copy of the input grid.
2.  **Identify Markers:**
    a.  Locate the single, unique Yellow (4) pixel at `(Ry, Cy)`.
    b.  Locate all Red (2) pixels.
    c.  Find the Red pixel `(Rr, Cr)` closest to the Yellow pixel using L1 distance. Tie-breaking: minimum row index, then minimum column index.
3.  **Determine Boundaries and Fill Columns:**
    a.  Define a boundary function: For a given column, find the minimum row index of any Blue (1) pixel. If no Blue pixel exists, the boundary is the grid height.
    b.  **If `Cr == Cy` (Same Column):**
        i.  The target column `C` is `Cr`.
        ii. Calculate the boundary row `B` for column `C`.
        iii. Fill `output_grid` column `C` from row 0 up to `B-1` with alternating Red (2, even rows) and Yellow (4, odd rows).
        iv. Override: For rows `r` from 0 to `B-1`, if `input_grid[r, C]` was Green (3), set `output_grid[r, C]` to Yellow (4).
    c.  **If `Cr != Cy` (Different Columns):**
        i.  Calculate Red boundary `Br` for column `Cr`. Fill `output_grid` column `Cr` from row 0 to `Br-1` with Red (2).
        ii. Calculate Yellow boundary `By` for column `Cy`. Fill `output_grid` column `Cy` from row 0 to `By-1` with Yellow (4).
4.  **Finalize:** Return the modified `output_grid`. Pixels not explicitly modified retain their original input values.
"""

def find_color_coords(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    # np.argwhere returns [row, col] pairs, scan order is row-major
    coords = np.argwhere(grid == color)
    return [tuple(coord) for coord in coords]

def find_upper_blue_boundary(grid, target_col):
    """
    Finds the minimum row index of a Blue (1) pixel in the target column.
    This row acts as the exclusive upper bound for modifications (fill up to boundary - 1).
    Returns grid height if no Blue pixel is found in the column.
    """
    height, width = grid.shape
    blue_rows_in_col = [r for r, c in find_color_coords(grid, 1) if c == target_col]

    if not blue_rows_in_col:
        # If no blue pixel, the modification applies to the whole column [0, height-1].
        # The boundary is effectively the bottom, so return height.
        return height
    else:
        # Return the row index of the highest (minimum row index) blue pixel.
        return min(blue_rows_in_col)

def find_closest_red(red_coords, yellow_coord):
    """
    Finds the red coordinate closest to the yellow coordinate using L1 distance.
    Tie-breaking: minimum row index, then minimum column index.
    Returns the closest (r, c) tuple or None if no red_coords provided.
    """
    if not red_coords:
        return None

    r_y, c_y = yellow_coord
    min_dist = float('inf')
    closest_r_coord = None

    for r_coord_cand in red_coords:
        r_r_cand, c_r_cand = r_coord_cand
        dist = abs(r_r_cand - r_y) + abs(c_r_cand - c_y)

        if dist < min_dist:
            min_dist = dist
            closest_r_coord = r_coord_cand
        elif dist == min_dist:
            # Tie-breaking
            # Check if candidate row is smaller
            if r_r_cand < closest_r_coord[0]:
                 closest_r_coord = r_coord_cand
            # If rows are equal, check if candidate column is smaller
            elif r_r_cand == closest_r_coord[0] and c_r_cand < closest_r_coord[1]:
                 closest_r_coord = r_coord_cand

    return closest_r_coord


def transform(input_grid):
    # 1. Initialize output_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify Markers
    yellow_coords = find_color_coords(input_grid, 4)
    red_coords = find_color_coords(input_grid, 2)

    # Ensure exactly one yellow marker exists
    if len(yellow_coords) != 1:
        # If assumption is violated, return original grid
        # (or raise an error depending on desired behavior)
        return output_grid
    
    unique_yellow_coord = yellow_coords[0]
    r_y, c_y = unique_yellow_coord

    # Find the closest red marker
    selected_red_coord = find_closest_red(red_coords, unique_yellow_coord)

    # Ensure a red marker was found (red_coords might be empty)
    if selected_red_coord is None:
         # No red marker found, return original grid
        return output_grid

    r_r, c_r = selected_red_coord

    # 3. Determine Boundaries and Fill Columns
    if c_r == c_y:
        # Case: Same Column
        target_col = c_r
        # Find boundary row (exclusive upper limit)
        boundary_row = find_upper_blue_boundary(input_grid, target_col)

        # Fill with alternating pattern up to the boundary
        for r in range(boundary_row):
            color = 2 if r % 2 == 0 else 4 # Red for even rows, Yellow for odd
            output_grid[r, target_col] = color

        # Apply Green override
        for r in range(boundary_row):
            if input_grid[r, target_col] == 3: # Check original input grid
                output_grid[r, target_col] = 4 # Override with Yellow

    else:
        # Case: Different Columns
        # Process Red column
        boundary_row_r = find_upper_blue_boundary(input_grid, c_r)
        for r in range(boundary_row_r):
            output_grid[r, c_r] = 2 # Fill with Red

        # Process Yellow column
        boundary_row_y = find_upper_blue_boundary(input_grid, c_y)
        for r in range(boundary_row_y):
            output_grid[r, c_y] = 4 # Fill with Yellow

    # 4. Finalize
    return output_grid