
Previous Code:
```python
"""
Transforms an input grid into an output grid based on anchor-based (red=2, gray=5) horizontal propagation and mirroring.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find anchor pixels (red = 2)
    anchor_positions = np.where(input_grid == 2)
    anchor_rows = anchor_positions[0]
    anchor_cols = anchor_positions[1]

    anchor_col_map = {}  # map row number to list of anchor column positions
    for r,c in zip(anchor_rows, anchor_cols):
        if r not in anchor_col_map:
            anchor_col_map[r] = []
        anchor_col_map[r].append(c)

    # Iterate through rows
    for row in range(rows):
        if row in anchor_col_map:
            anchors = sorted(anchor_col_map[row])

            # process to left of first anchor
            first_anchor = anchors[0]
            for col in range(first_anchor):
                 # Check for gray anchor to the left, stop propagation
                if 5 in input_grid[row, :col+1]:
                    gray_anchor_pos = np.where(input_grid[row, :col+1] == 5)[0][-1] # get the rightmost gray
                    output_grid[row,col] = output_grid[row, col] # no change
                else:
                    output_grid[row, col] = _transform_left(input_grid[row, col])

            # process between anchors (mirroring)
            for i in range(len(anchors)-1):
                anchor1 = anchors[i]
                anchor2 = anchors[i+1]
                for col in range(anchor1+1, anchor2):
                    # mirrored position
                    input_val_index = anchor1 + (anchor2 - col)
                    # use transform_right rules for mirroring, but with corrected index
                    output_grid[row,col] = _transform_right(input_grid[row, input_val_index], input_grid, row, input_val_index)

            # process to right of last anchor
            last_anchor = anchors[-1]
            for col in range(last_anchor+1, cols):
                # Check for gray anchor to right, stop propagation
                gray_anchors_right = np.where(input_grid[row, last_anchor+1:] == 5)[0]
                if len(gray_anchors_right) > 0:
                    first_gray_anchor_right = gray_anchors_right[0] + last_anchor + 1
                    if col >= first_gray_anchor_right:
                        output_grid[row, col] = input_grid[row, col]  # No change past gray
                        continue  # Skip to the next column

                output_grid[row, col] = _transform_right(input_grid[row, col], input_grid, row, col)


        # Rows without red anchors remain unchanged (already handled by initializing output as a copy)

    return output_grid.tolist()

def _transform_left(input_val):
    # Transformation rules for left of anchor
    if input_val == 1:
        return 8
    elif input_val == 3:
        return 3
    elif input_val == 4:
        return 4
    elif input_val == 7:
        return 7
    else:
        return input_val

def _transform_right(input_val, input_grid, row, col):
    # Transformation rules for right of anchor
    if input_val == 1:
        return 8
    elif input_val == 4:
        # Check for any red anchors to the left within the current segment
        red_to_left = False
        for c in range(col):
          if input_grid[row, c] == 2:
            red_to_left = True
            break

        if red_to_left:
            return 4
        else:
            return 8
    elif input_val == 8:
        return 8
    elif input_val == 0:
        return 0
    elif input_val == 5:
        return 5
    else:
        return input_val
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 8
1 8 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 4 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 3 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 4 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
7 8 8 8 8 8 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 7 7 7 7 8 7 2 8 4 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 4 4 4 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 8 8 8 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 4 4 4 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 7 8 8 7 8 7 2 8 8 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 2 2 2 2 2 2 2 2 8 4 8
7 8 7 8 8 7 8 7 2 3 3 3 3 3 3 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 4 4 4 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 3 3 3 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 4 4 4 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 3 3 3 3 3 3 2 8 4 8
7 8 7 8 8 7 8 7 2 2 2 2 2 2 2 2 2 8 4 8
7 8 7 8 8 7 8 7 2 8 8 8 8 8 8 8 8 8 4 8
7 8 7 7 7 7 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
7 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 4 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 2 8 4 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 186
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 93.0

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 4 4 2 8 4 4 4 4 4 4 4 4
4 3 4 4 4 4 4 4 4 4 2 4 1 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 2 5 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 2 8 8 8 8 8 8 8 8 8
4 3 3 3 3 3 3 3 3 4 2 8 1 1 1 1 1 1 1 8
4 3 4 4 4 4 4 4 3 4 2 8 1 8 8 8 8 8 1 8
4 3 4 3 3 3 3 4 3 4 2 8 1 8 1 1 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 1 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 8 8 8 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 1 1 1 1 1 1 8
4 3 4 3 4 4 3 4 3 4 2 8 8 8 8 8 8 8 8 8
4 3 4 3 4 4 3 4 3 4 2 2 2 2 2 2 2 2 2 2
4 3 4 3 4 4 3 4 3 4 2 5 5 5 5 5 5 5 5 5
4 3 4 3 4 4 3 4 3 4 2 5 0 0 0 0 0 0 0 5
4 3 4 3 4 4 3 4 3 4 2 5 0 1 1 1 1 1 0 5
4 3 4 3 3 3 3 4 3 4 2 5 0 1 5 5 5 1 0 5
4 3 4 4 4 4 4 4 3 4 2 5 0 1 1 1 1 1 0 5
4 3 3 3 3 3 3 3 3 4 2 5 0 0 0 0 0 0 0 5
4 4 4 4 4 4 4 4 4 4 2 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 2 8 4 4 4 4 4 4 4 4
4 3 4 4 4 4 4 4 4 4 2 4 8 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 2 5 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 8 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 247
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 123.5
