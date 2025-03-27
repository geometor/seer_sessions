"""
Transforms an input grid into an output grid based on the following rules:

1.  **Identify "Anchor" Pixels:** Locate all pixels in the input grid with the color red (value 2). These act as primary anchor points for the transformation. Gray (value 5) acts as secondary anchors.

2.  **Process Rows with Anchors:**
    *   Iterate through each row of the input.
    *   If a row contains anchor pixels, process that row; otherwise, the row remains unchanged in the output.
    *   The red pixels remain unchanged in the output.

3. **Horizontal Propagation (Left of Anchor):**
   * Colors to the left of the leftmost red anchor are transformed based on a specific mapping, and propagated to the left edge of the grid.
       * input color 1 becomes 8
       * input color 3 becomes 3
       * input color 4 becomes 4
       * input color 7 becomes 7

4. **Horizontal Propagation (Right of Anchor):**
    *   Colors to the right of the rightmost red anchor in a row are handled, with transformations, to the right edge.
    * Input values to right of red anchors are transformed and propagated based on these rules.
       * input color 1 becomes 8
       * input color 4 becomes 8, unless there is a red pixel to the left, in which case it is 4
       * input color 8 becomes 8
       * input color 0 becomes 0
       * input color 5 becomes 5

5. **Horizontal Propagation (Between Anchors):**
    *  If there are multiple red anchors, colors between them.
        *  From the left anchor moving towards the right anchor.
        *  The color is determined based on the mirrored position of the value from the left anchor.

6. **Gray Anchor (5) Behavior:**
    * Gray pixels act as secondary anchors and also stop propagation

7.  **Process all Rows:** Ensure all rows have been processed and that un-processed rows remain the same.

"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find anchor pixels (red = 2)
    anchor_positions = np.where(input_grid == 2)
    anchor_rows = anchor_positions[0]
    anchor_cols = anchor_positions[1]

    anchor_col_map = {}
    for r,c in zip(anchor_rows, anchor_cols):
        if r not in anchor_col_map:
            anchor_col_map[r] = []
        anchor_col_map[r].append(c)

    # Iterate through rows
    for row in range(rows):
        if row in anchor_col_map:
            anchors = sorted(anchor_col_map[row])
            # print(f"row:{row} anchors: {anchors}")

            # process to left of first anchor
            first_anchor = anchors[0]
            for col in range(first_anchor):
                 # Check for gray anchor to the left
                if 5 in input_grid[row, :col+1]:
                    gray_anchor_pos = np.where(input_grid[row, :col+1] == 5)[0][-1]
                    output_grid[row,col] = output_grid[row, col]
                else:
                    output_grid[row, col] = transform_left(input_grid[row, col])

            # print(f"   left of {first_anchor} complete: {output_grid[row]}")


            # process between anchors
            for i in range(len(anchors)-1):
                anchor1 = anchors[i]
                anchor2 = anchors[i+1]
                for col in range(anchor1+1, anchor2):
                    input_val_index = anchor1 + (anchor2-col)
                    output_grid[row,col] = transform_right(input_grid[row, input_val_index], input_grid, row, col)
                # print(f"   middle {anchor1}-{anchor2} complete: {output_grid[row]}")

            # process to right of last anchor
            last_anchor = anchors[-1]
            for col in range(last_anchor+1, cols):
                input_val_index = last_anchor + (cols - col)
                if input_val_index >= cols:
                    input_val_index = cols - 1

                # Check for gray anchor
                if 5 in input_grid[row, last_anchor:col+1]:
                    gray_anchor_pos = np.where(input_grid[row,last_anchor:col+1] == 5)[0][0] + last_anchor
                    if col > gray_anchor_pos:
                        input_val_index = gray_anchor_pos + (col - gray_anchor_pos)
                        # print(f"   col: {col} gray at: {gray_anchor_pos}, using {input_val_index}")
                        output_grid[row,col] = transform_right(input_grid[row, input_val_index], input_grid, row, col)

                    else:
                        output_grid[row, col] = input_grid[row,col]

                else:
                    output_grid[row, col] = transform_right(input_grid[row, input_val_index], input_grid, row, col)
            # print(f"   right of {last_anchor} complete: {output_grid[row]}")

    return output_grid.tolist()

def transform_left(input_val):
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

def transform_right(input_val, input_grid, row, col):
    rows, cols = input_grid.shape

    if input_val == 1:
        return 8
    elif input_val == 4:
        if 2 in input_grid[row, col:]:
            return 4
        return 8
    elif input_val == 8:
        return 8
    elif input_val == 0:
        return 0
    elif input_val == 5:
        return 5
    else:
        return input_val