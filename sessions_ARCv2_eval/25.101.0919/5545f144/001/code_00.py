import numpy as np
from collections import Counter

"""
Transformation rule:
1. Determine the most frequent color in the input grid; this is the background color.
2. Scan the input grid column by column from left to right.
3. Identify the first column where all pixels share the same color, and this color is different from the background color. This column is the 'first separator line'.
4. Create the output grid by taking all rows and all columns from the input grid that are to the left of the 'first separator line'. The height of the output grid is the same as the input grid, and the width is equal to the column index of the 'first separator line'.
"""

def find_most_frequent_color(grid: np.ndarray) -> int:
    """Finds the most frequent color (pixel value) in the grid."""
    if grid.size == 0:
        return 0 # Default or raise error? Assuming default for now.
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts the portion of the input grid to the left of the first vertical
    separator line. A separator line is defined as a column where all pixels
    have the same color, and that color is different from the most frequent
    (background) color in the grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    if input_array.size == 0:
        return [] # Handle empty input

    rows, cols = input_array.shape

    # 1. Determine the background color
    background_color = find_most_frequent_color(input_array)

    # 2. & 3. Find the index of the first separator line
    separator_col_index = -1
    for c in range(cols):
        column = input_array[:, c]
        # Check if all elements in the column are the same
        if np.all(column == column[0]):
            column_color = column[0]
            # Check if the column color is different from the background color
            if column_color != background_color:
                separator_col_index = c
                break # Found the first separator

    # 4. Create the output grid
    if separator_col_index != -1:
        # Extract columns from the start up to the separator index
        output_array = input_array[:, :separator_col_index]
    else:
        # If no separator is found, return the original grid?
        # Based on examples, a separator seems guaranteed.
        # Let's return an empty grid or raise an error if no separator is found.
        # For now, we'll assume it's always found based on task description.
        # If it *could* be missing, returning input_array might be safer,
        # but let's stick to the pattern observed.
        # Returning empty list if no separator found.
         return [] # Or potentially input_grid based on interpretation

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid