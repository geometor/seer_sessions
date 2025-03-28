```python
import numpy as np

"""
Identifies horizontal strips within the input grid, where strips are delimited by rows composed entirely of the white color (0). 
It calculates the number of non-white pixels (pixels with values 1-9) within each strip. 
The function then selects and returns the strip possessing the maximum count of non-white pixels. 
In cases where multiple strips share the same maximum count, the strip that appears highest (i.e., has the smallest starting row index) in the input grid is chosen.

Note: This logic successfully reproduces the output for Example 1 but fails for Examples 2, 3, and 4, where the expected output differs from the strip selected by this rule. The exact mechanism or transformation for those examples remains undetermined.
"""

def find_strips(grid: np.ndarray) -> list:
    """
    Identifies horizontal strips separated by all-white rows.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each containing a 'strip' (np.ndarray),
              'start_row' (int), and 'end_row' (int).
    """
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

def count_non_white_pixels(strip: np.ndarray) -> int:
    """
    Counts the number of non-white (non-zero) pixels in a strip.

    Args:
        strip (np.ndarray): The strip grid.

    Returns:
        int: The count of non-white pixels.
    """
    return np.count_nonzero(strip)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by selecting a horizontal strip based on pixel counts.

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
        return [] # No strips found (e.g., empty or all-white grid)

    # 2. Calculate Non-White Pixels for each strip
    strips_data = []
    for item in identified_strips:
        strip_array = item['strip']
        count = count_non_white_pixels(strip_array)
        strips_data.append({
            'strip': strip_array,
            'count': count,
            'start_row': item['start_row'] 
        })

    # 3. Select Target Strip (Max count, Topmost tiebreak)
    max_count = -1
    selected_strip = None
    
    # Find the maximum count first
    for data in strips_data:
        if data['count'] > max_count:
            max_count = data['count']
            
    # Find the first strip (topmost) that has the maximum count
    for data in strips_data:
        if data['count'] == max_count:
            selected_strip = data['strip']
            break # Stop after finding the first one (topmost)

    # 4. Output the selected strip
    if selected_strip is not None:
        # Convert the numpy array back to a list of lists for the output format
        return selected_strip.tolist()
    else:
        # This case should not be reached if strips_data was populated,
        # but included for robustness.
        return []
```