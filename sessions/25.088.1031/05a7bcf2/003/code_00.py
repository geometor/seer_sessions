import numpy as np
from typing import List, Tuple, Optional

"""
Transforms the input grid based on the following rules:
1.  Identify a single, continuous horizontal or vertical separator line of azure (8) pixels that spans the grid.
2.  Initialize the output grid as a copy of the input grid.
3.  Identify source pixels: yellow (4) and red (2) pixels in the input grid.
4.  For each yellow source pixel found in the input, change its color to green (3) in the output grid at the corresponding location. Red source pixels remain red in the output grid.
5.  For each location corresponding to an original yellow or red source pixel:
    a.  Determine the direct orthogonal path from the pixel adjacent to the source pixel's location towards the separator line.
    b.  The path stops just before reaching the separator line (it does not include or overwrite the separator).
    c.  Iterate through the cells along this calculated path.
    d.  For each cell on the path, if its current color in the output grid is white (0), change its color to azure (8). Otherwise, leave the cell's color unchanged.
"""

def find_separator(grid: np.ndarray) -> Tuple[Optional[str], Optional[int]]:
    """
    Identifies the azure separator line/column.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple (orientation, index) where orientation is 'h' (horizontal)
        or 'v' (vertical), and index is the row or column index of the
        separator. Returns (None, None) if no single full separator is found.
    """
    rows, cols = grid.shape
    # Check for horizontal separator
    for r in range(rows):
        if np.all(grid[r, :] == 8):
            # Check if it's the only one
            is_unique = True
            for r2 in range(rows):
                if r != r2 and np.all(grid[r2, :] == 8):
                    is_unique = False
                    break
            if is_unique:
                 # Check if columns might also be separators
                 for c in range(cols):
                     if np.all(grid[:, c] == 8):
                         # Found both H and V separators, ambiguous or complex case not handled
                         return None, None
                 return 'h', r

    # Check for vertical separator
    for c in range(cols):
        if np.all(grid[:, c] == 8):
             # Check if it's the only one
            is_unique = True
            for c2 in range(cols):
                if c != c2 and np.all(grid[:, c2] == 8):
                    is_unique = False
                    break
            if is_unique:
                 # Already checked for H separators, so this must be the one if unique
                 return 'v', c

    return None, None


def draw_projection_path(output_grid: np.ndarray, r_start: int, c_start: int, sep_orientation: str, sep_index: int):
    """
    Draws the azure projection path from a source pixel towards the separator,
    only overwriting white (0) pixels in the output_grid. Modifies output_grid in place.

    Args:
        output_grid: The numpy array representing the output grid (modified in place).
        r_start: The row index of the source pixel's original location.
        c_start: The column index of the source pixel's original location.
        sep_orientation: 'h' or 'v' for the separator orientation.
        sep_index: The row or column index of the separator.
    """
    if sep_orientation == 'h':
        # Project vertically towards the horizontal separator at row sep_index
        if r_start < sep_index: # Project down from above
            for r in range(r_start + 1, sep_index):
                # Check if the path pixel is currently white (0) before drawing
                if output_grid[r, c_start] == 0:
                    output_grid[r, c_start] = 8
        elif r_start > sep_index: # Project up from below
            # Iterate from r_start-1 down to sep_index+1
            for r in range(r_start - 1, sep_index, -1):
                 # Check if the path pixel is currently white (0) before drawing
                 if output_grid[r, c_start] == 0:
                    output_grid[r, c_start] = 8
    elif sep_orientation == 'v':
        # Project horizontally towards the vertical separator at column sep_index
        if c_start < sep_index: # Project right from left
            for c in range(c_start + 1, sep_index):
                 # Check if the path pixel is currently white (0) before drawing
                 if output_grid[r_start, c] == 0:
                    output_grid[r_start, c] = 8
        elif c_start > sep_index: # Project left from right
            # Iterate from c_start-1 down to sep_index+1
            for c in range(c_start - 1, sep_index, -1):
                 # Check if the path pixel is currently white (0) before drawing
                 if output_grid[r_start, c] == 0:
                    output_grid[r_start, c] = 8


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify Separator
    separator_orientation, separator_index = find_separator(input_np)

    # If no valid separator is found, return the original grid (or handle as error)
    # Based on task structure, a separator is expected.
    if separator_orientation is None:
        # This case might indicate an unexpected input format or multiple separators.
        # Returning the input might be a safe default for ARC, but could be wrong.
        # Let's assume a separator always exists per the pattern.
        # If this fails tests, we might need to reconsider this assumption.
         return input_grid # Or raise an error, or return empty?

    # 2. Initialize Output grid as a copy
    output_np = input_np.copy()

    # 3. Identify Source Pixels and perform initial Color Changes
    source_pixel_locations = []
    for r in range(rows):
        for c in range(cols):
            # Skip pixels on the separator line itself
            if separator_orientation == 'h' and r == separator_index:
                continue
            if separator_orientation == 'v' and c == separator_index:
                continue

            pixel_value = input_np[r, c]
            if pixel_value == 4: # Yellow pixel
                # Change yellow to green in the output grid
                output_np[r, c] = 3
                # Record its location as a source for projection
                source_pixel_locations.append((r, c))
            elif pixel_value == 2: # Red pixel
                # Red remains red (already copied), just record its location
                source_pixel_locations.append((r, c))

    # 4. Draw Projection Paths for each identified source pixel
    for r_source, c_source in source_pixel_locations:
        draw_projection_path(output_np, r_source, c_source, separator_orientation, separator_index)

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_np.tolist()