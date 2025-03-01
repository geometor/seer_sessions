"""
1.  **Identify:** Find all blue (1), red (2), and azure (8) pixels in the input grid.
2.  **Orange Rule:** For each blue (1) and red (2) pixel, examine its immediate neighbors (up, down, left, right). If a neighboring cell is empty (0), change it to orange (7).
3.  **Yellow Rule:** For each pair of blue (1) and azure (8) pixels:
    *   Check if they are in the same row or the same column.
    *   If they are in the same row or column, count the number of empty (0) cells between them.
    *  If there are three or more empty cells between them, place yellow pixels to complete the straight line connecting them
    *   If there are two or fewer empty cells between them, do *not* add any yellow pixels.
4.  **Copy:** All original pixels from the input that have not be changed, are copied.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in the grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    return neighbors

def find_pixels_by_color(grid, color):
    """Finds the positions of pixels of a specific color."""
    return np.argwhere(grid == color)

def count_empty_cells_between(grid, pos1, pos2):
    """Counts empty cells between two positions in the same row or column."""
    if pos1[0] == pos2[0]:  # Same row
        start = min(pos1[1], pos2[1]) + 1
        end = max(pos1[1], pos2[1])
        return np.sum(grid[pos1[0], start:end] == 0)
    elif pos1[1] == pos2[1]:  # Same column
        start = min(pos1[0], pos2[0]) + 1
        end = max(pos1[0], pos2[0])
        return np.sum(grid[start:end, pos1[1]] == 0)
    else:
        return -1  # Not in the same row or column

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find pixels of color 1, 2 and 8
    one_positions = find_pixels_by_color(input_grid, 1)
    two_positions = find_pixels_by_color(input_grid, 2)
    eight_positions = find_pixels_by_color(input_grid, 8)

    # Add orange (7) around 1s and 2s
    for pos in np.concatenate((one_positions, two_positions)):
        for r, c in get_neighbors(input_grid, pos[0], pos[1]):
            if output_grid[r, c] == 0:
                output_grid[r, c] = 7

    # Add yellow (4) between 1s and 8s
    for one_pos in one_positions:
        for eight_pos in eight_positions:
            empty_count = count_empty_cells_between(input_grid, one_pos, eight_pos)
            if empty_count >= 3:
                if one_pos[0] == eight_pos[0]:  # Same row
                    start = min(one_pos[1], eight_pos[1]) + 1
                    end = max(one_pos[1], eight_pos[1])
                    output_grid[one_pos[0], start:end] = 4
                elif one_pos[1] == eight_pos[1]:  # Same column
                    start = min(one_pos[0], eight_pos[0]) + 1
                    end = max(one_pos[0], eight_pos[0])
                    output_grid[start:end, one_pos[1]] = 4

    return output_grid