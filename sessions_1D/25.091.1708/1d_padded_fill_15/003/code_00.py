import numpy as np

"""
Transformation Rule:
1. Assume the input is a grid, likely with a single row (shape 1xN).
2. Identify the unique non-white color (C) present in the input grid's first row.
3. Find all column indices where color C appears in the first row.
4. Determine the minimum (min_index) and maximum (max_index) of these column indices.
5. Create a new output grid with the exact same dimensions as the input grid, and initialize all its pixels to white (0).
6. In the first row of the output grid, set the color of all pixels from column min_index to max_index (inclusive) to color C.
7. Return the modified output grid.
"""

def find_non_background_color(grid, background_color=0):
    """Finds the single color in the grid that is not the background color."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != background_color:
            return color
    # Return background color if only background is present,
    # or None if grid is empty (though ARC constraints likely prevent empty).
    return background_color if grid.size > 0 else None

def transform(input_grid):
    """
    Fills the horizontal segment between the first and last occurrence
    of the non-background color in the first row.
    """
    # Find the non-background color
    fill_color = find_non_background_color(input_grid, background_color=0)

    # If only background color exists, return a grid of background color
    # (Using zeros_like handles the case where input was already all background)
    if fill_color == 0:
        return np.zeros_like(input_grid)

    # Find the row and column indices where the fill_color appears
    # We assume the relevant information is in the first row if multiple rows exist,
    # but the examples strongly suggest 1xN grids. If it's truly 1xN,
    # row_indices will just be zeros. We primarily need column indices.
    row_indices, col_indices = np.where(input_grid == fill_color)

    # Handle case where the identified fill_color isn't actually present
    # (Should not happen if fill_color != 0, but defensive check)
    if col_indices.size == 0:
         return np.zeros_like(input_grid) # Or return input_grid? Based on rule, output should be filled. Let's stick to zeros.

    # Determine the minimum and maximum column index
    min_col = np.min(col_indices)
    max_col = np.max(col_indices)

    # Create the output grid, initialized with the background color (0)
    output_grid = np.zeros_like(input_grid)

    # Fill the segment in the first row (index 0) between min_col and max_col (inclusive)
    # This assumes the transformation applies to the first row or the only row.
    # If the grid can have multiple rows and the color appears in others,
    # this logic might need adjustment, but fits the examples.
    output_grid[0, min_col : max_col + 1] = fill_color

    return output_grid