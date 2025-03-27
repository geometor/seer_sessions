"""
Transforms an input grid into an output grid based on the following rules:

1.  **Identify "Anchor" Pixels:** Locate all pixels in the input grid with the color red (value 2). These act as anchor points for the transformation.

2.  **Process Columns with Anchors:**
    *   Iterate through the input.
    *   The red pixels remain unchanged in the output.
    *   The colors to the left of the "anchor" pixels influence pixels to the left in output
    *   The colors to the right of the "anchor" pixels inflence pixels to the right in output.

3. **Horizontal Propagation/Mirroring (Left of Anchor):**
   * Consider input values to left of red anchors to be mirrored and changed by original color.
       * input color 1 becomes 8
       * input color 3 becomes 3
       * input color 4 becomes 4
       * input color 7 becomes 7
   * The mirroring continues to an outer edge or another anchor.

4. **Horizontal Propagation/Mirroring (Right of Anchor):**
   * Consider input values to right of red anchors to be mirrored and changed by original color.
       * input color 1 becomes 8
       * input color 4 becomes 8, unless there is a red pixel to the left, in which case it is 4
       * input color 8 becomes 8
       * input color 0 becomes 0
       * input color 5 becomes 5
   * The mirroring continues to an outer edge or another anchor.

5. Process all Columns:** Ensure all pixels have been assigned colors during processing.
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

                # print(f"input_val_index={input_val_index}")
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