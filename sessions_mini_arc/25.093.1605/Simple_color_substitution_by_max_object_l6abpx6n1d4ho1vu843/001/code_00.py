"""
Transforms an input grid by swapping two specific colors: 
1. The color that appears exactly once (excluding 0).
2. The non-zero color that appears most frequently.
All other colors remain unchanged.
"""

import numpy as np
from collections import Counter

def _get_color_frequencies(grid):
    """Calculates the frequency of each non-zero color in the grid."""
    # Flatten the grid to easily count elements
    flat_grid = grid.flatten()
    # Count frequencies, excluding the background color 0
    counts = Counter(cell for cell in flat_grid if cell != 0)
    return counts

def _find_swap_colors(counts):
    """Identifies the unique color (count=1) and the most frequent color."""
    if not counts: # Handle empty grid or grid with only zeros
        return None, None

    color_1 = None
    color_2 = None
    max_freq = 0

    # Find the unique color (frequency 1)
    for color, freq in counts.items():
        if freq == 1:
            color_1 = color
            break # Assume only one such color based on examples

    # Find the most frequent color
    # If multiple colors have the same max frequency, the one encountered first (arbitrary) is chosen
    # Or, if the unique color (color_1) is also the most frequent (e.g., only one non-zero element), handle appropriately
    temp_counts = counts.copy()
    if color_1 is not None and color_1 in temp_counts:
         # Exclude color_1 when searching for color_2 if they are distinct
         # If color_1 *is* the most frequent, it will be picked below
         pass # No action needed here, logic below handles it

    max_freq = 0
    most_frequent_colors = []
    for color, freq in temp_counts.items():
        if freq > max_freq:
            max_freq = freq
            most_frequent_colors = [color]
        elif freq == max_freq:
             most_frequent_colors.append(color)

    # Select color_2. If color_1 is among the most frequent, pick another if possible.
    # If color_1 is the *only* most frequent color, it becomes color_2.
    if len(most_frequent_colors) == 1:
        color_2 = most_frequent_colors[0]
    else: # Tie in frequencies
        # Prioritize picking a color different from color_1 if possible
        found_other = False
        for c in most_frequent_colors:
            if c != color_1:
                color_2 = c
                found_other = True
                break
        if not found_other: # If color_1 is one of the tied most frequent, and no others exist
             color_2 = color_1 # Or could pick any, examples suggest they are distinct

    # Correction if color_1 wasn't found (e.g., no unique color)
    # Or if color_2 wasn't found (e.g., only zeros or all unique counts)
    # Based on examples, we expect both to be found and distinct.
    if color_1 is None or color_2 is None:
         # Handle edge cases not present in examples if needed.
         # For now, assume valid inputs based on examples.
         # A more robust implementation might raise an error or have default behavior.
         pass


    # Handle the case where the unique color is also the most frequent (e.g., only one non-zero element)
    # In this specific problem based on examples, color_1 and color_2 seem guaranteed to exist and be distinct.
    # If the grid had only one '8', counts = {8: 1}. color_1=8, color_2=8. Swap is a no-op.
    if len(counts) == 1:
        single_color = list(counts.keys())[0]
        if counts[single_color] == 1: # Only one non-zero element
             color_1 = single_color
             color_2 = single_color

    return color_1, color_2


def transform(input_grid):
    """
    Applies the color swapping transformation to the input grid.
    """
    # Convert input list of lists to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)

    # Calculate frequencies of non-zero colors
    frequencies = _get_color_frequencies(grid_np)

    # Identify the two colors to be swapped
    color_1, color_2 = _find_swap_colors(frequencies)

    # Initialize output_grid as a copy of the input
    output_grid = grid_np.copy()

    # If colors to swap weren't found or are the same, return the original grid copy
    if color_1 is None or color_2 is None or color_1 == color_2:
        return output_grid.tolist() # Return as list of lists

    # Perform the swap
    # Iterate through each cell and apply the swap logic
    rows, cols = grid_np.shape
    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] == color_1:
                output_grid[r, c] = color_2
            elif grid_np[r, c] == color_2:
                output_grid[r, c] = color_1
            # else: the value remains the same (already copied)

    # Return the transformed grid as a list of lists
    return output_grid.tolist()