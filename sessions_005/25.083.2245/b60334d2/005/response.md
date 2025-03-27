```python
"""
The transformation identifies gray pixels in the input grid and generates an alternating pattern of gray and blue pixels in the output grid. The pattern starts from the gray pixels' positions, extending horizontally and vertically. Horizontal alternation involves placing gray and blue pixels (5, 1) bidirectionally from the original gray pixel positions. A vertical extension places blue pixels one row below and one row to the left of the gray/blue alternating pattern. Empty rows in the input remain empty.
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

        # Horizontal Alternation
        if gray_indices:
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

    # Vertical Extension
    for row_index, row in enumerate(input_grid):
        gray_indices = get_gray_pixel_indices(row)
        if gray_indices:
          for col_index in gray_indices:
            # re-process horizontal for vertical
            current_col = col_index
            color = 5  # Start with gray
            while current_col >= 0:
                # output_grid[row_index, current_col] = color # done above
                next_row = row_index + 1
                if next_row < output_grid.shape[0]:  # Check bounds
                  if current_col -1 >= 0:
                      output_grid[next_row, current_col - 1] = 1

                color = 1 if color == 5 else 5  # Alternate colors
                current_col -= 1
            current_col = col_index + 1
            color = 1
            while current_col < output_grid.shape[1]:
                # output_grid[row_index, current_col] = color
                next_row = row_index + 1
                if next_row < output_grid.shape[0]: # Check bounds
                  if current_col -1 >= 0:
                    output_grid[next_row, current_col - 1] = 1
                color = 1 if color == 5 else 5  # Alternate colors

                current_col += 1

    return output_grid
```