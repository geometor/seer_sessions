
Previous Code:
```python
import numpy as np

"""
Identify a unique horizontal or vertical line composed entirely of yellow pixels (4) 
that acts as a separator. This separator line is characterized by having 
"foreground pixels" (defined as pixels that are neither white (0) nor yellow (4)) 
strictly on one side of it (either above/below for horizontal, or left/right 
for vertical). Reflect the pattern formed by these foreground pixels (along with 
any white or yellow pixels within the source region) across the separator line 
into the target region, overwriting the original content of the target region. 
The separator line itself remains unchanged.
"""

def has_foreground(region, foreground_colors):
    """
    Checks if a given grid region contains any foreground pixels.
    Foreground pixels are those not in the foreground_colors set.
    Args:
        region (np.ndarray): The region of the grid to check.
        foreground_colors (set): A set of colors considered background/separator.
    Returns:
        bool: True if foreground pixels are present, False otherwise.
    """
    if region.size == 0: # Handle empty regions (e.g., above row 0)
        return False
    # Check if any pixel in the region is NOT in the foreground_colors set
    return np.any(~np.isin(region, list(foreground_colors)))

def transform(input_grid):
    """
    Transforms the input grid by reflecting a pattern across a unique yellow separator line.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape
    yellow = 4
    white = 0
    background_separator_colors = {white, yellow}

    # --- 1. Find potential horizontal and vertical separators ---
    h_separator_indices = [r for r in range(rows) if np.all(grid[r, :] == yellow)]
    v_separator_indices = [c for c in range(cols) if np.all(grid[:, c] == yellow)]

    # --- 2. Identify the unique primary separator ---
    separator_info = None # Will store ('horizontal'/'vertical', index, 'above'/'below'/'left'/'right')

    # Check horizontal candidates
    for r in h_separator_indices:
        region_above = grid[:r, :]
        region_below = grid[r+1:, :]
        
        pattern_above = has_foreground(region_above, background_separator_colors)
        pattern_below = has_foreground(region_below, background_separator_colors)

        # If pattern exists exclusively on one side, this is the separator
        if pattern_above and not pattern_below:
            separator_info = ('horizontal', r, 'above')
            break
        if not pattern_above and pattern_below:
            separator_info = ('horizontal', r, 'below')
            break
    
    # If no horizontal separator found, check vertical candidates
    if separator_info is None:
        for c in v_separator_indices:
            region_left = grid[:, :c]
            region_right = grid[:, c+1:]

            pattern_left = has_foreground(region_left, background_separator_colors)
            pattern_right = has_foreground(region_right, background_separator_colors)

            # If pattern exists exclusively on one side, this is the separator
            if pattern_left and not pattern_right:
                separator_info = ('vertical', c, 'left')
                break
            if not pattern_left and pattern_right:
                 separator_info = ('vertical', c, 'right')
                 break

    # --- 3. Perform reflection if a valid separator was found ---
    if separator_info:
        orientation, index, pattern_side = separator_info

        if orientation == 'horizontal':
            R = index
            if pattern_side == 'above':
                # Reflect region above (0 to R-1) to region below (R+1 onwards)
                for r in range(R):
                    for c in range(cols):
                        target_r = 2 * R - r
                        if 0 <= target_r < rows:
                            output_grid[target_r, c] = grid[r, c]
            else: # pattern_side == 'below'
                # Reflect region below (R+1 to end) to region above (0 to R-1)
                 for r in range(R + 1, rows):
                    for c in range(cols):
                        target_r = 2 * R - r
                        if 0 <= target_r < rows:
                             output_grid[target_r, c] = grid[r, c]

        elif orientation == 'vertical':
            C = index
            if pattern_side == 'left':
                 # Reflect region left (0 to C-1) to region right (C+1 onwards)
                 for r in range(rows):
                    for c in range(C):
                        target_c = 2 * C - c
                        if 0 <= target_c < cols:
                            output_grid[r, target_c] = grid[r, c]
            else: # pattern_side == 'right'
                 # Reflect region right (C+1 to end) to region left (0 to C-1)
                for r in range(rows):
                     for c in range(C + 1, cols):
                         target_c = 2 * C - c
                         if 0 <= target_c < cols:
                             output_grid[r, target_c] = grid[r, c]

    # --- 4. Return the result ---
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
0 2 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 2 0 0 0 5 5 0 0
0 0 2 0 0 0 0 2 0
0 0 1 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 5 0 2 0
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 7.017543859649123

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 8 0 0 3 0
0 7 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 8 0 0 3 0
0 7 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
```
Transformed Output:
```
0 7 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 34
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.83656509695291
