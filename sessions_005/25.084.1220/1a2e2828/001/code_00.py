import numpy as np
from collections import Counter

"""
Analyzes the input grid row by row to determine the output color.
The transformation follows these rules in order:
1.  Identify the first row (from top to bottom) that consists entirely of a single non-background color (color != 0). If such a row exists, the output is a 1x1 grid containing that color.
2.  If no row satisfies rule 1, identify the first row (from top to bottom) that contains exactly two distinct non-background colors. In this row, find the color that appears less frequently (the minority color). The output is a 1x1 grid containing this minority color.
"""

def transform(input_grid):
    """
    Transforms the input grid based on row color patterns.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: A 1x1 grid containing the determined output color.
    """
    # Convert input to a NumPy array for easier row manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- Check Primary Condition: Monochromatic non-background row ---
    for r in range(height):
        row = grid[r, :]
        # Get the first color in the row
        first_color = row[0]

        # Rule 1 applies only to non-background colors
        if first_color == 0:
            continue

        # Check if all elements in the row are the same as the first color
        is_monochromatic = True
        for pixel in row:
            if pixel != first_color:
                is_monochromatic = False
                break
        
        # If the row is monochromatic and not the background color, return it
        if is_monochromatic:
            # Found a monochromatic non-background row
            # Ensure output is standard list of lists with native int
            return [[int(first_color)]] 

    # --- Check Secondary Condition: Dichromatic non-background row, find minority color ---
    # This part is executed only if the primary condition was not met for any row
    for r in range(height):
        row = grid[r, :]
        
        # Filter out background color (0) to focus on relevant pixels
        non_background_pixels = [p for p in row if p != 0]

        # If there are no non-background pixels in this row, skip it
        if not non_background_pixels:
            continue

        # Count occurrences of each unique non-background color
        counts = Counter(non_background_pixels)
        unique_colors = list(counts.keys())

        # Check if there are exactly two distinct non-background colors
        if len(unique_colors) == 2:
            # Find the color with the minimum count (minority color)
            # If counts are equal, min() selects the first one encountered, which is acceptable
            minority_color = min(counts, key=counts.get)
            
            # Found the first row meeting the secondary condition
            # Ensure output is standard list of lists with native int
            return [[int(minority_color)]] 

    # Fallback case: If neither condition is met for any row.
    # Based on the provided examples, one of the conditions should always be met.
    # Returning a default or raising an error could be options.
    # For ARC tasks, often returning a simple grid like [[0]] might be expected if unsure.
    # However, given the examples always produce a result, this path shouldn't be reached.
    # If it were, it would indicate a misunderstanding or an edge case not covered.
    # Let's return [[0]] as a safe default, although unexpected.
    return [[0]] 