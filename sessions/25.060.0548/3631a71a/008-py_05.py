"""
1.  **Identify and Remove the Maroon Block:** Locate the contiguous block of maroon (9) colored pixels in the input grid.  Remove all pixels within this block, setting their color to the background color (0).

2.  **Column-wise Conditional Shift:** For each column, iterate through the pixels from top to bottom. If a pixel is *not* the background color (0), check if there are any empty spaces (pixels with color 0) below it *within the same column*. If empty spaces exist below, shift the pixel downward to fill the *closest* empty space.  Maintain the relative vertical order of non-background pixels within each column. This means if pixel A was above pixel B before the shift, pixel A should remain above pixel B after the shift, unless they occupy the same vertical position.
"""

import numpy as np

def find_maroon_block(grid):
    """
    Finds the contiguous block of maroon pixels using a breadth-first search.
    """
    maroon_pixels = np.argwhere(grid == 9)
    if maroon_pixels.size == 0:
        return []

    start_pixel = tuple(maroon_pixels[0])
    block = set()
    queue = [start_pixel]

    while queue:
        current_pixel = queue.pop(0)
        if current_pixel in block:
            continue
        block.add(current_pixel)
        row, col = current_pixel

        # Check adjacent pixels (up, down, left, right)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 9 and (r, c) not in block:
                queue.append((r, c))

    return list(block)

def shift_pixels_down(column):
    """
    Shifts non-zero pixels down to the nearest empty space within a column,
    maintaining relative order.
    """
    new_column = np.zeros_like(column)
    non_zero_indices = np.nonzero(column)[0]
    non_zero_values = column[non_zero_indices]

    # Iterate from top to bottom
    target_index = 0
    for value in non_zero_values:
        while target_index < len(new_column) and new_column[target_index] != 0:
            target_index += 1
        if target_index < len(new_column):
             new_column[target_index] = value
             target_index+=1

    return new_column

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find and remove the maroon block
    maroon_block = find_maroon_block(output_grid)
    for row, col in maroon_block:
        output_grid[row, col] = 0  # Set to background color

    # Column-wise conditional shift
    for col in range(output_grid.shape[1]):
        # Extract the column
        column = output_grid[:, col]

        #Shift pixels in column
        new_column = shift_pixels_down(column)
        output_grid[:,col] = new_column


    return output_grid