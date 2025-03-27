"""
Identifies whether the grid has uniform, non-white horizontal borders (top and bottom rows)
or vertical borders (left and right columns). For each green pixel (color 3) located
between these borders, its color is changed to the color of the nearest border.
Distance is measured orthogonally (row distance for horizontal borders, column distance
for vertical borders). If a green pixel is equidistant, it takes the color of the
top border (for horizontal) or the left border (for vertical). Other pixels remain unchanged.
"""

import numpy as np

def _check_uniform_color(line):
    """Checks if a 1D numpy array (row or column) has a single, non-zero color."""
    if line.size == 0:
        return None
    first_color = line[0]
    if first_color == 0:  # Check if the first color is white (background)
        return None
    if np.all(line == first_color):
        return first_color
    return None

def transform(input_grid):
    """
    Applies the border-proximity color transformation to green pixels.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    border_type = None
    color1 = None
    color2 = None
    start_row, end_row = 0, height
    start_col, end_col = 0, width

    # 1. Identify Horizontal Borders
    top_color = _check_uniform_color(input_np[0, :])
    bottom_color = _check_uniform_color(input_np[height - 1, :])
    if top_color is not None and bottom_color is not None:
        border_type = "horizontal"
        color1 = top_color
        color2 = bottom_color
        start_row, end_row = 1, height - 1 # Exclude border rows from iteration

    # 2. Identify Vertical Borders (only if horizontal not found)
    if border_type is None:
        left_color = _check_uniform_color(input_np[:, 0])
        right_color = _check_uniform_color(input_np[:, width - 1])
        if left_color is not None and right_color is not None:
            border_type = "vertical"
            color1 = left_color
            color2 = right_color
            start_col, end_col = 1, width - 1 # Exclude border columns from iteration

    # 3. Handle cases with no valid borders (return original grid)
    if border_type is None:
        return input_grid # Or raise an error, but examples imply borders exist

    # 4. Iterate and Transform Green Pixels within the bounds
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            # Check if the current pixel is green
            if input_np[r, c] == 3:
                if border_type == "horizontal":
                    # Calculate distance to top and bottom borders
                    dist1 = r # Distance from top row (index 0)
                    dist2 = height - 1 - r # Distance from bottom row (index height-1)
                    # Assign color of the closer border (or top if equidistant)
                    if dist1 <= dist2:
                        output_grid[r, c] = color1
                    else:
                        output_grid[r, c] = color2
                elif border_type == "vertical":
                    # Calculate distance to left and right borders
                    dist1 = c # Distance from left column (index 0)
                    dist2 = width - 1 - c # Distance from right column (index width-1)
                    # Assign color of the closer border (or left if equidistant)
                    if dist1 <= dist2:
                        output_grid[r, c] = color1
                    else:
                        output_grid[r, c] = color2

    # Convert back to list of lists before returning
    return output_grid.tolist()