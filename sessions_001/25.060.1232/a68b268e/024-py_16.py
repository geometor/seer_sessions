"""
1.  **Identify the Central Line:** Locate the vertical line of blue (1) pixels in the input grid. This line serves as a reference point.
2.  **Observe the pattern:** Starting immediately *after* the blue line, find the *first* occurrences of the colors orange (7), azure (8), yellow (4), and magenta (6), *in that order*.
3.  **Extract Selected Pixels**:  Record *only* these four pixels.
4.  **Construct Output Grid:** Create a grid of appropriate dimension, in this case 2x2, and arrange the selected pixels into the grid, row by row.
"""

import numpy as np

def find_central_blue_line(grid):
    # Find the vertical line of blue (1) pixels.
    rows, cols = grid.shape
    for j in range(cols):
        if all(grid[:, j] == 1):
            return j
    return -1  # Return -1 if no such line is found

def extract_pixels(grid):
    """Extracts pixels based on color and position relative to the central blue line."""
    central_line_x = find_central_blue_line(grid)
    rows, cols = grid.shape
    
    selected_pixels = []
    color_order = [7, 8, 4, 6]  # orange, azure, yellow, magenta
    color_index = 0

    if central_line_x != -1:  # Ensure a central line was found.
        for j in range(central_line_x + 1, cols): # start searching *after* blue line
            for i in range(rows):
                if grid[i,j] == color_order[color_index]:
                    selected_pixels.append(grid[i,j])
                    color_index += 1
                    if color_index == 4:
                        return selected_pixels
    return selected_pixels


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Extract relevant pixels.
    selected_pixels = extract_pixels(input_grid)

    # Create the output grid.  It will always be 2x2 based on training data
    output_grid = np.zeros((2, 2), dtype=int)

    # Fill output
    if len(selected_pixels) == 4:
        output_grid = np.array(selected_pixels).reshape(2, 2)
    else:
        return np.zeros((2,2), dtype=int) # Not enough to fill

    return output_grid