"""
1.  **Identify Rectangles:** Locate all rectangular regions of color '4' (yellow) on the input grid.
2.  **Separate Rectangles:** Distinguish the rectangles based on location (top and bottom).
3.  **Inner Fill (Top Rectangle):** For the top-most rectangle, change the color of the inner pixels (excluding the outline) to '1' (blue).
4.  **Inner Fill (Bottom Rectangle):** For the bottom-most rectangle, change the color of the inner pixels (excluding the outline) to '2' (red).
5. **Preserve Outline:** Do not modify the original outline of the rectangles. Maintain pixels of original rectangle color.
6. **Output:** The output grid should reflect these changes, preserving background.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds rectangular objects of a specified color in the grid.
    Returns a list of (min_row, min_col, max_row, max_col) tuples for each object.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                min_row, min_col = r, c
                max_row, max_col = r, c

                # Expand horizontally
                while max_col + 1 < cols and grid[r, max_col + 1] == color and not visited[r, max_col+1]:
                    max_col += 1

                # Expand vertically
                while max_row + 1 < rows and all(grid[max_row + 1, min_col:max_col + 1] == color) and not any(visited[max_row+1, min_col:max_col+1]):
                    max_row += 1

                # Mark visited
                for i in range(min_row, max_row+1):
                    for j in range(min_col, max_col + 1):
                        visited[i,j] = True
                
                objects.append((min_row, min_col, max_row, max_col))
    return objects


def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    yellow_objects = get_objects(input_grid, 4)

    # Sort objects by top-left corner's row, then column (to ensure top-to-bottom order).
    yellow_objects.sort(key=lambda x: (x[0], x[1]))

    for i, (min_row, min_col, max_row, max_col) in enumerate(yellow_objects):
        if i == 0:  # Top rectangle
            fill_color = 1
        elif i == 1:  # Bottom rectangle
            fill_color = 2
        else:
            fill_color = 0  #should not happen, but just in case

        # Fill inner area
        for row in range(min_row + 1, max_row):
            for col in range(min_col + 1, max_col):
                output_grid[row, col] = fill_color

    return output_grid