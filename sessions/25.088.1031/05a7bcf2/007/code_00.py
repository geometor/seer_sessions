import numpy as np
from typing import List, Tuple, Optional

"""
Transforms the input grid based on the following rules:
1. Initialize the output grid as an identical copy of the input grid.
2. Find a single, continuous line (horizontal or vertical) of azure (8) pixels that fully spans the grid's width or height. Record its orientation and index. Assume such a unique separator exists.
3. Identify the locations of all yellow (4) and red (2) source pixels in the *input* grid that are not on the separator line.
4. For each identified *yellow* source pixel location `(r, c)`, change the color in the *output* grid at `(r, c)` to green (3). Red source pixels remain red in the output grid initially (due to the copy).
5. For *each* identified source pixel location `(r_source, c_source)` (both original yellow and red):
    a. Determine the direct orthogonal path from the cell adjacent to `(r_source, c_source)` towards the separator line.
    b. The path extends up to, but does not include, the separator line itself.
    c. Iterate through each cell `(r_path, c_path)` along this path.
    d. Change the color of the cell `(r_path, c_path)` in the *output* grid to azure (8), overwriting any existing color at that location.
"""

def find_separator(grid: np.ndarray) -> Tuple[Optional[str], Optional[int]]:
    """
    Identifies the unique azure separator line/column.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple (orientation, index) where orientation is 'h' (horizontal)
        or 'v' (vertical), and index is the row or column index of the
        separator. Returns (None, None) if no single full separator is found,
        or if both horizontal and vertical separators exist.
    """
    rows, cols = grid.shape
    h_sep_index = None
    v_sep_index = None
    azure_color = 8

    # Check for horizontal separator
    for r in range(rows):
        if np.all(grid[r, :] == azure_color):
            if h_sep_index is None: # Found the first one
                 h_sep_index = r
            else: # Found more than one horizontal separator
                 return None, None # Ambiguous case

    # Check for vertical separator
    for c in range(cols):
        if np.all(grid[:, c] == azure_color):
             if v_sep_index is None: # Found the first one
                 v_sep_index = c
             else: # Found more than one vertical separator
                 return None, None # Ambiguous case

    # Determine result based on findings
    if h_sep_index is not None and v_sep_index is None:
        return 'h', h_sep_index
    elif v_sep_index is not None and h_sep_index is None:
        return 'v', v_sep_index
    else:
        # Either none found, or both types found, or multiple of one type
        return None, None


def draw_projection_path(output_grid: np.ndarray, r_start: int, c_start: int, sep_orientation: str, sep_index: int):
    """
    Draws the azure projection path from a source pixel's original location
    towards the separator, overwriting existing pixels in the output_grid.
    Modifies output_grid in place.

    Args:
        output_grid: The numpy array representing the output grid (modified in place).
        r_start: The row index of the source pixel's original location.
        c_start: The column index of the source pixel's original location.
        sep_orientation: 'h' or 'v' for the separator orientation.
        sep_index: The row or column index of the separator.
    """
    azure_color = 8

    if sep_orientation == 'h':
        # Project vertically towards the horizontal separator at row sep_index
        if r_start < sep_index: # Project down from above
            # Path starts one step below the source, ends just before the separator
            for r in range(r_start + 1, sep_index):
                # Check bounds just in case, though path should be within grid
                if 0 <= r < output_grid.shape[0]:
                    output_grid[r, c_start] = azure_color # Overwrite with azure
        elif r_start > sep_index: # Project up from below
            # Path starts one step above the source, ends just after the separator
            # Iterate from r_start-1 down to sep_index+1
            for r in range(r_start - 1, sep_index, -1):
                 # Check bounds
                 if 0 <= r < output_grid.shape[0]:
                     output_grid[r, c_start] = azure_color # Overwrite with azure
    elif sep_orientation == 'v':
        # Project horizontally towards the vertical separator at column sep_index
        if c_start < sep_index: # Project right from left
            # Path starts one step right of the source, ends just before the separator
            for c in range(c_start + 1, sep_index):
                 # Check bounds
                 if 0 <= c < output_grid.shape[1]:
                     output_grid[r_start, c] = azure_color # Overwrite with azure
        elif c_start > sep_index: # Project left from right
            # Path starts one step left of the source, ends just after the separator
            # Iterate from c_start-1 down to sep_index+1
            for c in range(c_start - 1, sep_index, -1):
                 # Check bounds
                 if 0 <= c < output_grid.shape[1]:
                     output_grid[r_start, c] = azure_color # Overwrite with azure


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rules to the input grid: finds an azure separator,
    identifies red/yellow sources, changes yellow sources to green, and projects
    azure paths from all sources towards the separator.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Initialize Output grid as a copy
    output_np = input_np.copy()

    # 2. Find Separator
    separator_orientation, separator_index = find_separator(input_np)

    # Handle cases where no unique separator is found
    # Based on the previous timeout, maybe the assumption of a separator isn't always true,
    # or the implementation needs refinement. For now, returning the copy if no separator.
    if separator_orientation is None:
        return output_np.tolist()

    # Define source colors and target color for yellow sources
    yellow_color = 4
    red_color = 2
    green_color = 3
    source_colors = {yellow_color, red_color}

    # 3. Identify Source Pixels (locations only for now)
    source_pixel_locations = []
    for r in range(rows):
        for c in range(cols):
            # Determine if the current pixel is on the separator line
            is_on_separator = False
            if separator_orientation == 'h' and r == separator_index:
                is_on_separator = True
            elif separator_orientation == 'v' and c == separator_index:
                is_on_separator = True

            # If not on the separator and is a source color, record its location
            if not is_on_separator:
                pixel_value = input_np[r, c]
                if pixel_value in source_colors:
                    source_pixel_locations.append((r, c))

    # 4. Perform Initial Color Transformation for Yellow Sources
    # Iterate through the identified source locations
    for r_source, c_source in source_pixel_locations:
        # Check the color in the *original* input grid
        if input_np[r_source, c_source] == yellow_color:
            # Change the color in the *output* grid
            output_np[r_source, c_source] = green_color

    # 5. Draw Projection Paths for ALL identified source locations
    # This happens *after* initial color changes. Paths are drawn onto the output grid.
    for r_source, c_source in source_pixel_locations:
        draw_projection_path(output_np, r_source, c_source, separator_orientation, separator_index)

    # Convert the final NumPy array back to a list of lists
    return output_np.tolist()