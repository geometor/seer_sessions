"""
Extracts "L" shapes from the bottom section of the input grid (below a row of 7s) and represents them with the color azure (8) in the output grid.
"""

import numpy as np

def find_separator_row(grid, separator_value=7):
    """Finds the row index of the separator line."""
    for i, row in enumerate(grid):
        if all(pixel == separator_value for pixel in row):
            return i
    return -1  # Separator not found

def extract_bottom_section(grid, separator_row_index):
    """Extracts the section of the grid below the separator row."""
    if separator_row_index != -1:
        return grid[separator_row_index + 1:]
    return None

def find_l_shapes(grid):
    """Identifies "L" shapes in the given grid.  This is a simplified "L" shape detector
    and may need to be improved."""
    l_shapes = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 6:
                # Check for different L orientations
                if grid[r + 1, c] == 6 and grid[r, c + 1] == 6:  # Standard L
                    l_shapes.append([(r, c), (r + 1, c), (r, c + 1)])
                if grid[r + 1,c] == 6 and grid[r+1,c+1] == 6:
                    l_shapes.append([(r,c), (r+1,c), (r+1, c+1)])
                if grid[r,c+1] == 6 and grid[r+1, c+1] == 6:
                    l_shapes.append([(r,c), (r,c+1), (r+1,c+1)])
                if r > 0 and grid[r-1,c] == 6 and grid[r,c+1] == 6:
                    l_shapes.append([(r,c), (r-1,c), (r, c+1)])

    return l_shapes

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find the separator row index
    separator_row_index = find_separator_row(input_grid)

    # Extract the bottom section of the grid
    bottom_section = extract_bottom_section(input_grid, separator_row_index)
    
    # initialize output grid as all zeros, same size as bottom section, or input section if no bottom
    if bottom_section is not None:
       output_grid = np.zeros(bottom_section.shape, dtype=int)
    else:
       output_grid = np.zeros(input_grid.shape, dtype=int)

    # Find "L" shapes in the bottom section
    if bottom_section is not None:
        l_shapes = find_l_shapes(bottom_section)

        # Replace "L" shape pixels with azure (8) in the output grid
        for l_shape in l_shapes:
            for r, c in l_shape:
                output_grid[r, c] = 8

    return output_grid.tolist()