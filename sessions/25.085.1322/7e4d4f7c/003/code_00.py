import numpy as np
from collections import Counter

"""
1.  Create an output grid with 3 rows and the same width as the input grid.
2.  Copy the first row (index 0) of the input grid to the first row (index 0) of the output grid.
3.  Copy the second row (index 1) of the input grid to the second row (index 1) of the output grid. (This assumes the input grid always has at least 2 rows).
4.  Identify the 'background color':
    a.  Consider all pixels from the second row (index 1) downwards in the input grid.
    b.  Count the frequency of each color in this area.
    c.  Find the color(s) with the maximum frequency.
    d.  **Tie-breaking:** If there is more than one color with the maximum frequency, identify which of these tied colors are *not* present in the first row (index 0) of the input grid.
        i.  If exactly one tied color is *not* present in the first row, that color is the 'background color'.
        ii. If multiple tied colors are *not* present in the first row, the 'background color' is the one among them with the smallest numerical value.
        iii. If all tied colors *are* present in the first row, the 'background color' is the one among the originally tied colors with the smallest numerical value.
    e.  If there was only one color with the maximum frequency initially, that color is the 'background color'.
5.  Identify the 'target color':
    a.  Consider the first row (index 0) of the input grid.
    b.  Count the frequency of each color in this row.
    c.  Ignore the count for the identified 'background color'.
    d.  Find the color(s) with the maximum frequency among the remaining colors.
    e.  If one or more such colors exist, the 'target color' is the one with the smallest numerical value.
    f.  If no colors remain after ignoring the 'background color', there is no 'target color'.
6.  Construct the third row (index 2) of the output grid:
    a.  Take a copy of the first row (index 0) of the input grid.
    b.  If a 'target color' was identified in the previous step, replace all pixels matching the 'target color' in the copied row with magenta (color 6).
    c.  Assign this modified (or unmodified, if no target color was found) row to the third row (index 2) of the output grid.
"""

def find_background_color(input_grid: np.ndarray) -> int | None:
    """
    Identifies the background color based on frequency in rows 1+
    with specific tie-breaking rules involving row 0.
    """
    input_height, _ = input_grid.shape

    if input_height <= 1:
        return None # Not enough rows to determine background

    background_area = input_grid[1:, :].flatten()

    if background_area.size == 0:
        return None # Background area is empty

    counts = Counter(background_area)
    if not counts:
        return None # Should not happen if size > 0, but safety check

    max_freq = max(counts.values())
    most_frequent_colors = sorted([color for color, freq in counts.items() if freq == max_freq])

    if len(most_frequent_colors) == 1:
        # Case 4e: Only one most frequent color
        return most_frequent_colors[0]
    else:
        # Case 4d: Tie-breaking needed
        row0_colors = set(input_grid[0, :])
        
        # Identify tied colors NOT present in row 0
        candidates_after_exclusion = [color for color in most_frequent_colors if color not in row0_colors]

        if len(candidates_after_exclusion) == 1:
            # Case 4d.i: Exactly one tied color not in row 0
            return candidates_after_exclusion[0]
        elif len(candidates_after_exclusion) > 1:
            # Case 4d.ii: Multiple tied colors not in row 0 -> pick smallest
            return min(candidates_after_exclusion)
        else: # len(candidates_after_exclusion) == 0
            # Case 4d.iii: All tied colors are in row 0 -> pick smallest among original tied colors
            return min(most_frequent_colors)

def find_target_color(input_row_0: np.ndarray, background_color: int | None) -> int | None:
    """
    Identifies the target color in row 0, excluding the background color,
    using frequency and picking the smallest value in case of a tie.
    """
    if input_row_0.size == 0:
        return None

    counts_row0 = Counter(input_row_0)

    # Case 5c: Ignore the background color
    if background_color is not None and background_color in counts_row0:
        del counts_row0[background_color]

    if not counts_row0:
        # Case 5f: No colors left after excluding background
        return None

    # Case 5d: Find max frequency among remaining
    max_freq_row0 = max(counts_row0.values())
    target_candidates = sorted([color for color, freq in counts_row0.items() if freq == max_freq_row0])

    if not target_candidates:
         # Should not happen if counts_row0 is not empty, but safety check
         return None
    
    # Case 5e: Pick smallest numerical value if tie
    return min(target_candidates)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    input_height, input_width = input_grid.shape
    
    # Step 1: Initialize output_grid with 3 rows and same width
    # Use a default color like black (0) initially
    output_grid = np.zeros((3, input_width), dtype=int)

    # Step 2: Copy row 0
    output_grid[0, :] = input_grid[0, :]

    # Step 3: Copy row 1 (assuming height >= 2 as per examples)
    if input_height > 1:
        output_grid[1, :] = input_grid[1, :]
    # Else: output_grid[1, :] remains zeros, behavior for height=1 input is undefined by examples.

    # Step 4: Identify background color using helper function
    background_color = find_background_color(input_grid)

    # Step 5: Identify target color using helper function
    input_row_0 = input_grid[0, :]
    target_color = find_target_color(input_row_0, background_color)

    # Step 6: Construct row 2
    # 6a: Take a copy of input row 0
    output_row_2 = input_row_0.copy() 
    replacement_color = 6 # Magenta

    # 6b: Replace target color if found
    if target_color is not None:
        output_row_2[output_row_2 == target_color] = replacement_color

    # 6c: Assign to output grid
    output_grid[2, :] = output_row_2

    return output_grid