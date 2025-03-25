"""
1. Identify Input Grid Dimensions: Determine the height and width of the input grid.
2. Identify Non-Background Colors: Find all colors in the input grid that are *not* the most frequent color (the background color).
3. Extract Non-Background Sequence:
    *   Examine the input grid rows. If a row contains all the non-background colors, extract the order in which they appear in that row. This is the repeating sequence.
    *   If no row contains all non-background colors, try examining columns.
    *   If neither rows or cols work - examine last row, and assume order

4. Create Output Grid: Create an output grid with the same dimensions as the input grid.
5. Replicate and Fill: Fill the output grid by repeating the extracted non-background sequence. Start from the top-left corner ([0, 0]). For each cell, take the next color in the sequence. If the end of the sequence is reached, loop back to the beginning of the sequence. Continue this process, moving across each row and then down to the next row, until the entire output grid is filled. The sequence is replicated across rows and down columns, restarting the sequence at the beginning of each row/col if necessary.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Determines the background color based on frequency."""
    color_counts = Counter(grid.flatten())
    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

def get_non_background_sequence(grid):
    """Extracts the sequence of non-background colors."""
    background_color = get_background_color(grid)
    non_background_colors = [color for color in np.unique(grid) if color != background_color]

    # Try to find sequence in rows
    for row in grid:
        row_colors = [color for color in row if color != background_color]
        if len(set(row_colors)) == len(non_background_colors):  # Check if all non-bg colors are present
            # Check the order is consistent
            sequence = []
            valid = True
            for color in row_colors:
                if color in non_background_colors:
                    if not sequence or sequence[-1] != color:
                         sequence.append(color)

            if len(sequence) == len(non_background_colors):
                return sequence

    #if not found, try cols
    for col in grid.T:
        col_colors = [color for color in col if color != background_color]
        if len(set(col_colors)) == len(non_background_colors):
            sequence = []

            for color in col_colors:
                if color in non_background_colors:
                    if not sequence or sequence[-1] != color:
                        sequence.append(color)

            if len(sequence) == len(non_background_colors):
                return sequence


    #fall back on using the last row (or any row that contains them - if no row has them all this will still get them in order
    last_row_colors =  [color for color in grid[-1] if color != background_color]
    sequence = []
    for color in last_row_colors:
       if color in non_background_colors:
           if not sequence or sequence[-1] != color:
                sequence.append(color)

    return sequence

def transform(input_grid):
    """Transforms the input grid by replicating a non-background color sequence."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. & 2. Get Non-Background sequence
    sequence = get_non_background_sequence(input_grid)
    # 3. Create Output Grid
    output_grid = np.zeros_like(input_grid)

    # 4. Replicate and Fill
    seq_index = 0
    for r in range(rows):
        for c in range(cols):
            output_grid[r, c] = sequence[seq_index % len(sequence)]
            seq_index += 1

    return output_grid.tolist()