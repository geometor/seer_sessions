```python
"""
Transforms an input grid into an output grid based on anchor-based (red=2, gray=5) horizontal propagation. Propagation direction and color changes depend on relative position to red anchors and interaction with gray anchors.
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

            # process between anchors (NO mirroring)
            for i in range(len(anchors)-1):
                anchor1 = anchors[i]
                anchor2 = anchors[i+1]
                for col in range(anchor1+1, anchor2):
                    # Check for gray anchor
                    if input_grid[row, col] == 5:
                      continue # no change if gray
                    
                    output_grid[row,col] = _transform_between(input_grid[row, col], input_grid, row, anchor1, anchor2)

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
        return 7
    elif input_val == 3:
        return 3
    elif input_val == 4:
        return 4
    elif input_val == 7: # added based on observation, propagate 7
        return 7
    else:
        return input_val

def _transform_right(input_val, input_grid, row, col):
    # Transformation rules for right of anchor
    if input_val == 1:
        return 8
    elif input_val == 4:
        return 8 # Always change 4 to 8 to right
    elif input_val == 8:
        return 8
    elif input_val == 0:
        return 0
    elif input_val == 5:
        return 5
    else:
        return input_val

def _transform_between(input_val, input_grid, row, anchor1, anchor2):
    if input_val == 1:
      return 1
    elif input_val == 3:  # propagate 3 to left
        return 3
    elif input_val == 4:
        return 4 # change 4 between
    if input_val == 0:
      return 0

    # check left neighbor, propagate left
    left_neighbor = input_grid[row, anchor1 + 1]
    if left_neighbor == 3:
      return 3

    return input_val
```