
## train_1

**input:**
```
4 2 2 3 3
0 0 0 0 3
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
4 2 2 3 3
0 0 0 0 3
0 0 0 0 4
0 0 0 0 4
0 0 0 4 4
```


## train_2

**input:**
```
1 5 5 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
1 5 5 1 1
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
3 7 7 5 5
0 0 0 0 5
0 0 0 0 1
0 0 0 0 1
0 0 0 1 1
```


**output:**
```
3 7 7 5 5
0 0 0 0 5
3 0 0 0 1
3 0 0 0 1
3 3 3 1 1
```

Okay, let's analyze the provided examples to understand the transformation logic.

## Perception of Elements

The task involves transforming a 2D grid of integers (colors) based on specific rules.
1.  **Grid:** A rectangular array of cells, each containing an integer.
2.  **Colors:** The integers represent colors. Color 0 is typically the background. Non-zero integers represent foreground objects or filled areas.
3.  **Input State:** The initial configuration of colors in the grid. Contains existing shapes or patterns.
4.  **Output State:** The modified configuration after applying the transformation rule. Some background cells (0) are changed to a specific foreground color. Existing foreground colors remain unchanged.
5.  **Transformation Logic:** The core process involves identifying a "source color" and one or more "trigger points" based on the input configuration. These triggers initiate a filling process (like dropping paint) which potentially involves vertical falling and horizontal spreading, using the source color. There appear to be two distinct scenarios for triggering the fill.

## YAML Fact Sheet


```yaml
Observations:
  Input_Type: 2D Grid of integers (Colors)
  Output_Type: 2D Grid of integers (Colors)
  Grid_Size: Consistent between input and output for a given example (e.g., 5x5)
  Background_Color: 0
  Foreground_Colors: Integers > 0
  Transformation_Type: Additive Filling - Only 0s are changed to non-zero colors. Existing non-zero colors are preserved.

Key_Elements:
  - Name: Topmost Populated Row
    Description: The highest row (smallest row index) containing at least one non-zero color.
    Symbolic_Name: r_top
  - Name: Fill Color Source
    Description: The leftmost non-zero color found in the Topmost Populated Row (r_top).
    Symbolic_Name: fill_color
  - Name: Rightmost Element Position (Top Row)
    Description: The column index of the rightmost non-zero color in the Topmost Populated Row (r_top).
    Symbolic_Name: c_right
  - Name: Isolated Trigger Element
    Description: A non-zero element that is the *only* non-zero element in its row, and this row must be below r_top. If multiple exist, the one in the lowest row (max row index) is chosen. If ties exist in the lowest row, the rightmost one (max column index) is chosen.
    Symbolic_Name: trigger (r_trigger, c_trigger)
  - Name: Top Row Fill Target
    Description: Zero-valued cells in r_top located to the right of c_right.
  - Name: Falling Path
    Description: A vertical sequence of 0-valued cells starting below a trigger point and extending downwards until hitting the grid boundary or a non-zero cell.
  - Name: Spreading Path
    Description: A horizontal sequence of 0-valued cells starting to the left of the lowest cell in a Falling Path and extending leftwards until hitting the grid boundary or a non-zero cell.

Transformation_Rules_Summary:
  - Rule 1 (Top Row Extension & Drip):
      Applies_When: No Isolated Trigger Element exists below r_top.
      Action:
        1. Fill any 0s in r_top to the right of c_right with fill_color.
        2. If any cells were filled in step 1, find the rightmost filled cell at (r_top, c_new_right).
        3. If the cell (r_top + 1, c_new_right) is within bounds and is 0, fill it with fill_color.
  - Rule 2 (Isolated Trigger Fall & Spread):
      Applies_When: An Isolated Trigger Element (r_trigger, c_trigger) exists below r_top.
      Action:
        1. Identify the vertical Falling Path starting below the trigger.
        2. Identify the horizontal Spreading Path starting leftwards from the bottom of the Falling Path.
        3. Fill all cells in the Falling Path and Spreading Path with fill_color.

Priority: Rule 2 (Isolated Trigger) takes precedence. If an Isolated Trigger exists, Rule 1 is not applied. If no Isolated Trigger exists, Rule 1 is applied.
```


## Natural Language Program

Here is a natural language program describing the transformation:

1.  **Initialize:** Create the output grid as a copy of the input grid.
2.  **Identify Top Row Parameters:**
    a. Find the highest row index, `r_top`, that contains at least one non-zero value. If no non-zero values exist anywhere, stop.
    b. Find the column index, `c_left`, of the leftmost non-zero value in row `r_top`. Set the `fill_color` to the value at `(r_top, c_left)`.
    c. Find the column index, `c_right`, of the rightmost non-zero value in row `r_top`.
3.  **Check for Isolated Trigger:**
    a. Search all rows `r` from `r_top + 1` down to the bottom row of the grid.
    b. For each row `r`, check if it contains exactly one non-zero value.
    c. Collect all such "isolated trigger" cells `(r, c)`.
    d. If one or more isolated triggers were found:
        i. Select the trigger `(r_trigger, c_trigger)` that has the maximum `r` value. If there's a tie for maximum `r`, select the one among them with the maximum `c` value.
        ii. **Perform Fall & Spread (Rule 2):**
            A. Starting from the cell directly below the trigger, `(r_trigger + 1, c_trigger)`, trace downwards column `c_trigger`. Identify the contiguous sequence of cells containing 0. Let the last cell in this sequence be `(y_stop, c_trigger)`. This is the Falling Path.
            B. Starting from the cell to the left of the end of the fall, `(y_stop, c_trigger - 1)`, trace leftwards along row `y_stop`. Identify the contiguous sequence of cells containing 0. Let the last cell in this sequence be `(y_stop, x_stop)`. This is the Spreading Path.
            C. Change the value of all cells in the Falling Path and the Spreading Path to `fill_color` in the output grid.
        iii. Proceed to step 5 (Finalize).
4.  **Perform Top Row Extension & Drip (Rule 1):** (This step only runs if NO isolated trigger was found in step 3)
    a. Initialize a flag `filled_top_row = false`.
    b. Iterate through columns `c` from `c_right + 1` to the last column index.
    c. If the cell `(r_top, c)` in the output grid contains 0:
        i. Change the value of `(r_top, c)` to `fill_color`.
        ii. Set `filled_top_row = true`.
        iii. Keep track of the rightmost column filled in this step, `c_new_right = c`.
    d. If `filled_top_row` is true:
        i. Check the cell below the rightmost filled cell: `(r_top + 1, c_new_right)`.
        ii. If this cell is within grid boundaries and contains 0, change its value to `fill_color` in the output grid.
5.  **Finalize:** The transformation is complete. The output grid holds the final state.
```python
"""
This program transforms a 2D grid of integers based on identified patterns.
The transformation involves two potential rules, prioritized as follows:

Rule 1 (Isolated Trigger Fall & Spread):
If there is an "isolated trigger" element (a non-zero cell that is the only non-zero element in its row, and this row is below the topmost row containing any non-zero elements), the rule applies. The trigger chosen is the one in the lowest row, breaking ties by choosing the rightmost one. The fill color is determined by the leftmost non-zero element in the topmost populated row. This fill color "falls" vertically downwards from below the trigger through consecutive 0s, and then "spreads" horizontally leftwards from the bottom of the fall path through consecutive 0s.

Rule 2 (Top Row Extension & Drip):
If no isolated trigger exists, this rule applies. The fill color is determined as in Rule 1. Any 0s in the topmost populated row to the right of the rightmost non-zero element are filled with the fill color. If any cells were filled this way, the cell directly below the rightmost newly filled cell is also filled with the fill color, provided it's within bounds and is currently 0.

Existing non-zero cells in the input grid are preserved in the output.
"""

import numpy as np

def _find_top_row_params(grid):
    """Finds the topmost row with non-zero elements and its parameters."""
    rows, cols = grid.shape
    r_top = -1
    fill_color = -1
    c_left = -1
    c_right = -1

    for r in range(rows):
        non_zeros = np.where(grid[r] != 0)[0]
        if len(non_zeros) > 0:
            r_top = r
            c_left = non_zeros[0]
            fill_color = grid[r, c_left]
            c_right = non_zeros[-1]
            break # Found the topmost row

    if r_top == -1:
        return None # No non-zero elements in the grid
    
    return r_top, fill_color, c_right

def _find_isolated_trigger(grid, r_top):
    """Finds the specific isolated trigger element based on the rules."""
    rows, cols = grid.shape
    potential_triggers = []

    for r in range(r_top + 1, rows):
        non_zeros_indices = np.where(grid[r] != 0)[0]
        if len(non_zeros_indices) == 1:
            c = non_zeros_indices[0]
            potential_triggers.append((r, c))

    if not potential_triggers:
        return None # No isolated triggers found

    # Sort triggers: primary key is row (descending), secondary key is col (descending)
    potential_triggers.sort(key=lambda item: (item[0], item[1]), reverse=True)
    
    # The best trigger is the first one after sorting
    return potential_triggers[0]


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    output_grid = np.array(input_grid, copy=True)
    rows, cols = output_grid.shape

    # 1. Identify Top Row Parameters
    top_params = _find_top_row_params(output_grid)
    if top_params is None:
        return output_grid # No non-zeros, return copy of input
    
    r_top, fill_color, c_right = top_params

    # 2. Check for Isolated Trigger
    trigger = _find_isolated_trigger(output_grid, r_top)

    if trigger:
        # 3. Perform Fall & Spread (Rule 2)
        r_trigger, c_trigger = trigger
        
        # Falling Path
        fall_path = []
        y_stop = r_trigger # Keep track of the last row reached by falling
        for r in range(r_trigger + 1, rows):
            if output_grid[r, c_trigger] == 0:
                fall_path.append((r, c_trigger))
                y_stop = r
            else:
                break # Hit boundary or non-zero

        # Spreading Path (only if fall path existed or starts right below trigger)
        spread_path = []
        # Start spreading from the row where the fall stopped (or trigger row if no fall)
        # But check if the fall path actually moved down first
        if fall_path:
            start_spread_row = y_stop
        else:
             # If nothing to fall into, check if we can spread from directly below trigger
             start_spread_row = r_trigger + 1
             if start_spread_row >= rows or output_grid[start_spread_row, c_trigger] != 0:
                 start_spread_row = -1 # Cannot start spread

        # Calculate spread only if we have a valid row to start from
        if start_spread_row != -1:
           for c in range(c_trigger - 1, -1, -1):
               if output_grid[start_spread_row, c] == 0:
                   spread_path.append((start_spread_row, c))
               else:
                   break # Hit boundary or non-zero

        # Fill paths
        for r, c in fall_path:
            output_grid[r, c] = fill_color
        for r, c in spread_path:
            output_grid[r, c] = fill_color

    else:
        # 4. Perform Top Row Extension & Drip (Rule 1)
        filled_top_row = False
        c_new_right = -1
        # Iterate from column after the rightmost element to the end
        for c in range(c_right + 1, cols):
            if output_grid[r_top, c] == 0:
                output_grid[r_top, c] = fill_color
                filled_top_row = True
                c_new_right = c # Track the last column filled

        # Perform drip if top row was extended
        if filled_top_row:
            r_drip = r_top + 1
            c_drip = c_new_right
            # Check bounds and if the cell below is 0
            if r_drip < rows and output_grid[r_drip, c_drip] == 0:
                output_grid[r_drip, c_drip] = fill_color

    # 5. Finalize
    return output_grid.tolist() # Return as list of lists as per typical format
```
