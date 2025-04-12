
## train_1

**input:**
```
0 4 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
4 4 4 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 4 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 7 0 0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
7 7 7 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
7 7 7 2 6 0 0 0 0 0 0 0 0 0 0 0 0 6
7 7 7 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
```


**output:**
```
0 0 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 4 0 0 0 0 0 0 0 3
0 0 0 2 4 0 0 0 4 4 4 0 0 0 0 0 0 4
0 0 0 2 3 0 0 0 0 4 7 7 0 0 0 0 0 3
0 0 0 2 7 0 0 0 0 7 7 7 0 0 0 0 0 7
0 0 0 2 3 0 0 0 0 7 7 7 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 6 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
```


## train_2

**input:**
```
0 5 0 0 3 4 4 7 4 5 4 7 4 4 4
5 0 5 0 3 4 0 0 0 0 0 0 0 0 4
0 5 0 0 3 7 0 0 0 0 0 0 0 0 7
8 0 0 0 3 4 0 0 0 0 0 0 0 0 4
0 8 0 0 3 4 0 0 0 0 0 0 0 0 4
0 0 8 0 3 5 0 0 0 0 0 0 0 0 5
0 7 0 0 3 4 0 0 0 0 0 0 0 0 4
7 7 7 0 3 7 0 0 0 0 0 0 0 0 7
0 7 0 0 3 4 0 0 0 0 0 0 0 0 4
0 0 0 0 3 4 4 7 4 5 4 7 4 4 4
```


**output:**
```
0 0 0 0 3 4 4 7 4 5 4 7 4 4 4
0 0 0 0 3 4 0 7 0 0 0 7 0 0 4
0 0 0 0 3 7 7 7 7 0 7 7 7 0 7
8 0 0 0 3 4 0 7 0 0 0 7 0 0 4
0 8 0 0 3 4 0 0 0 5 0 0 0 0 4
0 0 8 0 3 5 0 0 5 0 5 0 0 0 5
0 0 0 0 3 4 0 7 0 5 0 7 0 0 4
0 0 0 0 3 7 7 7 7 0 7 7 7 0 7
0 0 0 0 3 4 0 7 0 0 0 7 0 0 4
0 0 0 0 3 4 4 7 4 5 4 7 4 4 4
```


## train_3

**input:**
```
0 3 0 1 2 2 2 3 2 2 2 6 2 2
3 3 3 1 2 0 0 0 0 0 0 0 0 2
0 3 0 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 3 0 0 0 0 0 0 0 0 3
0 6 0 1 2 0 0 0 0 0 0 0 0 2
6 0 6 1 2 0 0 0 0 0 0 0 0 2
0 6 0 1 6 0 0 0 0 0 0 0 0 6
0 0 0 1 2 0 0 0 0 0 0 0 0 2
7 7 7 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 2 2 2 3 2 2 2 6 2 2
```


**output:**
```
0 0 0 1 2 2 2 3 2 2 2 6 2 2
0 0 0 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 2 0 0 3 0 0 0 0 0 2
0 0 0 1 3 0 3 3 3 0 0 0 0 3
0 0 0 1 2 0 0 3 0 0 0 0 0 2
0 0 0 1 2 0 0 0 0 0 0 6 0 2
0 0 0 1 6 0 0 0 0 0 6 0 6 6
0 0 0 1 2 0 0 0 0 0 0 6 0 2
7 7 7 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 2 2 2 3 2 2 2 6 2 2
```

## Perception

1.  **Input/Output Format:** Both input and output are 2D grids of numerical digits, likely representing colors where '0' is the background.
2.  **Grid Dimensions:** The output grid always has the same dimensions as the input grid.
3.  **Axis Column:** A key feature is a vertical column (the "axis") that is mostly preserved from input to output. Its horizontal position varies between tasks (col 3 in train_1, col 4 in train_2, col 3 in train_3). This column seems to act as a separator.
4.  **Value Column:** The column immediately to the right of the axis column (the "value column") in the input plays a crucial role. The value in this column for a given row determines how the right side of that output row is constructed.
5.  **Left Zone Modification:** The area to the left of the axis column in the input is mostly cleared (set to 0) in the output for the middle rows. There are some exceptions where parts of the left side are preserved, but the general rule seems to be clearing.
6.  **Right Zone Modification:** The area to the right of the axis column is significantly modified. For the middle rows, the output pattern seems determined by the value `C` found in the corresponding row of the "value column" (`input[row, axis_col + 1]`). It appears that each non-zero color `C` maps to a specific, predefined shape or "glyph" for that task. This glyph, using color `C` (and sometimes other colors specific to the glyph, like in train_2 and train_3), is drawn onto the right side of the output row, typically centered horizontally within the right zone. If `C` is 0, the right zone remains 0.
7.  **Boundary Rows:** The top and bottom rows of the grid seem to be treated specially: they are copied directly from the input to the output without modification.

## Facts

```yaml
objects:
  - name: input_grid
    properties:
      - grid of digits (colors)
      - height H
      - width W
  - name: output_grid
    properties:
      - grid of digits (colors)
      - height H
      - width W
  - name: axis_column
    properties:
      - vertical column in the grid
      - index: axis_col
      - largely preserved between input and output
      - separates left and right zones
  - name: value_column
    properties:
      - vertical column in the input grid
      - index: axis_col + 1
      - contains selector_color values
  - name: left_zone
    properties:
      - region of the grid
      - columns: 0 to axis_col - 1
  - name: right_zone
    properties:
      - region of the grid
      - columns: axis_col + 1 to W - 1
  - name: middle_rows
    properties:
      - rows: 1 to H - 2
  - name: boundary_rows
    properties:
      - rows: 0 and H - 1
  - name: selector_color
    properties:
      - color C found in input[row, value_column_index]
      - determines the glyph for the output right_zone
  - name: glyph_pattern
    properties:
      - predefined 1D pattern of colors associated with a selector_color C
      - specific to each task (train_1, train_2, train_3 have different glyph sets)
      - drawn into the output right_zone

actions:
  - name: identify_axis_column
    actor: system
    operates_on: input_grid
    description: Find the index (axis_col) of the vertical dividing column.
  - name: copy_column
    actor: system
    operates_on: input_grid, output_grid, axis_column
    description: Copy the axis_column from input to output.
  - name: copy_rows
    actor: system
    operates_on: input_grid, output_grid, boundary_rows
    description: Copy the top and bottom rows from input to output.
  - name: clear_zone
    actor: system
    operates_on: output_grid, left_zone, middle_rows
    description: Set the cells in the left_zone of middle_rows to 0.
  - name: select_color
    actor: system
    operates_on: input_grid, value_column, middle_rows
    description: Get the selector_color C for each middle row r from input[r, axis_col + 1].
  - name: retrieve_glyph
    actor: system
    operates_on: selector_color
    description: Look up the predefined glyph_pattern associated with the selector_color C for the current task.
  - name: draw_glyph
    actor: system
    operates_on: output_grid, right_zone, middle_rows, glyph_pattern
    description: Clear the right_zone and draw the retrieved glyph_pattern into the output row's right_zone, horizontally centered.

relationships:
  - type: spatial
    from: axis_column
    to: left_zone, right_zone
    description: axis_column separates left_zone and right_zone.
  - type: determination
    from: selector_color
    to: glyph_pattern
    description: The selector_color determines which glyph_pattern is used.
  - type: placement
    from: glyph_pattern
    to: output_grid, right_zone
    description: The glyph_pattern is placed within the right_zone of the output_grid.
  - type: preservation
    from: input_grid, boundary_rows
    to: output_grid, boundary_rows
    description: Boundary rows are preserved from input to output.
```

## Natural Language Program

1.  Initialize the `output_grid` with the same dimensions as the `input_grid`.
2.  Identify the vertical `axis_column` in the `input_grid` (this seems to be the first column from the left containing non-zero values that isn't part of a uniform border). Let its index be `axis_col`.
3.  Copy the entire `axis_column` from the `input_grid` to the `output_grid` at index `axis_col`.
4.  Copy the entire top row (row 0) and bottom row (row H-1) from the `input_grid` to the `output_grid`.
5.  For each middle row `r` (from row 1 to H-2):
    a.  Set all cells in the `left_zone` (columns 0 to `axis_col - 1`) of the `output_grid` at row `r` to 0 (background color).
    b.  Get the `selector_color` `C` from the `input_grid` at position (`r`, `axis_col + 1`).
    c.  Clear all cells in the `right_zone` (columns `axis_col + 1` to W-1) of the `output_grid` at row `r` to 0.
    d.  If `C` is not 0:
        i.  Retrieve the task-specific `glyph_pattern` associated with color `C`.
        ii. Calculate the starting column index to place the `glyph_pattern` so it is horizontally centered within the `right_zone` for row `r`.
        iii. Draw the `glyph_pattern` onto the `output_grid` at row `r` starting at the calculated column index.
```python
import numpy as np
import math

"""
Transforms the input grid based on task-specific rules determined by an axis column.

General Process:
1. Identify the vertical 'axis' column (first column where middle rows share the same non-zero value).
2. Copy top/bottom rows and the axis column from input to output.
3. For middle rows:
   - Clear the area left of the axis in the output (columns 0 to axis_col-1).
   - Copy the 'value column' (column axis_col + 1) from input to output.
   - Use the value in the value column (selector_color) to determine an action for the 'right zone' (columns from axis_col + 2 onwards) in the output row.
   - The action depends on the 'task context', identified by the value in the axis column.

Task Context Rules (axis_value -> selector_color -> action on right zone):
- Task 1 (axis=2): selector column = 3, right zone = 4 onwards
    - 4: Draw pattern [4,4,4] centered in the right zone.
    - 7: Draw pattern [7,7,7] centered in the right zone.
    - 6: Copy the value from the last column of the input row to the last column of the output row.
    - 3: Do nothing (leave right zone as 0s).
- Task 2 (axis=3): selector column = 4, right zone = 5 onwards
    - 4: Copy values from input row 0 at column indices [7, 9, 11] to the corresponding columns in the output row's right zone.
    - 7: Draw pattern [7,7,7,7, 0, 7,7,7] centered in the right zone.
    - 5: Draw pattern [5, 0, 5] centered in the right zone.
    - 3: Do nothing.
- Task 3 (axis=1): selector column = 2, right zone = 3 onwards
    - 3: Draw pattern [3,3,3] centered in the right zone.
    - 6: Draw pattern [6, 0, 6, 6] right-aligned in the right zone.
    - 2: Conditional copy: If the input row does not contain 7 left of the axis:
         Copy input[0, 7] to output[r, 7] (if 7 is in the right zone).
         Copy input[0, 11] to output[r, 11] (if 11 is in the right zone).
         The choice between 7 and 11 depends on the current row index r (r < 5 copies 7, r >= 5 copies 11).
    - 1: Do nothing.
"""

def find_axis_column(grid: np.ndarray) -> int:
    """
    Finds the index of the vertical axis column.
    The axis column is the first column 'j' such that grid[r, j]
    has the same non-zero value for all middle rows r (1 to H-2).
    Includes fallbacks for edge cases.
    """
    H, W = grid.shape
    # Handle grids too small to have middle rows (H<=2)
    if H <= 2:
        # Fallback: first column with any non-zero value in any row
        for j in range(W):
             if np.any(grid[:, j] != 0):
                 return j
        return 0 # If grid is all zeros

    middle_rows = grid[1:H-1, :]

    # Primary rule: Find first column with a single, non-zero value repeated
    # across all middle rows.
    for j in range(W):
        if W == 0: return 0 # Handle empty grid case inside loop
        # Need to handle case where middle_rows is empty or has 0 cols
        if middle_rows.shape[1] == 0: return 0
        col = middle_rows[:, j]
        unique_vals = np.unique(col)
        # Check if there's exactly one unique value AND it's non-zero
        if len(unique_vals) == 1 and unique_vals[0] != 0:
             return j

    # Fallback if primary rule fails: first col with any non-zero in middle rows
    for j in range(W):
        if np.any(middle_rows[:, j] != 0):
            return j

    # Absolute fallback if middle rows are all zeros or primary rule fails
    # Let's return 0 as a default axis if no clear one is found
    return 0

def solve(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    H, W = input_grid.shape
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Handle edge cases: empty or very small grids
    if H == 0 or W == 0:
        return []
    if H <= 2: # If 1 or 2 rows, copy input directly (consistent with examples)
        return input_grid_list

    # 1. Identify the axis column
    axis_col = find_axis_column(input_grid)

    # 2. Determine task context and define rules based on axis value
    # Use the value in the axis column (e.g., from the first middle row)
    axis_value = input_grid[1, axis_col]
    rules = {}
    if axis_value == 2: # Task 1 context (train_1)
        rules = {
            4: ('draw', [4,4,4], 'center'),
            7: ('draw', [7,7,7], 'center'),
            6: ('copy_last_col',),
            3: ('noop',)
        }
    elif axis_value == 3: # Task 2 context (train_2)
        rules = {
            4: ('copy_indices', 0, [7, 9, 11]),
            7: ('draw', [7,7,7,7, 0, 7,7,7], 'center'),
            5: ('draw', [5, 0, 5], 'center'),
            3: ('noop',)
        }
    elif axis_value == 1: # Task 3 context (train_3)
         rules = {
            3: ('draw', [3,3,3], 'center'),
            6: ('draw', [6, 0, 6, 6], 'right'),
            2: ('copy_conditional_row_index', 0, 7, 11, 5, 7), # src_row, idx1, idx2, row_threshold, prohibited_val_left
            1: ('noop',) # No action if selector is the axis value itself
        }
    # else: handle unexpected axis_value? For now, assume one of these contexts.

    # 3. Copy boundary rows (top and bottom)
    output_grid[0, :] = input_grid[0, :]
    output_grid[H-1, :] = input_grid[H-1, :]

    # 4. Process middle rows (r from 1 to H-2)
    for r in range(1, H - 1):
        # --- Part A: Copy preserved columns ---
        # Left zone is implicitly zeroed by initialization.

        # Copy axis column value
        if 0 <= axis_col < W:
            output_grid[r, axis_col] = input_grid[r, axis_col]

        # Copy value column (immediately right of axis) and get selector color
        selector_color = 0 # Default selector if no value column exists
        value_col = axis_col + 1
        if value_col < W:
             output_grid[r, value_col] = input_grid[r, value_col]
             selector_color = input_grid[r, value_col]

        # --- Part B: Apply rules to the right zone ---
        if selector_color in rules:
            action = rules[selector_color]
            rule_type = action[0]
            # Define the right zone (columns right of the value column)
            # This is where drawing/copying actions place their results.
            right_zone_start_col = axis_col + 2
            right_zone_end_col = W
            right_zone_width = right_zone_end_col - right_zone_start_col

            # Proceed only if there is a right zone (width > 0)
            if right_zone_width <= 0: continue

            # Execute action based on rule type
            if rule_type == 'draw':
                _, pattern, alignment = action
                pattern_arr = np.array(pattern)
                pattern_width = len(pattern_arr)

                # Skip if pattern is wider than the available zone
                if pattern_width > right_zone_width: continue

                # Calculate starting column offset *within* the right zone
                start_offset = 0
                if alignment == 'center':
                    start_offset = (right_zone_width - pattern_width) // 2
                elif alignment == 'right':
                    start_offset = right_zone_width - pattern_width

                # Calculate absolute column index in the output grid
                draw_start_col = right_zone_start_col + start_offset
                # Calculate end column, ensuring it doesn't exceed grid width
                draw_end_col = min(draw_start_col + pattern_width, W)
                # Calculate the actual length of the pattern segment to draw
                pattern_len_to_draw = draw_end_col - draw_start_col

                # Perform the draw if valid length
                if pattern_len_to_draw > 0:
                   # Slice the pattern array to match the destination length
                   output_grid[r, draw_start_col:draw_end_col] = pattern_arr[:pattern_len_to_draw]

            elif rule_type == 'copy_indices':
                _, source_row_idx, indices_to_copy = action
                for col_idx in indices_to_copy:
                    # Check source index validity
                    # Check target index validity AND ensure target is within the right zone
                    if 0 <= source_row_idx < H and 0 <= col_idx < W and col_idx >= right_zone_start_col:
                       output_grid[r, col_idx] = input_grid[source_row_idx, col_idx]

            elif rule_type == 'copy_last_col':
                 last_col_idx = W - 1
                 # Check last column index validity AND ensure target is within the right zone
                 if last_col_idx >= right_zone_start_col:
                    output_grid[r, last_col_idx] = input_grid[r, last_col_idx]

            elif rule_type == 'copy_conditional_row_index':
                _, src_row, idx1, idx2, row_thresh, prohibited_val = action
                # Check condition: prohibited value not present left of axis
                # Ensure axis_col > 0 before slicing left zone
                left_zone_exists = axis_col > 0
                condition_met = True # Assume condition met if no left zone
                if left_zone_exists:
                    left_zone = input_grid[r, 0:axis_col] # Slice up to axis_col (exclusive)
                    if prohibited_val in left_zone:
                        condition_met = False

                if condition_met:
                    # Determine target index based on row threshold
                    target_idx = idx1 if r < row_thresh else idx2
                    # Check source/target index validity & ensure target is within the right zone
                    if 0 <= src_row < H and 0 <= target_idx < W and target_idx >= right_zone_start_col:
                         output_grid[r, target_idx] = input_grid[src_row, target_idx]

            # 'noop' requires no action as the right zone remains 0 by default

    # 5. Convert final numpy array grid back to list of lists for the expected output format
    return output_grid.tolist()
```
