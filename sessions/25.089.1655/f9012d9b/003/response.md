```python
"""
Transforms an input grid based on the frequency counts of its non-white pixels.

1.  Identify all unique non-white colors (pixels with value != 0) present in the input grid.
2.  Count the occurrences (frequency) of each unique non-white color.
3.  If there are fewer than two distinct non-white colors, return an empty list [].
4.  Determine the color with the highest frequency (C1) and the color with the second highest frequency (C2). Record their counts: count(C1) and count(C2).
5.  Calculate the difference between the counts: diff = count(C1) - count(C2).
6.  Case 1: If diff is exactly 1:
    *   The output is a 1x1 grid containing the second most frequent color (C2).
7.  Case 2: If diff is greater than 1:
    *   The output is a 2x2 grid.
    *   Determine the majority color (majC) and minority color (minC) based on count parity:
        *   If count(C1) is odd and count(C2) is even, then majC = C1 and minC = C2.
        *   If count(C1) is even and count(C2) is odd, then majC = C2 and minC = C1.
        *   If both counts have the same parity (both odd or both even), default to majC = C1 and minC = C2.
    *   Determine the position for the single pixel of minC within the 2x2 grid:
        *   If minC was originally C2 (meaning C1 had the determining odd count, or it's the default case where C1 remains majority), place minC at row 1, column 0.
        *   If minC was originally C1 (meaning C2 had the determining odd count), place minC at row 1, column 1.
    *   Fill the remaining three cells of the 2x2 grid with majC.
8.  Return the constructed grid as a list of lists.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the transformation rule based on non-white color frequencies.
    """
    # Convert input to NumPy array for easier processing
    grid = np.array(input_grid, dtype=int)

    # Flatten the grid to easily count pixels
    pixels = grid.flatten()

    # Filter out white pixels (value 0)
    non_white_pixels = [p for p in pixels if p != 0]

    # Count the frequency of each non-white color
    color_counts = Counter(non_white_pixels)

    # Get sorted colors by frequency
    sorted_colors = color_counts.most_common()

    # Handle cases with fewer than two distinct non-white colors
    if len(sorted_colors) < 2:
        # Undefined behavior based on examples, returning empty list common in ARC
        return [] 

    # Get the top two colors and their counts
    c1, count1 = sorted_colors[0]
    c2, count2 = sorted_colors[1]

    # Calculate the difference in counts
    diff = count1 - count2

    # Case 1: Difference is exactly 1
    if diff == 1:
        # Output is 1x1 grid of the second most frequent color (C2)
        output_grid = np.array([[c2]], dtype=int)
    
    # Case 2: Difference is greater than 1
    elif diff > 1:
        # Determine majority (majC) and minority (minC) colors based on parity
        parity1_odd = count1 % 2 != 0
        parity2_odd = count2 % 2 != 0

        if parity1_odd and not parity2_odd:
            majC = c1
            minC = c2
            min_is_c2 = True
        elif not parity1_odd and parity2_odd:
            majC = c2
            minC = c1
            min_is_c2 = False
        else: # Same parity (both odd or both even) - default rule
            majC = c1
            minC = c2
            min_is_c2 = True # Default case treats minC as C2 for positioning

        # Create a 2x2 grid initialized with the majority color
        output_grid = np.full((2, 2), majC, dtype=int)

        # Determine the position of the minority color
        if min_is_c2:
            # If minC was C2 (or default), position is (1, 0)
            min_pos = (1, 0)
        else:
            # If minC was C1, position is (1, 1)
            min_pos = (1, 1)
            
        # Place the minority color at the determined position
        output_grid[min_pos] = minC

    else: 
        # This case (diff <= 0) shouldn't happen if C1 is strictly most frequent
        # but added for completeness. Return empty or handle as error.
        return []

    # Convert the final NumPy grid back to a list of lists
    return output_grid.tolist()
```