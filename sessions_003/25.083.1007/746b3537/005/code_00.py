"""
The transformation identifies all unique colors present in the input grid.
The output is a 1D grid. 
If the first row of the input grid contains all unique colors, the output is one row of pixels, with colors ordered as they first appear, going across each row from top to bottom.
Otherwise, the output is one column of pixels, ordered according to the numerical value of the colors, ascending.
"""

import numpy as np

def _extract_unique_colors(grid):
    """Extracts unique colors from a grid."""
    return np.unique(grid)

def _first_row_contains_all_unique_colors(grid, unique_colors):
    """Checks if the first row contains all unique colors."""
    first_row_colors = np.unique(grid[0])
    return np.array_equal(np.sort(first_row_colors), np.sort(unique_colors))
    
def _get_row_wise_color_order(grid):
    """Gets the order of unique colors appearing row-wise."""
    unique_colors_ordered = []
    for row in grid:
        for pixel in row:
            if pixel not in unique_colors_ordered:
                unique_colors_ordered.append(pixel)
    return unique_colors_ordered

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The 1D output grid.
    """
    # Convert input grid to a numpy array for easier manipulation.
    input_array = np.array(input_grid)

    # Extract unique colors.
    unique_colors = _extract_unique_colors(input_array)

    # Determine output shape and order.
    if _first_row_contains_all_unique_colors(input_array, unique_colors):
        # Output is a single row, ordered by row-wise appearance.
        ordered_colors = _get_row_wise_color_order(input_array)
        output_grid = [ordered_colors]
    else:
        # Output is a single column, ordered numerically.
        output_grid = [[color] for color in sorted(unique_colors)]
        
    return output_grid