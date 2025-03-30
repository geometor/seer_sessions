
Previous Code:
```python
"""
Transformation Rule Natural Language Description:

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each row of the grid.
3. For each row, check if a red (2) pixel exists at the beginning (column 0).
4. If a red pixel is found at the beginning:
    a. Search for the first azure (8) pixel in that row, starting from column 1 up to the second-to-last column.
    b. If an azure (8) pixel is found at column index 'stopper_col':
        i. Fill the cells in the output grid for the current row from column 1 up to (but not including) 'stopper_col' with azure (8).
        ii. Change the pixel at 'stopper_col' in the output grid to yellow (4).
    c. If no azure (8) pixel is found in the specified range:
        i. Fill the cells in the output grid for the current row from column 1 up to (but not including) the last column with azure (8).
    d. Proceed to the next row (do not check the right side if the left side had a red pixel).
5. If no red pixel was found at the beginning of the row (column 0), check if a red (2) pixel exists at the end (last column).
6. If a red pixel is found at the end:
    a. Search for the first azure (8) pixel in that row, scanning backwards from the second-to-last column down to column 0.
    b. If an azure (8) pixel is found at column index 'stopper_col':
        i. Fill the cells in the output grid for the current row from the last column minus one down to (but not including) 'stopper_col' with azure (8). (i.e., fill columns stopper_col + 1 to last_col - 1).
        ii. Change the pixel at 'stopper_col' in the output grid to yellow (4).
    c. If no azure (8) pixel is found in the specified range:
        i. Fill the cells in the output grid for the current row from column 0 up to (but not including) the last column with azure (8).
7. After checking all rows, return the modified output grid.
"""

import numpy as np

def find_stopper_left(row_data, start_col, end_col):
    """Finds the index of the first azure (8) pixel from left."""
    for c in range(start_col, end_col):
        if row_data[c] == 8:
            return c
    return -1 # Not found

def find_stopper_right(row_data, start_col, end_col):
    """Finds the index of the first azure (8) pixel from right."""
    for c in range(start_col, end_col - 1, -1): # Iterate backwards
        if row_data[c] == 8:
            return c
    return -1 # Not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Draws horizontal azure lines from red boundary pixels, stopping at or
    replacing azure pixels encountered in the path.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.array(input_grid, dtype=int)
    num_rows, num_cols = output_grid.shape

    # Iterate through each row
    for r in range(num_rows):
        row_data = output_grid[r, :]

        # Check for red pixel at the left edge (priority)
        if num_cols > 1 and row_data[0] == 2:
            # Find the stopper from left (column 1 to num_cols - 1)
            stopper_col = find_stopper_left(row_data, 1, num_cols)

            if stopper_col != -1:
                # Fill with azure up to the stopper
                output_grid[r, 1:stopper_col] = 8
                # Replace stopper with yellow
                output_grid[r, stopper_col] = 4
            else:
                # Fill with azure up to the right edge (exclusive)
                output_grid[r, 1:num_cols] = 8
            # If red was on the left, skip checking the right for this row
            continue

        # Check for red pixel at the right edge (only if no red on left)
        if num_cols > 1 and row_data[num_cols - 1] == 2:
            # Find the stopper from right (column num_cols - 2 down to 0)
            stopper_col = find_stopper_right(row_data, num_cols - 2, 0) # Check columns from second-last down to first

            if stopper_col != -1:
                 # Fill with azure from stopper+1 up to the right edge (exclusive)
                output_grid[r, stopper_col + 1 : num_cols - 1] = 8
                 # Replace stopper with yellow
                output_grid[r, stopper_col] = 4
            else:
                # Fill with azure from the left edge (inclusive) up to the right edge (exclusive)
                output_grid[r, 0 : num_cols - 1] = 8

    return output_grid.tolist() # Return as list of lists

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 8 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 8 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 4 0 0
2 0 0 0 0 0 0 0 0 0
2 8 8 8 8 4 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
8 8 8 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0 0 2
8 8 8 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 4 0 0
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 4 0 0 0 0
2 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 54
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 54.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
2 0 0 0 8 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
2 8 8 8 4 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 2
8 8 8 8 8 8 8 2
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8
2 8 8 8 4 0 0 0
2 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 42
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 55.26315789473685

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 8 0 0 2
0 0 8 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 8 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 4 8 8 2
0 0 4 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 4 8 8 8 8 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
2 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8 8 8
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 2
0 0 0 0 0 0 4 8 8 2
0 0 4 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
0 0 0 0 4 8 8 8 8 2
8 8 8 8 8 8 8 8 8 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 54
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 54.0
