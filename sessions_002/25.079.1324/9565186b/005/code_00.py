"""
1.  **Identify Azure Pixels:** Locate all pixels with color 8 (azure) in the input grid.

2.  **Define Segments:** For each azure pixel, define two "segments":
    *   **Row Segment:** Starting from the azure pixel, extend the segment to the left and right along the row. The segment continues as long as the pixels have the *same color as each other*, the segment terminates when the edge of the grid is reached or a pixel of a *different* color is encountered.
    *   **Column Segment:** Starting from the azure pixel, extend the segment upwards and downwards along the column. The segment continues as long as the pixels have the *same color as each other*, the segment terminates when the edge of the grid is reached or a pixel of a *different* color is encountered.

3.  **Conditional Replacement:**
    *   If a pixel is on a segment described in part 2, And if the segment's color is not 2 (Red), then change to color to 5 (grey).

4.  **Output:** The output grid is the result of applying these replacements. Pixels not part of any identified segment retain their original color.
"""

import numpy as np

def get_segment(grid, row, col, direction):
    """
    Gets a segment of pixels starting at (row, col) in the given direction.
    Direction: 0 for row, 1 for column.
    """
    rows, cols = grid.shape
    segment = []
    start_color = grid[row, col]
    
    if direction == 0:  # Row segment
        # Left
        for c in range(col, -1, -1):
            if grid[row, c] == start_color:
                segment.append((row, c))
            else:
                break
        # Right
        for c in range(col + 1, cols):
            if grid[row, c] == start_color:
                segment.append((row, c))
            else:
                break
    else:  # Column segment
        # Up
        for r in range(row, -1, -1):
            if grid[r, col] == start_color:
                segment.append((r, col))
            else:
                break
        # Down
        for r in range(row + 1, rows):
            if grid[r, col] == start_color:
                segment.append((r, col))
            else:
                break
    return segment

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify Azure Pixels
    azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                azure_pixels.append((r, c))

    # Define and process segments
    for r, c in azure_pixels:
        # Row segment
        row_segment = get_segment(input_grid, r, c, 0)
        first_color = -1
        if row_segment:
            first_color = input_grid[row_segment[0]]

        if first_color != 2:  # if segment color is not red
            for row, col in row_segment:
                output_grid[row, col] = 5

        # Column segment
        col_segment = get_segment(input_grid, r, c, 1)
        first_color = -1
        if col_segment:
            first_color = input_grid[col_segment[0]]

        if first_color != 2:   # if segment color is not red
            for row, col in col_segment:
                output_grid[row, col] = 5

    return output_grid