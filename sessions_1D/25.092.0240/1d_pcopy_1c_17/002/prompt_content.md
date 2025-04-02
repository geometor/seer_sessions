
Previous Code:
```python
import numpy as np
import copy

def find_reference_line(grid):
    """
    Finds the topmost contiguous horizontal segment of non-white pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (color, row_index, min_col, max_col) or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        non_white_indices = np.where(grid[r] != 0)[0]
        if len(non_white_indices) > 0:
            # Check for contiguity (simple check: is the range of indices equal to the count?)
            min_c = np.min(non_white_indices)
            max_c = np.max(non_white_indices)
            
            # Extract the segment and check if all colors are the same and non-white
            segment = grid[r, min_c : max_c + 1]
            if np.all(segment != 0):
                 # More robust contiguity check: ensure no zeros within the min/max bounds
                if np.all(grid[r, min_c : max_c + 1] != 0):
                     # Check if all elements in the segment are the same color
                     if len(np.unique(segment)) == 1:
                          color = segment[0]
                          return color, r, min_c, max_c

    return None # No reference line found

def transform(input_grid_list):
    """
    Transforms the input grid based on the following rules:
    1. Find the topmost contiguous horizontal line of a single non-white color (the "reference line").
    2. Identify its color (C), row (R), start column (min_col), and end column (max_col).
    3. For each row below R (r > R):
       a. Check if any pixel in that row (in the input grid) has the color C.
       b. If yes, fill the segment in the output grid from (r, min_col) to (r, max_col) with color C.
       c. Otherwise, keep the row as it is.
    4. Rows R and above, and pixels outside the min_col to max_col range in rows below R (if not filled), remain unchanged.
    """
    input_grid = np.array(input_grid_list)
    output_grid = copy.deepcopy(input_grid)
    rows, cols = input_grid.shape

    # Find the reference line
    reference_info = find_reference_line(input_grid)

    if reference_info is None:
        # No reference line found, return the original grid
        return output_grid.tolist()

    color_c, row_r, min_col, max_col = reference_info

    # Iterate through rows below the reference line
    for r in range(row_r + 1, rows):
        # Check if any pixel in the current input row 'r' has color C
        trigger_found = False
        for c in range(cols):
            if input_grid[r, c] == color_c:
                trigger_found = True
                break # Found one, no need to check further in this row

        # If a trigger pixel was found, fill the corresponding segment in the output grid
        if trigger_found:
            for c_fill in range(min_col, max_col + 1):
                 # Ensure we don't write out of bounds, although min/max_col should be valid
                 if c_fill < cols:
                     output_grid[r, c_fill] = color_c

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 2 2 2 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 2 2 2 0 0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 2 2 2 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.0

## Example 2:
Input:
```
0 0 4 4 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 4 4 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.5

## Example 3:
Input:
```
0 0 5 5 5 0 0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 5 5 5 0 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 5 5 5 0 0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.0
