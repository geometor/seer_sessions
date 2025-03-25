"""
For each row in the input grid:

1.  Identify the leftmost azure (8) pixel. If no azure pixel exists in the row, skip the row.
2.  Identify all green (3) pixels in the row. If no green exists, skip to the next row.
3.  Identify all white/empty (0) pixels to the left of the leftmost azure (8) pixel.
4.  Iterate through the green (3) pixels. For each green pixel:
    *   Check if it's horizontally adjacent (immediately to the left or right) to *any* azure (8) pixel.
    *   If it's *not* horizontally adjacent, move it to the *leftmost available* white/empty (0) space to the left of the leftmost azure (8).
    *   If a green pixel is moved, replace it with an empty(0) in the original position.
5. Repeat steps 3 and 4.
"""

import numpy as np

def _is_horizontally_adjacent(grid, row, col, target_value):
    """Helper function to check horizontal adjacency."""
    _, cols = grid.shape
    if col > 0 and grid[row, col - 1] == target_value:
        return True
    if col < cols - 1 and grid[row, col + 1] == target_value:
        return True
    return False

def _find_leftmost_value(row, value):
    """Finds the index of the leftmost occurrence of a value in a row."""
    indices = np.where(row == value)[0]
    return indices[0] if indices.size > 0 else -1

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, _ = output_grid.shape

    for row_index in range(rows):
        row = output_grid[row_index]

        # 1. Find leftmost azure (8)
        leftmost_azure_index = _find_leftmost_value(row, 8)
        if leftmost_azure_index == -1:
            continue  # Skip row if no azure

        # 2. Find all green (3) pixels
        green_indices = np.where(row == 3)[0]
        if green_indices.size == 0:
            continue  # Skip if no green

        # 3. Find all empty (0) spaces to the left of leftmost azure
        empty_indices = []
        for i in range(leftmost_azure_index):
            if row[i] == 0:
                empty_indices.append(i)

        # 4. Iterate through green pixels and move
        empty_index_ptr = 0  # Pointer for the next available empty spot
        for green_index in green_indices:
            # Check horizontal adjacency to *any* azure
            if not _is_horizontally_adjacent(output_grid, row_index, green_index, 8):
                # Move to leftmost available empty space
                if empty_index_ptr < len(empty_indices):
                    output_grid[row_index, empty_indices[empty_index_ptr]] = 3
                    if empty_indices[empty_index_ptr] != green_index:  #don't set to zero if already at destination
                        output_grid[row_index, green_index] = 0
                    empty_index_ptr += 1

    return output_grid