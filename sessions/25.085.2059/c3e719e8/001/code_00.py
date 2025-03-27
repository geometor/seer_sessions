import numpy as np
from collections import Counter

"""
Identifies the most frequent non-background color in the input grid.
Creates an output grid 3 times larger in each dimension, initialized with the background color (0).
Iterates through the input grid. If a pixel's color matches the most frequent color,
the entire input grid is copied into the corresponding block (scaled by input grid size) in the output grid.
Blocks corresponding to input pixels not matching the most frequent color remain filled with the background color.
"""

def find_most_frequent_color(grid, background_color=0):
    """
    Counts occurrences of each color in the grid, ignoring the background color,
    and returns the color with the highest frequency.
    In case of a tie, the color with the lower numerical value is chosen.
    """
    counts = Counter()
    # Flatten the grid and count non-background colors
    for color in grid.flatten():
        if color != background_color:
            counts[color] += 1

    if not counts:
        # Handle case where the grid only contains background color or is empty
        # The behavior isn't strictly defined by examples, but returning background
        # or a default seems reasonable. Let's default to background if no other color exists.
         # Or perhaps raise an error? Let's stick to the logic seen: if no target color, no copies.
         # So returning None or a special value might be best, or handle it in the caller.
         # For now, let's return None to indicate no target color found.
        return None

    # Find the maximum frequency
    max_freq = 0
    for color in counts:
        if counts[color] > max_freq:
            max_freq = counts[color]

    # Find all colors with the maximum frequency
    most_frequent_colors = []
    for color in counts:
        if counts[color] == max_freq:
            most_frequent_colors.append(color)

    # Return the one with the minimum numerical value in case of a tie
    return min(most_frequent_colors)


def transform(input_grid):
    """
    Transforms the input grid based on replicating it according to the positions
    of its most frequent non-background color.
    """
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape
    background_color = 0

    # 1. Find the most frequent non-background color
    target_color = find_most_frequent_color(input_np, background_color)

    # 2. Calculate output dimensions and initialize output grid
    output_H = H * 3
    output_W = W * 3
    output_grid = np.full((output_H, output_W), background_color, dtype=int)

    # If no non-background color was found, return the empty (background-filled) grid
    if target_color is None:
        return output_grid.tolist() # Return as list of lists per ARC format

    # 3. Iterate through the input grid
    for r in range(H):
        for c in range(W):
            # 4. Check if the current input pixel matches the target color
            if input_np[r, c] == target_color:
                # 5. Calculate the top-left corner for the block in the output grid
                start_row = r * H
                start_col = c * W
                end_row = start_row + H
                end_col = start_col + W

                # 6. Copy the entire input grid to the calculated block
                output_grid[start_row:end_row, start_col:end_col] = input_np

    # Return the resulting grid as a list of lists
    return output_grid.tolist()