import numpy as np

"""
Identifies red (2) and yellow (4) pixels in the input grid.
Determines the geometric alignment (row, column, or diagonal) of all red and yellow pixels combined.
If all colored pixels are aligned in the same row OR if there is no specific alignment (row, column, or diagonal), change the yellow pixel(s) to white (0).
If all colored pixels are aligned in the same column OR on the same diagonal, change the red pixels to white (0).
"""

def find_pixels(grid, color):
    """Finds all pixels of a specific color."""
    locations = np.argwhere(grid == color)
    # Convert to list of (row, col) tuples
    return [tuple(loc) for loc in locations]

def is_row_aligned(locations):
    """Checks if all locations share the same row."""
    if not locations:
        return False # Or True depending on definition, False seems safer
    first_row = locations[0][0]
    return all(loc[0] == first_row for loc in locations)

def is_col_aligned(locations):
    """Checks if all locations share the same column."""
    if not locations:
        return False
    first_col = locations[0][1]
    return all(loc[1] == first_col for loc in locations)

def is_diag_aligned(locations):
    """Checks if all locations lie on the same diagonal."""
    if len(locations) <= 1:
         # A single point or no points can be considered diagonally aligned
         # Or false, let's treat single/no points as not aligned for clarity
        return False

    # Check main diagonal type (r - c = constant)
    first_diff = locations[0][0] - locations[0][1]
    main_diag = all((loc[0] - loc[1]) == first_diff for loc in locations)

    # Check anti-diagonal type (r + c = constant)
    first_sum = locations[0][0] + locations[0][1]
    anti_diag = all((loc[0] + loc[1]) == first_sum for loc in locations)

    return main_diag or anti_diag

def transform(input_grid):
    """
    Transforms the input grid based on the alignment of red and yellow pixels.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find the locations of red and yellow pixels
    red_locations = find_pixels(output_grid, 2)
    yellow_locations = find_pixels(output_grid, 4)

    # Combine all colored pixel locations
    all_colored_locations = red_locations + yellow_locations

    # Handle cases where one or both colors might be missing (though not in examples)
    if not all_colored_locations:
        return output_grid # No colored pixels, return original

    # Check alignment of all colored pixels
    row_align = is_row_aligned(all_colored_locations)
    col_align = is_col_aligned(all_colored_locations)
    diag_align = is_diag_aligned(all_colored_locations)

    # Determine which pixels to remove based on alignment rules
    remove_yellow = False
    remove_red = False

    if row_align:
        remove_yellow = True
    elif col_align:
        remove_red = True
    elif diag_align:
        remove_red = True
    else: # No specific alignment
        remove_yellow = True

    # Change the selected pixels to white (0)
    if remove_yellow:
        for r, c in yellow_locations:
            output_grid[r, c] = 0
    elif remove_red:
        for r, c in red_locations:
            output_grid[r, c] = 0

    return output_grid