"""
The transformation identifies gray pixels (value 5) in the input grid and generates an alternating pattern of gray and blue pixels in the output grid. The horizontal pattern starts from the gray pixels' positions, extending bidirectionally.  A vertical alternation occurs, extending the pattern downwards one row, creating a checkerboard pattern, but only immediately below rows with the horizontal gray/blue alternation. Rows that are all zeros in the input remain all zeros in the output.
"""

import numpy as np

def get_gray_pixel_indices(grid):
    """Finds the indices of gray (5) pixels in a row."""
    gray_indices = []
    for i, pixel in enumerate(grid):
        if pixel == 5:
            gray_indices.append(i)
    return gray_indices

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.zeros_like(input_grid)

    for row_index, row in enumerate(input_grid):
        gray_indices = get_gray_pixel_indices(row)

        # Preserve Empty Rows
        if not gray_indices:
            continue  # Skip to the next row if the current row is all zeros

        # Horizontal Alternation
        for col_index in gray_indices:
            # Leftward alternation
            current_col = col_index
            color = 5  # Start with gray
            while current_col >= 0:
                output_grid[row_index, current_col] = color
                color = 1 if color == 5 else 5  # Alternate colors
                current_col -= 1

            # Rightward alternation
            current_col = col_index + 1
            color = 1  # Start with blue (opposite of gray)
            while current_col < output_grid.shape[1]:
                output_grid[row_index, current_col] = color
                color = 1 if color == 5 else 5  # Alternate
                current_col += 1

        # Vertical Alternation (one row down)
        next_row_index = row_index + 1
        if next_row_index < output_grid.shape[0]: # boundary check
            
            for col_index in gray_indices:
                # leftward
                current_col = col_index
                color = 5
                while current_col >= 0:
                    if current_col - 1 >= 0:
                        output_grid[next_row_index, current_col -1] = 1
                    color = 1 if color ==5 else 5
                    current_col -= 1

                current_col = col_index + 1
                color = 1
                while current_col < output_grid.shape[1]:
                    if current_col -1 >= 0:
                        output_grid[next_row_index, current_col - 1] = 1
                    color = 1 if color == 5 else 5
                    current_col += 1

    return output_grid