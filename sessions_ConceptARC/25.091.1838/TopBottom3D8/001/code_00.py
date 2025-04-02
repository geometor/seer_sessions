import numpy as np
import copy

"""
Identifies a single vertical bar and one or more horizontal bars in the input grid.
For each intersection point between the vertical bar and a horizontal bar:
- If the horizontal bar's color is yellow (4), the intersection pixel in the output grid takes the yellow color.
- Otherwise, the intersection pixel in the output grid takes the color of the vertical bar.
Pixels not at an intersection remain unchanged.
"""

def find_vertical_bar(grid):
    """
    Finds the column index and color of the single vertical bar.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (column_index, color) of the vertical bar, or (None, None) if not found.
    """
    height, width = grid.shape
    for c in range(width):
        col_cells = grid[:, c]
        non_background_indices = np.where(col_cells != 0)[0]

        if len(non_background_indices) >= 2:  # Need at least 2 pixels for a bar
            # Check for contiguity
            if np.all(np.diff(non_background_indices) == 1):
                # Check if all non-background cells have the same color
                bar_color = col_cells[non_background_indices[0]]
                if np.all(col_cells[non_background_indices] == bar_color):
                    return c, bar_color
    return None, None

def find_horizontal_bars(grid):
    """
    Finds the row index and color of all horizontal bars.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (row_index, color) of a horizontal bar.
    """
    height, width = grid.shape
    bars = []
    for r in range(height):
        row_cells = grid[r, :]
        non_background_indices = np.where(row_cells != 0)[0]

        if len(non_background_indices) >= 2: # Need at least 2 pixels for a bar
            # Check for contiguity
             # Find potential bar segments within the row
            current_start = -1
            current_color = -1
            for c in range(width):
                pixel_color = row_cells[c]
                if pixel_color != 0: # Non-background
                    if current_start == -1: # Start of a new potential segment
                        current_start = c
                        current_color = pixel_color
                    elif pixel_color != current_color: # Color changed, end previous segment
                         if c - current_start >= 2: # Check length of the previous segment
                             bars.append((r, current_color))
                         # Start new segment
                         current_start = c
                         current_color = pixel_color
                elif current_start != -1: # Background pixel encountered, end current segment
                    if c - current_start >= 2: # Check length
                        bars.append((r, current_color))
                    current_start = -1
                    current_color = -1

            # Check for segment ending at the last column
            if current_start != -1 and width - current_start >= 2:
                 bars.append((r, current_color))


    # It seems the previous logic might detect multiple segments in a single row.
    # Let's refine based on the examples where each horizontal bar seems unique per row.
    # Revised simpler logic: If a row has >=2 non-background cells AND they are contiguous AND all the same color, it's a bar.
    refined_bars = []
    for r in range(height):
        row_cells = grid[r, :]
        non_background_indices = np.where(row_cells != 0)[0]

        if len(non_background_indices) >= 2:
             # Check contiguity
             if np.all(np.diff(non_background_indices) == 1):
                 # Check same color
                 bar_color = row_cells[non_background_indices[0]]
                 if np.all(row_cells[non_background_indices] == bar_color):
                     refined_bars.append((r, bar_color))

    return refined_bars


def transform(input_grid):
    """
    Transforms the input grid based on the intersection color rules.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = copy.deepcopy(grid_np)

    # Find the vertical bar
    v_col, v_color = find_vertical_bar(grid_np)
    if v_col is None:
        # No vertical bar found, return copy of input
        return output_grid.tolist()

    # Find horizontal bars
    h_bars = find_horizontal_bars(grid_np)

    # Process intersections
    for h_row, h_color in h_bars:
        # Intersection point coordinates
        intersection_row = h_row
        intersection_col = v_col

        # Check if the intersection point actually exists on both bars
        # (This check might be redundant if find_* functions are accurate)
        if grid_np[intersection_row, intersection_col] != 0: # Ensure intersection is not background
            # Apply the color rule
            if h_color == 4: # If horizontal bar is yellow
                output_grid[intersection_row, intersection_col] = h_color # Set to yellow
            else:
                output_grid[intersection_row, intersection_col] = v_color # Set to vertical bar color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
