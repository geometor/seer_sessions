"""
The transformation extracts specific columns from the input grid and arranges them to form the output grid. The selection of columns is based on the colors present at the top row of the input grid. The rule consistently selects columns starting with colors 4 (yellow), 0 (white), 1 (blue), and 9 (maroon), followed by color 8 (azure) if present. The height of selected columns is always 5. The selected subgrids are then placed adjacent to one another to produce the output.
"""

import numpy as np

def get_subgrids_by_top_row_colors(grid, colors, height=5):
    """
    Identifies and returns subgrids (columns) that start with specified colors,
    with a fixed height of 5.
    """
    selected_subgrids = []
    for j in range(grid.shape[1]):
        if grid[0, j] in colors:
            subgrid = grid[:height, j]
            selected_subgrids.append(subgrid)
    return selected_subgrids

def transform(input_grid):
    """
    Transforms the input grid by selecting subgrids starting with specified colors
    and arranging them into a new output grid. The height of the subgrids
    is fixed at 5.
    """
    # Define the target colors, including 8 (azure)
    target_colors = [4, 0, 1, 9, 8]

    # Get subgrids starting with the target colors and a fixed height of 5
    selected_subgrids = get_subgrids_by_top_row_colors(input_grid, target_colors)

    # Initialize the output grid
    output_grid = np.zeros((5, len(selected_subgrids)), dtype=int)

    # Fill in output
    for i, subgrid in enumerate(selected_subgrids):
        output_grid[:, i] = subgrid

    return output_grid