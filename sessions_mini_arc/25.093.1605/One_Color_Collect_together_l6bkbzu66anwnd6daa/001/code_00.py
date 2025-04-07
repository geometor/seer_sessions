"""
Transforms a 5x5 binary grid based on the line formed by the '1's.

1.  Identifies the coordinates of all cells containing '1' in the input grid.
2.  Determines if these '1's form a single vertical line, horizontal line, or the main diagonal line.
3.  Initializes an empty 5x5 output grid filled with '0's.
4.  Modifies the output grid based on the identified line type and the center point (2, 2):
    a.  If Vertical Line (at column `C`): Sets cells `(r, C)` to '1' in the output for all input '1's where `r <= 2`. Also ensures the cell `(2, C)` is set to '1'.
    b.  If Horizontal Line (at row `R`): Sets cells `(R, c)` to '1' in the output for all input '1's where `c >= 2`. Also ensures the cell `(R, 2)` is set to '1'.
    c.  If Diagonal Line (r == c): Sets cells `(d, d)` to '1' in the output for all input '1's where `d <= 2`. Also ensures the cell `(2, 2)` is set to '1'.
5.  Returns the modified output grid.
"""

import numpy as np

def _find_ones(grid):
    """Finds the coordinates of all cells with value 1."""
    ones_coords = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                ones_coords.append((r, c))
    return ones_coords

def _check_line_type(ones_coords):
    """
    Determines if the coordinates form a vertical, horizontal, or diagonal line.
    Returns a tuple (line_type, line_index) or (None, None).
    line_index is the column index for vertical, row index for horizontal,
    and None for diagonal.
    """
    if not ones_coords:
        return None, None

    rows = {r for r, c in ones_coords}
    cols = {c for r, c in ones_coords}
    is_diagonal = all(r == c for r, c in ones_coords)

    if len(cols) == 1:
        return 'vertical', list(cols)[0]
    elif len(rows) == 1:
        return 'horizontal', list(rows)[0]
    elif is_diagonal:
        return 'diagonal', None
    else:
        # This case is not expected based on the examples,
        # but included for robustness.
        return None, None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier handling if needed, though list access is fine
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    # Define the center point (zero-based index)
    center_row, center_col = 2, 2

    # Initialize output_grid with zeros
    output_grid = np.zeros_like(grid_np)

    # Find the coordinates of all '1's in the input
    ones_coords = _find_ones(grid_np)

    # Determine the line type formed by the '1's
    line_type, line_index = _check_line_type(ones_coords)

    # Apply transformation based on line type
    if line_type == 'vertical':
        col_idx = line_index
        # Copy relevant '1's from input to output
        for r, c in ones_coords:
            if r <= center_row:
                output_grid[r, col_idx] = 1
        # Ensure the center row coordinate on the line is '1'
        output_grid[center_row, col_idx] = 1
        
    elif line_type == 'horizontal':
        row_idx = line_index
        # Copy relevant '1's from input to output
        for r, c in ones_coords:
             if c >= center_col:
                output_grid[row_idx, c] = 1
        # Ensure the center column coordinate on the line is '1'
        output_grid[row_idx, center_col] = 1

    elif line_type == 'diagonal':
        # Copy relevant '1's from input to output
        for r, c in ones_coords:
             if r <= center_row: # implies c <= center_col as r==c
                output_grid[r, c] = 1
        # Ensure the center coordinate is '1'
        output_grid[center_row, center_col] = 1
        
    # Convert numpy array back to list of lists for the final output format
    return output_grid.tolist()
