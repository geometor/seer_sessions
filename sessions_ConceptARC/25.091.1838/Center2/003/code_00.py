"""
Selects a single color value from a 1xN input grid based on color frequency and median position of least frequent colors.
1. Extract the single row of colors from the input grid.
2. Count the occurrences of each unique color within this list.
3. Find the smallest occurrence count (the minimum frequency).
4. Identify all colors that appear exactly this minimum number of times.
5. Create a list containing the original 0-based indices from the color list where any of these least frequent colors occur.
6. Sort this list of positions numerically from smallest to largest.
7. Determine the median position within this sorted list of positions (index floor((n-1)/2)).
8. Retrieve the numerical value stored at this median position. This value is the target index within the original color list.
9. The final output is the single color value located at this target index in the original color list.
"""

import collections
import math
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described logic.
    Args:
        input_grid (list or np.array): A 2D grid, expected to be 1xN.
    Returns:
        int: The selected color value.
    """

    # Ensure input is usable, convert numpy array if necessary
    if isinstance(input_grid, np.ndarray):
        # Check if it's effectively a 1D array or a single row
        if input_grid.ndim == 1:
             input_list = input_grid.tolist()
        elif input_grid.shape[0] == 1:
             input_list = input_grid[0].tolist()
        elif input_grid.shape[1] == 1: # Handle Nx1 case as well
             input_list = input_grid.flatten().tolist()
        else:
             # Handle unexpected multi-row/multi-column cases if necessary
             # For now, assume the first row is the target if multiple rows exist
             # or raise an error, based on expected ARC behavior.
             # Let's try the first row for now.
             input_list = input_grid[0].tolist()
    elif isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         # Standard list of lists format
         if len(input_grid) == 1:
             input_list = input_grid[0]
         elif len(input_grid[0]) == 1: # Handle Nx1 list of lists
              input_list = [row[0] for row in input_grid]
         else:
             # Fallback to first row for multi-row list of lists
             input_list = input_grid[0]
    elif isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
        # Input might already be a flat list
        input_list = input_grid
    else:
        # Handle error case: invalid input format
        # Returning 0 (white) might be a safe default in ARC
        return 0


    # Step 1: Extract the single row of colors (handled above)
    # Handle empty list case
    if not input_list:
        return 0 # Return default color for empty input

    # Step 2: Count frequencies of each color
    color_counts = collections.Counter(input_list)

    # Handle case where counting might yield nothing (unlikely if input_list wasn't empty)
    if not color_counts:
        return 0

    # Step 3: Find the minimum frequency
    min_freq = min(color_counts.values())

    # Step 4: Identify all colors with the minimum frequency
    least_frequent_colors = {color for color, count in color_counts.items() if count == min_freq}

    # Step 5: Collect the indices of all occurrences of these least frequent colors
    indices = []
    for i, color in enumerate(input_list):
        if color in least_frequent_colors:
            indices.append(i)

    # Step 6: Sort the collected indices
    indices.sort()

    # Handle case where indices list might be empty (shouldn't happen if input_list wasn't empty and colors were found)
    if not indices:
        # Fallback behavior, perhaps return the first element? Or 0?
        return input_list[0] if input_list else 0

    # Step 7: Find the median index *position* within the sorted list of indices
    # For n elements, the median index in the sorted list is floor((n-1)/2)
    median_list_index_position = (len(indices) - 1) // 2

    # Step 8: Get the actual index *value* from the median position in the sorted list
    target_index_in_original_list = indices[median_list_index_position]

    # Step 9: Select the output color from the original input list at the target index
    output_color = input_list[target_index_in_original_list]

    # The task requires returning a single color value, not a grid.
    return output_color