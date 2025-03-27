```python
import numpy as np
from collections import Counter

def find_limit_row(grid):
    """
    Finds the index of the first row that consists entirely of gray (5) or white (0) pixels.
    Returns grid height if no such row is found.
    """
    h, w = grid.shape
    for r in range(h):
        row = grid[r, :]
        # Check if all elements in the row are either 0 or 5
        if np.all((row == 5) | (row == 0)):
            # Further check if the row is *only* 0s or *only* 5s
            if np.all(row == 5) or np.all(row == 0):
                 return r
    return h # If no such row found, limit is the grid height

def find_target_row(grid):
    """
    Finds the index of the last row that consists entirely of white (0) pixels.
    Raises ValueError if no such row is found.
    """
    h, w = grid.shape
    target_r = -1
    for r in range(h - 1, -1, -1): # Iterate backwards from the second last row
        if np.all(grid[r, :] == 0):
            target_r = r
            break # Found the last all-white row

    if target_r == -1:
         raise ValueError("No all-white row found in the input grid.")

    return target_r

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify the 'active region': rows above the first row containing only gray (5) or white (0).
    2. Count the frequency of non-white (0) and non-gray (5) colors in the active region.
    3. Determine the most frequent color ('target_color'). Assumes a unique max based on examples.
    4. Find the middle column index ('mid_col').
    5. Find the row index of the last row containing only white (0) ('target_row').
    6. Place the 'target_color' at the position ('target_row', 'mid_col') in a copy of the input grid.
    """
    # Convert input list of lists to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the original input is unchanged
    output_grid = np.copy(input_np)
    h, w = input_np.shape

    # 1. Find the limit row defining the bottom boundary of the active region.
    # The active region consists of rows above this limit.
    limit_row = find_limit_row(input_np)

    # Handle edge case where the active region might be empty (e.g., first row is gray/white)
    if limit_row == 0:
        # The examples don't cover this specific scenario.
        # Based on the observed pattern, if there's no active region, no change occurs.
        return output_grid.tolist()

    # 2. Define the active region and count color frequencies within it.
    # Exclude white (0) and gray (5) from the count.
    active_region = input_np[0:limit_row, :]
    color_counts = Counter()
    for r in range(active_region.shape[0]):
        for c in range(active_region.shape[1]):
            color = active_region[r, c]
            if color != 0 and color != 5: # Ignore white and gray pixels
                color_counts[color] += 1

    # 3. Determine the most frequent color in the active region.
    # Handle edge case where there are no countable colors in the active region.
    if not color_counts:
         # No non-white/non-gray colors found. Assume no change based on task structure.
         return output_grid.tolist()

    # Find the color with the maximum frequency.
    # Based on the provided examples, there seems to be a unique most frequent color.
    # Counter.most_common(1) efficiently gets the most frequent item.
    target_color = color_counts.most_common(1)[0][0]

    # 4. Calculate the middle column index. Integer division handles both odd and even widths.
    mid_col = (w - 1) // 2

    # 5. Find the target row index, which is the last row composed entirely of white pixels.
    try:
        target_row = find_target_row(input_np)
    except ValueError as e:
        # If the required all-white row structure isn't found, we cannot apply the rule.
        # Return the original grid as per the logic of not changing if conditions aren't met.
        # print(f"Warning: {e}. Required grid structure not found. Returning original grid.")
        return output_grid.tolist()

    # 6. Modify the output grid by placing the target color at the calculated position.
    output_grid[target_row, mid_col] = target_color

    # Convert the result back to a list of lists as required by the ARC format
    return output_grid.tolist()
```