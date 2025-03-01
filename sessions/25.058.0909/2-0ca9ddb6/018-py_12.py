"""
1.  **Preserve Magenta:** Copy all magenta (6) pixels from the input to the output without changes.
2.  **Identify Key Pixels**: A pixel is a "key" pixel if it is either blue (1) or red (2) AND has at least one adjacent (up, down, left, or right) white (0) pixel.
3.  **Expand Around Key Pixels**:
    *   If a key pixel is blue (1), change any adjacent white (0) pixels to orange (7).
    *   If a key pixel is red (2), change any adjacent white (0) pixels to yellow (4).
4.  **All Other Pixels**: Pixels that are not magenta and are not adjacent to a *key* pixel remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbor coordinates (up, down, left, right).
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_key_pixel(grid, row, col):
    """
    Checks if a pixel is a "key" pixel (blue or red with at least one white neighbor).
    """
    if grid[row, col] not in (1, 2):
        return False

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r, c] == 0:
            return True  # At least one white neighbor

    return False

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            # Preserve Magenta
            if input_grid[row, col] == 6:
                continue

            if is_key_pixel(input_grid, row, col):
                neighbors = get_neighbors(input_grid, row, col)
                if input_grid[row, col] == 1:  # Blue key pixel
                    for r, c in neighbors:
                        if input_grid[r, c] == 0:
                            output_grid[r, c] = 7  # Change to orange
                elif input_grid[row, col] == 2:  # Red key pixel
                    for r, c in neighbors:
                        if input_grid[r, c] == 0:
                            output_grid[r, c] = 4  # Change to yellow

    return output_grid