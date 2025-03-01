"""
1.  **Identify a Repeating Pattern:** Within the input grid, locate the largest repeating subgrid pattern. This subgrid can consist of any two or three colors.
2.  **Find a Border:** Identify a continuous horizontal line of pixels of the same color *above* the identified repeating pattern. This forms the top border.
3. **Find a Border:** Identify a continuous horizontal line of pixels of the same color *below* the identified repeating pattern. This forms the bottom border.
4.  **Extract:** Extract the subgrid that begins at the row of the top border and continues to the row of the bottom border, inclusive.
5.  **Output:** The extracted subgrid *is* the output.
"""

import numpy as np

def find_repeating_pattern(grid):
    """Finds the largest repeating subgrid pattern in the grid."""
    max_height = 0
    best_pattern = None
    top_row = -1
    pattern_start_col = -1

    for height in range(1, grid.shape[0]):
        for row in range(0, grid.shape[0] - height):
            for col in range(0, grid.shape[1]):
                pattern = grid[row:row + height, col:]
                # Check if this pattern repeats
                is_repeating = False
                next_row = row + height
                while next_row + height <= grid.shape[0]:
                    if np.array_equal(pattern, grid[next_row:next_row + height, col:]):
                        is_repeating = True
                        next_row += height
                    else:
                        break

                if is_repeating:
                  if height > max_height:
                    max_height = height
                    best_pattern = pattern
                    top_row = row
                    pattern_start_col = col
    return best_pattern, top_row, pattern_start_col


def find_border(grid, row, direction, pattern_width):
    """Finds a continuous horizontal line of the same color."""
    if direction == "above":
        start = row - 1
        step = -1
        end = -1
    elif direction == "below":
        start = row
        step = 1
        end = grid.shape[0]
    else:
        return -1

    for r in range(start, end, step):
        first_color = grid[r, 0]
        is_uniform = True
        # check that the row has uniform color
        for c in range(1, grid.shape[1]):
            if grid[r, c] != first_color:
                is_uniform = False
                break
        if is_uniform:
            return r  # Return the row index of the border
    return -1 # No border found


def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the repeating pattern and its location
    pattern, pattern_row, pattern_col = find_repeating_pattern(input_grid)

    # Handle case where no pattern is found
    if pattern is None:
        return []

    pattern_height, pattern_width = pattern.shape

    # Find top border
    top_border_row = find_border(input_grid, pattern_row, "above", pattern_width)
    if top_border_row == -1:
        return []

    # Find bottom border
    bottom_border_row = find_border(input_grid, pattern_row + pattern_height, "below", pattern_width)

    if bottom_border_row == -1:
      return []

    # Extract the subgrid
    output_grid = input_grid[top_border_row:bottom_border_row + 1, :]

    return output_grid