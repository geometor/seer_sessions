"""
Transformation Rule:
1. Identify the background color (most frequent) and the single foreground color in the input grid.
2. Count the total number of foreground pixels.
3. Determine the dimensions (height H, width W) of the grid.
4. Calculate the target row for the output line as the vertical middle row: row_index = floor((H - 1) / 2).
5. Calculate the length of the output line, which is equal to the count of foreground pixels (line_length).
6. Calculate the starting column for the output line to center it horizontally: start_col = floor((W - line_length) / 2).
7. Create a new output grid of the same dimensions as the input, filled entirely with the background color.
8. Draw a horizontal line of the foreground color in the output grid at the calculated row_index, starting from start_col and extending for line_length pixels.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Consolidates scattered pixels of a single foreground color into a centered horizontal line.
    """
    input_grid = np.array(input_grid)
    H, W = input_grid.shape

    # Find unique colors and their counts
    colors, counts = np.unique(input_grid, return_counts=True)

    # Identify background and foreground colors
    if len(colors) == 1:
        # If only one color exists, return the grid as is (or filled with that color)
        # Based on examples, seems there's always a foreground element.
        # If not, this might need adjustment based on specific task requirements.
        return input_grid.copy()

    # Assume the most frequent color is the background
    background_color_index = np.argmax(counts)
    background_color = colors[background_color_index]

    # Assume the other color is the foreground
    foreground_color = -1
    line_length = 0
    for i, color in enumerate(colors):
        if color != background_color:
            foreground_color = color
            line_length = counts[i]
            break # Assuming only one foreground color based on examples

    # If no foreground color found (shouldn't happen based on examples), return background grid
    if foreground_color == -1:
        return np.full((H, W), background_color, dtype=int)

    # Calculate the target row (vertical middle)
    row_index = (H - 1) // 2

    # Calculate the starting column for horizontal centering
    start_col = (W - line_length) // 2
    end_col = start_col + line_length # Exclusive end index for slicing

    # Create the output grid filled with the background color
    output_grid = np.full((H, W), background_color, dtype=int)

    # Draw the horizontal line
    # Ensure start/end columns are within grid bounds (might be needed for edge cases)
    start_col = max(0, start_col)
    end_col = min(W, end_col)

    if start_col < end_col: # Check if the line has positive length and fits
        output_grid[row_index, start_col:end_col] = foreground_color

    return output_grid.tolist() # Return as list of lists, as per ARC standard
