import numpy as np
from collections import Counter

"""
Identifies horizontal and vertical lines partitioning the input grid. Finds a single unique 'target' pixel located in one of the four quadrants defined by these lines. Extracts and returns the subgrid corresponding to the quadrant containing the target pixel.

1.  Identify the primary background color (most frequent).
2.  Find the row index of the single horizontal line (all same color, different from background).
3.  Find the column index of the single vertical line (all same color, different from background).
4.  Find the coordinates (row, col) of the single 'target' pixel whose color is different from the background color and the line colors.
5.  Determine the quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) containing the target pixel based on its position relative to the lines.
6.  Define the row and column ranges corresponding to the target quadrant.
7.  Extract the subgrid from the input grid using these ranges.
8.  Return the extracted subgrid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Assuming background is the most frequent color
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_lines(grid, background_color):
    """Finds the indices of the horizontal and vertical lines."""
    rows, cols = grid.shape
    h_line_idx = -1
    v_line_idx = -1
    h_line_color = -1
    v_line_color = -1

    # Find horizontal line
    for r in range(rows):
        row = grid[r, :]
        first_color = row[0]
        if first_color != background_color and np.all(row == first_color):
            h_line_idx = r
            h_line_color = first_color
            break # Assume only one horizontal line

    # Find vertical line
    for c in range(cols):
        col = grid[:, c]
        first_color = col[0]
        if first_color != background_color and np.all(col == first_color):
            v_line_idx = c
            v_line_color = first_color
            break # Assume only one vertical line

    if h_line_idx == -1 or v_line_idx == -1:
        raise ValueError("Could not find both horizontal and vertical lines.")

    # In case line colors are needed later, return them too
    # Return line colors as a set to handle cases where they might be the same
    line_colors = {h_line_color, v_line_color}

    return h_line_idx, v_line_idx, line_colors


def find_target_pixel(grid, background_color, line_colors):
    """Finds the coordinates of the unique target pixel."""
    rows, cols = grid.shape
    target_r, target_c = -1, -1
    found = False

    for r in range(rows):
        for c in range(cols):
            pixel_color = grid[r, c]
            if pixel_color != background_color and pixel_color not in line_colors:
                if found:
                     # This assumes exactly one such pixel exists per the problem description
                     raise ValueError("Found more than one potential target pixel.")
                target_r, target_c = r, c
                found = True

    if not found:
        raise ValueError("Could not find the target pixel.")

    return target_r, target_c


def transform(input_grid):
    """
    Transforms the input grid based on quadrant selection guided by a unique pixel.
    """
    # Convert input list of lists to a numpy array
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Identify background color
    background_color = find_background_color(grid_np)

    # 2. & 3. Identify horizontal and vertical lines
    h_line_idx, v_line_idx, line_colors = find_lines(grid_np, background_color)

    # 4. Identify the target pixel
    target_r, target_c = find_target_pixel(grid_np, background_color, line_colors)

    # 5. Determine the target quadrant
    # Define quadrant boundaries (exclusive of lines)
    row_start, row_end = 0, 0
    col_start, col_end = 0, 0

    if target_r < h_line_idx and target_c < v_line_idx:
        # Top-Left quadrant
        row_start, row_end = 0, h_line_idx
        col_start, col_end = 0, v_line_idx
    elif target_r < h_line_idx and target_c > v_line_idx:
        # Top-Right quadrant
        row_start, row_end = 0, h_line_idx
        col_start, col_end = v_line_idx + 1, cols
    elif target_r > h_line_idx and target_c < v_line_idx:
        # Bottom-Left quadrant
        row_start, row_end = h_line_idx + 1, rows
        col_start, col_end = 0, v_line_idx
    elif target_r > h_line_idx and target_c > v_line_idx:
        # Bottom-Right quadrant
        row_start, row_end = h_line_idx + 1, rows
        col_start, col_end = v_line_idx + 1, cols
    else:
        # Should not happen if target pixel is not on a line
        raise ValueError("Target pixel appears to be on a line.")

    # 6. & 7. Extract the subgrid
    output_grid_np = grid_np[row_start:row_end, col_start:col_end]

    # 8. Convert back to list of lists and return
    output_grid = output_grid_np.tolist()

    return output_grid