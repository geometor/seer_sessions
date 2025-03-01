"""
1.  **Identify Yellow Rectangles:** Locate all rectangular regions outlined by color '4' (yellow) in the input grid.
2.  **Enumerate Rectangles:** Assign a sequence number to each identified rectangle from top to bottom based on their top-left corner's row index, starting with 1.
3.  **Fill Rectangles by Sequence Number:** Fill the inner regions (excluding the border) of the rectangles based on their sequence number:
    *   Odd-numbered rectangles: Fill with color '1' (blue).
    *   Even-numbered rectangles: Fill with color '2' (red).
4.  **Preserve Outline:** The outline of all rectangles (pixels with the initial color '4') should remain unchanged.
5.  **Output:** The output grid reflects these changes, maintaining the original background and the yellow outlines of the rectangles.
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

    # Sort objects by top-left corner's row.
    yellow_objects.sort(key=lambda x: x[0])

    for i, (min_row, min_col, max_row, max_col) in enumerate(yellow_objects):
        # Determine fill color based on sequence number (starting from 1).
        if (i + 1) % 2 != 0:  # Odd-numbered rectangle
            fill_color = 1  # Blue
        else:  # Even-numbered rectangle
            fill_color = 2  # Red

        # Fill inner area
        for row in range(min_row + 1, max_row):
            for col in range(min_col + 1, max_col):
                output_grid[row, col] = fill_color

    return output_grid