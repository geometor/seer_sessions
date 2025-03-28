```python
import numpy as np
from typing import List, Dict, Tuple, Optional

"""
Identifies horizontal strips in the input grid separated by all-white rows. 
Calculates the sum of pixel values and the count of non-white pixels for each strip.
Selects a target strip based on the following criteria:
1. Primary: Maximum sum of pixel values.
2. Tiebreaker 1: Maximum count of non-white pixels among strips tied for maximum sum.
3. Tiebreaker 2: Topmost position (minimum starting row index) among strips still tied.

Currently, the function returns the selected strip *without modification*. 
This successfully reproduces the output for Example 1 but fails for Examples 2, 3, and 4, 
where the expected output is a modified version of the selected strip. 
The exact transformation rule preserving shape and non-white count but potentially altering 
pixel values and sum remains undetermined.
"""

def find_strips(grid: np.ndarray) -> list:
    """
    Identifies horizontal strips separated by all-white rows.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each containing a 'strip' (np.ndarray),
              'start_row' (int), and 'end_row' (int). Returns empty list
              if grid is empty or invalid.
    """
    if grid is None or grid.size == 0:
        return []
        
    height, width = grid.shape
    strips = []
    
    # Find indices of rows that are entirely white (0)
    separator_rows = [-1] # Virtual separator before the first row
    for r in range(height):
        if np.all(grid[r, :] == 0):
            separator_rows.append(r)
    separator_rows.append(height) # Virtual separator after the last row

    # Extract strips based on separators
    for i in range(len(separator_rows) - 1):
        start_row = separator_rows[i] + 1
        end_row = separator_rows[i+1]

        # Ensure the strip has at least one row
        if start_row < end_row:
            strip_array = grid[start_row:end_row, :]
            strips.append({
                'strip': strip_array,
                'start_row': start_row,
                'end_row': end_row
            })
            
    return strips

def calculate_strip_properties(strip_array: np.ndarray) -> Tuple[int, int]:
    """
    Calculates the sum of pixel values and the count of non-white pixels for a strip.

    Args:
        strip_array (np.ndarray): The strip grid.

    Returns:
        Tuple[int, int]: A tuple containing (sum_of_pixels, non_white_count).
    """
    strip_sum = np.sum(strip_array)
    non_white_count = np.count_nonzero(strip_array)
    return strip_sum, non_white_count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects a horizontal strip based on max sum, max non-white count, and topmost position.
    Note: Does not currently apply the final modification step needed for examples 2-4.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The selected horizontal strip as a list of lists.
                         Returns an empty list if no valid strips are found.
    """
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)

    if grid.size == 0:
        return []

    # 1. Identify Horizontal Strips
    identified_strips = find_strips(grid)

    if not identified_strips:
        return [] # No strips found

    # 2. Calculate Properties for each strip
    strips_data = []
    max_sum = -1
    for i, item in enumerate(identified_strips):
        strip_array = item['strip']
        strip_sum, non_white_count = calculate_strip_properties(strip_array)
        strips_data.append({
            'index': i,
            'strip': strip_array,
            'sum': strip_sum,
            'count': non_white_count,
            'start_row': item['start_row']
        })
        if strip_sum > max_sum:
            max_sum = strip_sum
            
    # 3. Select Target Strip based on criteria
    
    # Filter for max sum
    candidates = [s for s in strips_data if s['sum'] == max_sum]
    
    # Tiebreaker 1: Max non-white count
    if len(candidates) > 1:
        max_count_in_candidates = -1
        for c in candidates:
            if c['count'] > max_count_in_candidates:
                max_count_in_candidates = c['count']
        candidates = [c for c in candidates if c['count'] == max_count_in_candidates]
        
    # Tiebreaker 2: Topmost (min start_row)
    if len(candidates) > 1:
        # Sort candidates by start_row and pick the first one
        candidates.sort(key=lambda c: c['start_row'])
        
    # The first candidate after filtering/sorting is the selected one
    selected_strip_data = candidates[0]
    selected_strip_array = selected_strip_data['strip']

    # 4. Transform Selected Strip (Placeholder)
    # !!! This is where the unknown modification logic should go !!!
    # Currently, we just return the selected strip directly.
    # This works for Example 1 but not for 2, 3, 4.
    output_grid_array = selected_strip_array

    # 5. Output the result
    if output_grid_array is not None:
        # Convert the numpy array back to a list of lists for the output format
        return output_grid_array.tolist()
    else:
        # Should not happen if strips_data was populated
        return []
```