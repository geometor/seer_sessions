"""
Transforms an input grid into an output grid by extracting colored regions above and below a horizontal azure line, and then stacking these regions, considering only the bounding box of colored pixels in each section.
"""

import numpy as np

def get_azure_line_row(grid):
    """Finds the row index of the horizontal azure line."""
    for i, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return i
    return -1  # Should not happen given the task description

def get_colored_rows_cols(grid_section):
    """
    Identifies rows and columns with colored (non-white, non-azure) pixels.
    Returns a tuple of (rows, cols), where each is a set of indices.
    """
    rows = set()
    cols = set()
    for i, row in enumerate(grid_section):
        for j, pixel in enumerate(row):
            if pixel != 0 and pixel != 8:
                rows.add(i)
                cols.add(j)
    return rows, cols


def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    input_grid = np.array(input_grid)
    azure_line_row = get_azure_line_row(input_grid)

    # Separate the grid into sections above and below the azure line
    top_section = input_grid[:azure_line_row]
    bottom_section = input_grid[azure_line_row + 1:]

    # Determine rows and columns with colored pixels for each section
    top_rows, top_cols = get_colored_rows_cols(top_section)
    bottom_rows, bottom_cols = get_colored_rows_cols(bottom_section)

    # Determine output grid dimensions
    output_height = len(top_rows) + len(bottom_rows)
    output_width = max(len(top_cols) if top_cols else 0, len(bottom_cols) if bottom_cols else 0)

    # Create output grid
    if output_height > 0 and output_width > 0:
        output_grid = np.zeros((output_height, output_width), dtype=int)
    else:
        return []

    # Map original column indices to new indices in output
    top_col_map = {old_col: new_col for new_col, old_col in enumerate(sorted(top_cols))}
    bottom_col_map = {old_col: new_col for new_col, old_col in enumerate(sorted(bottom_cols))}

    # Copy top section
    for new_row, old_row in enumerate(sorted(top_rows)):
        for old_col in top_cols:
          if top_section[old_row,old_col] != 0 and top_section[old_row, old_col] != 8:
            output_grid[new_row, top_col_map[old_col]] = top_section[old_row, old_col]

    # Copy bottom section
    for new_row, old_row in enumerate(sorted(bottom_rows)):
        for old_col in bottom_cols:
          if bottom_section[old_row,old_col] != 0 and bottom_section[old_row, old_col] != 8:
            output_grid[new_row + len(top_rows), bottom_col_map[old_col]] = bottom_section[old_row, old_col]


    return output_grid.tolist()