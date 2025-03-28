"""
Transforms the input grid by identifying specific white rows and columns that act as separators between gray blocks. 
These separators are filled primarily with red, but cells adjacent to non-separator white areas are filled with blue.

1. Identify rows (excluding borders) that are entirely white and are positioned between rows containing at least one gray pixel.
2. Identify columns (excluding borders) that are entirely white and are positioned between columns containing at least one gray pixel.
3. Create a copy of the input grid.
4. Iterate through each cell of the grid.
5. If a cell's row index is identified as a separator row OR its column index is identified as a separator column, AND the cell's original color is white:
    a. Check its four cardinal neighbors in the original input grid.
    b. If any neighbor is within bounds, is white, and its coordinates do NOT correspond to a separator row or column, mark the current cell's target color as blue.
    c. Otherwise, mark the current cell's target color as red.
    d. Update the cell in the output grid with the target color (blue or red).
6. Cells not meeting the separator criteria or cells that were originally not white remain unchanged.
7. Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills separating white rows/columns between gray blocks with red, marking edges with blue.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)

    white = 0
    blue = 1
    red = 2
    gray = 5

    red_rows = set()
    red_cols = set()

    # 1. Identify separating rows
    for r in range(1, height - 1):
        # Check if row r is all white
        if np.all(input_grid[r, :] == white):
            # Check if row r-1 contains gray
            contains_gray_above = np.any(input_grid[r - 1, :] == gray)
            # Check if row r+1 contains gray
            contains_gray_below = np.any(input_grid[r + 1, :] == gray)
            if contains_gray_above and contains_gray_below:
                red_rows.add(r)

    # 2. Identify separating columns
    for c in range(1, width - 1):
        # Check if column c is all white
        if np.all(input_grid[:, c] == white):
             # Check if column c-1 contains gray
            contains_gray_left = np.any(input_grid[:, c - 1] == gray)
            # Check if column c+1 contains gray
            contains_gray_right = np.any(input_grid[:, c + 1] == gray)
            if contains_gray_left and contains_gray_right:
                red_cols.add(c)

    # 3. Iterate and fill separators
    for r in range(height):
        for c in range(width):
            # 4. Check if the cell belongs to a separator row or column
            is_separator_cell = (r in red_rows) or (c in red_cols)

            # 5. If it's a separator cell and was originally white
            if is_separator_cell and input_grid[r, c] == white:
                target_color = red  # Assume red initially
                is_edge = False

                # 5a & 5b. Check neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc

                    # Check if neighbor is within bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # 5b.i Check if neighbor was white
                        if input_grid[nr, nc] == white:
                            # 5b.ii Check if neighbor is NOT part of any separator row/column
                            if (nr not in red_rows) and (nc not in red_cols):
                                is_edge = True
                                break # Found an edge condition, no need to check other neighbors

                # 5c. If it's an edge, set target to blue
                if is_edge:
                    target_color = blue

                # 5d. Update the output grid
                output_grid[r, c] = target_color
            
            # 6. Cells not meeting criteria or not originally white remain unchanged (already copied)

    # 7. Return the result
    return output_grid.tolist() # Convert back to list of lists if necessary
