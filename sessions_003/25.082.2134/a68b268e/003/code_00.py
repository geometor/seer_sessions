"""
Transforms an input grid into a 4x4 output grid based on the following rules:

1.  Find the horizontal blue line (all 1s) in the input.
2.  The output grid's content comes from the first four columns of the section *above* the blue line.
3.  Initialize the output grid with the first four columns of the upper section.
4.  Iterate through each cell of the *output* grid:
    *   If the cell is black (0), replace it with the first non-black pixel in the *same* column of the section *below* the blue line in the original input grid.
    *   Otherwise, keep the cell's value.
5. The output will be 4x4
"""

import numpy as np

def find_blue_line(grid):
    """Finds the row index of the horizontal blue line."""
    for i, row in enumerate(grid):
        if all(pixel == 1 for pixel in row):
            return i
    return -1  # Should not happen

def transform(input_grid):
    input_grid = np.array(input_grid)
    blue_line_row = find_blue_line(input_grid)
    upper_section = input_grid[:blue_line_row, :4]  # First 4 cols above blue line
    lower_section = input_grid[blue_line_row + 1:]

    # Initialize the output grid (4x4)
    output_grid = np.zeros((4, 4), dtype=int)

    # Copy the first four columns of the upper section to initialize
    for i in range(min(4, upper_section.shape[0])): # handles cases where upper has < 4 rows
        for j in range(4):
           output_grid[i,j] = upper_section[i,j] if upper_section.shape[1] > j else 0

    # Replace black pixels
    for i in range(4):  # Iterate through rows of output
        for j in range(4):  # Iterate through cols of output
            if output_grid[i, j] == 0:
                # Find replacement in the lower section
                for k in range(lower_section.shape[0]):
                    if lower_section[k, j] != 0:
                        output_grid[i, j] = lower_section[k, j]
                        break  # Found the replacement

    return output_grid.tolist()