"""
Identifies "L" shapes (groups of three connected magenta pixels) in the section of the input grid below a horizontal line of orange (7) pixels.
Replaces these "L" shapes with azure (8) pixels in the output grid, maintaining their original relative positions.
If no separator line is found, the entire input grid is considered.
"""

import numpy as np

def find_separator_row(grid):
    """Finds the row index of the separator line (all 7s)."""
    for i, row in enumerate(grid):
        if all(pixel == 7 for pixel in row):
            return i
    return -1  # Separator not found

def extract_bottom_section(grid, separator_row_index):
    """Extracts the section of the grid below the separator row."""
    if separator_row_index != -1:
        return grid[separator_row_index + 1:]
    return grid # Return entire grid if separator not found

def is_valid_coordinate(row, col, rows, cols):
    """Checks if a coordinate is within the grid bounds."""
    return 0 <= row < rows and 0 <= col < cols

def find_l_shapes(grid):
    """Identifies "L" shapes in the given grid."""
    l_shapes = []
    rows, cols = grid.shape
    visited = set()

    def is_l_shape(pixels):
        """Checks if a set of three pixels forms an L shape."""
        if len(pixels) != 3:
            return False

        # Convert pixel list to a set of tuples for easier comparison
        pixel_set = set(pixels)

        # Check for connectivity:  All pixels should be neighbors of at least one other pixel in the set
        for r1, c1 in pixel_set:
            neighbors = 0
            for r2, c2 in pixel_set:
                if (r1, c1) != (r2, c2):
                    if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                        neighbors += 1
            if neighbors < 1:  # At least one neighbor required
                return False
        
        # check for 3 pixels that are connected and form a L
        # find a corner and two adjacent pixels.
        for r1, c1 in pixel_set:
            adj = []
            for r2, c2 in pixel_set:
                if (r1,c1) != (r2,c2) and abs(r1-r2) <= 1 and abs(c1-c2) <= 1:
                    adj.append((r2,c2))
            if len(adj) == 2:
                # check for straight line
                if adj[0][0] == adj[1][0] or adj[0][1] == adj[1][1]:
                    return True
        return False


    def explore_neighbors(row, col, current_l_shape):
        """Recursively explores neighbors to find connected magenta pixels."""
        if (row, col) in visited or not is_valid_coordinate(row, col, rows, cols) or grid[row, col] != 6:
            return

        visited.add((row, col))
        current_l_shape.append((row, col))

        # Explore adjacent cells
        explore_neighbors(row + 1, col, current_l_shape)
        explore_neighbors(row - 1, col, current_l_shape)
        explore_neighbors(row, col + 1, current_l_shape)
        explore_neighbors(row, col - 1, current_l_shape)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 6 and (r, c) not in visited:
                current_l_shape = []
                explore_neighbors(r, c, current_l_shape)
                if is_l_shape(current_l_shape):
                    l_shapes.append(current_l_shape)

    return l_shapes

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find the separator row index
    separator_row_index = find_separator_row(input_grid)

    # Extract the bottom section of the grid (or the whole grid if no separator)
    bottom_section = extract_bottom_section(input_grid, separator_row_index)

    # Calculate offset for correct positioning in output
    row_offset = separator_row_index + 1 if separator_row_index != -1 else 0
    
    # initialize output grid as all zeros, same size as *bottom section*
    output_grid = np.zeros(bottom_section.shape, dtype=int)


    # Find "L" shapes in the bottom section
    l_shapes = find_l_shapes(bottom_section)

    # Replace "L" shape pixels with azure (8) in the output grid
    for l_shape in l_shapes:
        for r, c in l_shape:
            # Adjust row index based on offset
            output_grid[r, c] = 8  

    return output_grid.tolist()