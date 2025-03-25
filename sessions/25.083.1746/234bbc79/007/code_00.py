"""
Transforms an input grid based on vertical and horizontal color propagation rules,
triggered by the interaction of red, gray, and other colored pixels. The grid
is then shrunk to fit the remaining non-white pixels.
"""

import numpy as np

def get_vertical_groups(grid):
    """
    Groups vertically adjacent pixels of non-white colors.
    """
    groups = []
    for j in range(grid.shape[1]):
        current_group = []
        for i in range(grid.shape[0]):
            if grid[i, j] != 0:  # Non-white pixel
                current_group.append((i, j, grid[i, j]))
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
        if current_group:  # Add any remaining group in the column
            groups.append(current_group)
    return groups

def get_neighbors(grid, row, col):
    """
    Gets the immediate neighbors (up, down, left, right) of a pixel.
    """
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col, grid[row - 1, col]))  # Up
    if row < grid.shape[0] - 1:
        neighbors.append((row + 1, col, grid[row + 1, col]))  # Down
    if col > 0:
        neighbors.append((row, col - 1, grid[row, col - 1]))  # Left
    if col < grid.shape[1] - 1:
        neighbors.append((row, col + 1, grid[row, col + 1]))  # Right
    return neighbors

def shrink_grid(grid):
    """
    Shrinks the grid to the smallest bounding box containing all non-white pixels.
    """
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    min_row, max_row = np.where(rows)[0][[0, -1]] if np.any(rows) else (0,0)
    min_col, max_col = np.where(cols)[0][[0, -1]] if np.any(cols) else (0,0)
    return grid[min_row : max_row + 1, min_col : max_col + 1]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)

    # 1. Vertical Propagation
    vertical_groups = get_vertical_groups(input_grid)
    for group in vertical_groups:
        for i, (row, col, color) in enumerate(group):
            if color == 2:  # Red pixel
                gray_above = False
                trigger_pixel = None

                for i_above in range(i):
                    row_above, col_above, color_above = group[i_above]
                    if color_above == 5:  # Gray pixel above
                        gray_above = True
                        for i_trigger in range(i_above):
                            row_trigger, col_trigger, color_trigger = group[i_trigger]
                            if color_trigger not in [0, 2, 5]:  # Trigger pixel found
                                trigger_pixel = (row_trigger, col_trigger, color_trigger)
                                break
                        if trigger_pixel:
                          break #found trigger, don't check for other grey

                if gray_above and trigger_pixel:
                    output_grid[row, col] = trigger_pixel[2]  # Propagate color down
                    output_grid[trigger_pixel[0], trigger_pixel[1]] = 0 #clear trigger
                    #clear grey pixels
                    for i_clear in range(i):
                      row_clear, col_clear, color_clear = group[i_clear]
                      if(color_clear == 5):
                        output_grid[row_clear, col_clear] = 0

    # 2. Horizontal Replacement
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 2:  # Remaining red pixel
                neighbors = get_neighbors(output_grid, i, j)
                for neighbor_row, neighbor_col, neighbor_color in neighbors:
                    if neighbor_color not in [0, 2, 5]:
                        output_grid[i, j] = neighbor_color
                        break  # Replace with the first valid neighbor

    # 3. Grid Shrinking
    output_grid = shrink_grid(output_grid)

    return output_grid