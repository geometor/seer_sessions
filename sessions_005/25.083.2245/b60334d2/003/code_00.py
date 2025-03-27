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
    rows_with_gray_or_blue = set()

    for row_index, row in enumerate(input_grid):
        gray_indices = get_gray_pixel_indices(row)

        if gray_indices:
            for col_index in gray_indices:
                # Horizontal Alternation - Left
                current_col = col_index
                color = 5
                while current_col >= 0:
                    output_grid[row_index, current_col] = color
                    rows_with_gray_or_blue.add(row_index)
                    color = 1 if color == 5 else 5
                    current_col -= 1
                # Horizontal Alternation - Right
                color = 1 # we already output the gray
                current_col = col_index + 1

                while current_col < output_grid.shape[1]:
                   output_grid[row_index, current_col] = color
                   rows_with_gray_or_blue.add(row_index)
                   color = 1 if color == 5 else 5
                   current_col += 1

    # Vertical Mirroring/Extension
    processed = set()
    for row_index in sorted(rows_with_gray_or_blue):
        for col_index in range(output_grid.shape[1]):
           if output_grid[row_index, col_index] in (1,5):

                # Extend Downwards, up to 2 additional
                next_row = row_index + 1
                if next_row < output_grid.shape[0] and (next_row,col_index -1) not in processed:
                        if col_index - 1 >= 0:
                           output_grid[next_row, col_index -1] = 1
                           processed.add((next_row, col_index -1))
                next_row = next_row+1

                if next_row < output_grid.shape[0] and (next_row, col_index -1) not in processed:
                    if col_index - 1 >= 0:
                        output_grid[next_row, col_index-1] = 1
                        processed.add((next_row,col_index -1))

    return output_grid