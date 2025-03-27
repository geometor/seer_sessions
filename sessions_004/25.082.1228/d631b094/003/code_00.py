"""
1.  **Identify the Dominant Color:** Examine the input grid. The dominant color is the non-zero color that appears most frequently. If only one non-zero color is present, that is the dominant color.
2.  **Count Dominant Color Occurrences:** Determine the number of times the dominant color appears in the input grid.
3.  **Construct Output Grid:** Create a new output grid. The output grid will have one row. The number of columns is equal to the count of the dominant color.
4.  **Populate Output:** Fill every cell of the output grid with the dominant color.
"""

import numpy as np

def get_dominant_color(grid):
    """
    Finds the most frequent non-zero color in a grid.

    Args:
        grid: a numpy array
    Returns color or None
    """
    counts = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            val = grid[r,c]
            if val != 0:
                if val not in counts:
                    counts[val] = 0
                counts[val] += 1
    dominant_color = None
    max_count = 0
    for color, count in counts.items():
        if count > max_count:
            max_count = count
            dominant_color = color
    return dominant_color

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # Find the dominant non zero color
    dominant_color = get_dominant_color(input_grid)

    # Count the occurrences of dominant non-zero color
    count = 0
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == dominant_color:
                count += 1

    # construct and populate output
    output_grid = np.full((1, count), dominant_color)

    return output_grid.tolist()