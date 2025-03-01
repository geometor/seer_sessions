"""
1.  **Identify the Pivot:** Find the vertical line composed of gray (5) pixels. This line serves as a potential axis of reflection.
2.  **Conditional Reflection:** For each row, examine the pixels to the right of the gray line.
    *   If a corresponding pixel exists to the left of the gray line (at the same distance from the gray line), and if that pixel color is different than the pixel on the right, then set the color of the cell to the left to be the same as the one on the right.
    * If a corresponding pixel does not exist to the left, extend the source pixel to the left.
3. If the cells on either side are the same, no action.
4. If there are two gray columns, treat as 1.
"""

import numpy as np

def find_gray_line(grid):
    # Find the column index of the vertical gray line.
    num_rows, num_cols = grid.shape
    for j in range(num_cols):
        if all(grid[i, j] == 5 for i in range(num_rows)):
            return j
    return -1  # Return -1 if no gray line is found

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Find the gray line index.
    gray_line_index = find_gray_line(input_grid)

    if gray_line_index == -1:
        return output_grid  # No gray line, return input as is

    # Iterate through rows and perform conditional reflection.
    for i in range(num_rows):
        for j in range(gray_line_index + 1, num_cols):
            distance_from_line = j - gray_line_index
            left_index = gray_line_index - distance_from_line

            if left_index >= 0:
                # Corresponding pixel exists
                if output_grid[i, j] != output_grid[i, left_index]:
                  output_grid[i, left_index] = output_grid[i, j]
            
            # If the gray line is at index 0, we need to handle potential
            # extension.
            elif gray_line_index < (num_cols-1):
                output_grid[i,left_index] = output_grid[i,j]

    return output_grid