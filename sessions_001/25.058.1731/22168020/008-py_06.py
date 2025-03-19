"""
1.  **Identify Green Pixel Groups:** Divide the green pixels into groups based on their row indices. A new group starts if the row difference with the previous green pixel is greater than one, except if that difference == 2, then check if the difference between the next is 1, if so they belong in the same group.
2.  **Connect Within Groups:** For each group of green pixels:
    *   Find the minimum and maximum column indices (`min_col`, `max_col`).
    *   For each row within the group's range fill all cells between `min_col` and `max_col` (inclusive) with green.
"""

import numpy as np

def get_green_pixels(grid):
    """
    This method returns the positions of green pixels
    """
    green_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 3:
                green_pixels.append((row_idx, col_idx))
    return green_pixels

def group_green_pixels(green_pixels):
    """
    Groups green pixels based on row proximity.
    """
    groups = []
    if not green_pixels:
        return groups

    current_group = [green_pixels[0]]
    for i in range(1, len(green_pixels)):
        prev_pixel = green_pixels[i-1]
        curr_pixel = green_pixels[i]
        row_diff = curr_pixel[0] - prev_pixel[0]

        if row_diff > 1:
            if row_diff == 2:
                if i+1<len(green_pixels) and green_pixels[i+1][0]-curr_pixel[0] == 1:
                    current_group.append(curr_pixel)
                else:
                    groups.append(current_group)
                    current_group = [curr_pixel]
            else:
                groups.append(current_group)
                current_group = [curr_pixel]
        else:
            current_group.append(curr_pixel)

    groups.append(current_group)
    return groups

def transform(input_grid):
    """
    Connects green pixels horizontally in groups based on row proximity.
    """
    output_grid = np.copy(input_grid)
    green_pixels = get_green_pixels(input_grid)
    green_groups = group_green_pixels(green_pixels)

    # Connect within groups
    for group in green_groups:
        min_col = min(p[1] for p in group)
        max_col = max(p[1] for p in group)
        min_row = min(p[0] for p in group)
        max_row = max(p[0] for p in group)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                output_grid[row, col] = 3

    return output_grid