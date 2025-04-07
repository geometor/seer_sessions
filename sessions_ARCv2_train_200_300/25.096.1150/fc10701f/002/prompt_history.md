
## train_1

**input:**
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 9 9 6 6 6 6
6 6 6 6 6 6 9 9 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
```


**output:**
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
```


## train_2

**input:**
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 7 6 6 6 6 6 9
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```


**output:**
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 2 6 2 6 7
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```


## train_3

**input:**
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 9 9 6 6 6 6 6 6 7 7 6 6
6 6 6 6 9 9 6 6 6 6 6 6 7 7 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```


**output:**
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 7 7 6 2 6 6 2 6 6 6 6 6
6 6 6 6 7 7 6 2 6 6 2 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```

## Perception

The task involves transforming a 2D grid of digits based on specific rules applied to individual cells. The grids are primarily composed of the digit '6', which acts as a background color. Other significant digits are '0', '7', and '9'. The transformation introduces a new digit, '2'.

The transformation appears to involve three distinct and independent rules applied simultaneously to each cell based on the input grid's state:
1.  Cells containing '9' are changed to '7'.
2.  Cells containing '7' are changed to '6'.
3.  Cells containing '6' are changed to '2' under specific contextual conditions related to neighboring '0's. A '6' changes to '2' if it lies on a direct path (horizontal or vertical) between two '0's, where the path consists only of '6's apart from the endpoint '0's.

The relative positions of '0's determine whether the '6'-to-'2' transformation occurs. In some examples, pairs of '0's are arranged horizontally (`0 0 ... 6 6 ... 0 0`), causing the intermediate '6's in that row to become '2'. In other examples, the '0's are arranged vertically (`0 ... 6 ... 0`), causing the intermediate '6' in that column to become '2'.

## Facts


```yaml
task_elements:
  - object: grid
    description: A 2D array of single digits.
    properties:
      - rows: Integer number of rows.
      - columns: Integer number of columns.
      - cells: Contains individual digit values.
  - object: cell
    description: An individual element within the grid.
    properties:
      - value: The digit contained in the cell (e.g., 0, 2, 6, 7, 9).
      - position: (row, column) coordinates.
      - neighbors: Adjacent cells (up, down, left, right).
      - context: Surrounding cells in the same row or column, particularly '0's.

transformation_rules:
  - rule: direct_replacement_9_to_7
    description: Any cell containing the digit '9' in the input grid is replaced with '7' in the output grid.
    input_value: 9
    output_value: 7
  - rule: direct_replacement_7_to_6
    description: Any cell containing the digit '7' in the input grid is replaced with '6' in the output grid.
    input_value: 7
    output_value: 6
  - rule: conditional_replacement_6_to_2
    description: A cell containing '6' in the input grid is replaced with '2' if it satisfies the 'betweenness' condition.
    input_value: 6
    output_value: 2
    condition:
      - type: horizontal_betweenness
        description: >
          The cell at (r, c) contains '6', AND there exists a column c_left < c such that the cell (r, c_left) contains '0',
          AND there exists a column c_right > c such that the cell (r, c_right) contains '0',
          AND all cells (r, k) for c_left < k < c_right contain '6' in the input grid.
      - type: vertical_betweenness
        description: >
          The cell at (r, c) contains '6', AND there exists a row r_up < r such that the cell (r_up, c) contains '0',
          AND there exists a row r_down > r such that the cell (r_down, c) contains '0',
          AND all cells (k, c) for r_up < k < r_down contain '6' in the input grid.
    condition_logic: The cell must satisfy EITHER horizontal_betweenness OR vertical_betweenness.
  - rule: default_copy
    description: If none of the above rules apply to a cell, its value remains unchanged from input to output.

processing_order:
  - All rules are evaluated based on the original input grid state.
  - The output grid is constructed based on the results of these evaluations.
```


## Natural Language Program

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Iterate through each cell (r, c) of the input grid.
3.  For the current cell (r, c), determine its output value based on the following prioritized rules, evaluated using the *input* grid values:
    a.  If the input cell value is '9', set the corresponding output cell value to '7'.
    b.  Else if the input cell value is '7', set the corresponding output cell value to '6'.
    c.  Else if the input cell value is '6':
        i.  Check for horizontal 'betweenness': Scan leftwards from (r, c-1) to find the nearest '0' at (r, c_left). Scan rightwards from (r, c+1) to find the nearest '0' at (r, c_right). If both are found AND all cells between (r, c_left) and (r, c_right) (exclusive) contain only '6's in the input grid, then set the output cell value to '2'.
        ii. Check for vertical 'betweenness': Scan upwards from (r-1, c) to find the nearest '0' at (r_up, c). Scan downwards from (r+1, c) to find the nearest '0' at (r_down, c). If both are found AND all cells between (r_up, c) and (r_down, c) (exclusive) contain only '6's in the input grid, then set the output cell value to '2'.
        iii. If the cell is '6' but neither the horizontal nor vertical 'betweenness' condition is met, set the corresponding output cell value to '6'.
    d.  Else (if the input cell value is '0' or any other value not covered above), copy the input cell value to the corresponding output cell.
4.  Return the completed output grid.
```python
import copy
import math # although not used in the final code, imported as per instructions
import numpy as np # although not used in the final code, imported as per instructions

"""
Transforms the input grid based on the following rules applied simultaneously to each cell using the input state:
1. Cells with '9' become '7'.
2. Cells with '7' become '6'.
3. Cells with '6' become '2' if they are horizontally or vertically positioned between two '0's, 
   with only '6's along the direct path between the '0's (excluding the '0's themselves).
4. All other cells retain their original value.
"""

def check_horizontal_betweenness(grid: list[list[int]], r: int, c: int) -> bool:
    """
    Helper function to check if the cell (r, c) containing 6 is horizontally 
    between two 0s with only 6s in between, based on the input grid state.
    Scans left and right from the target cell (r, c).
    """
    rows = len(grid)
    cols = len(grid[0])

    # --- Scan left from c-1 down to 0 ---
    found_left_0 = False
    path_clear_left = True 
    for k in range(c - 1, -1, -1):
        if grid[r][k] == 0:
            # Found the left '0'
            found_left_0 = True
            break 
        elif grid[r][k] != 6:
            # Found a non-'6' before finding '0', path is blocked
            path_clear_left = False
            break
    
    # If no left '0' was found or the path was blocked, condition fails
    if not found_left_0 or not path_clear_left:
        return False

    # --- Scan right from c+1 up to cols-1 ---
    found_right_0 = False
    path_clear_right = True
    for k in range(c + 1, cols):
        if grid[r][k] == 0:
            # Found the right '0'
            found_right_0 = True
            break
        elif grid[r][k] != 6:
             # Found a non-'6' before finding '0', path is blocked
            path_clear_right = False
            break

    # If no right '0' was found or the path was blocked, condition fails
    if not found_right_0 or not path_clear_right:
        return False

    # If both left and right '0's were found with clear '6' paths in between
    return True


def check_vertical_betweenness(grid: list[list[int]], r: int, c: int) -> bool:
    """
    Helper function to check if the cell (r, c) containing 6 is vertically 
    between two 0s with only 6s in between, based on the input grid state.
    Scans up and down from the target cell (r, c).
    """
    rows = len(grid)
    cols = len(grid[0])

    # --- Scan up from r-1 down to 0 ---
    found_up_0 = False
    path_clear_up = True
    for k in range(r - 1, -1, -1):
        if grid[k][c] == 0:
            # Found the upper '0'
            found_up_0 = True
            break
        elif grid[k][c] != 6:
             # Found a non-'6' before finding '0', path is blocked
            path_clear_up = False
            break

    # If no upper '0' was found or the path was blocked, condition fails
    if not found_up_0 or not path_clear_up:
        return False

    # --- Scan down from r+1 up to rows-1 ---
    found_down_0 = False
    path_clear_down = True
    for k in range(r + 1, rows):
        if grid[k][c] == 0:
            # Found the lower '0'
            found_down_0 = True
            break
        elif grid[k][c] != 6:
            # Found a non-'6' before finding '0', path is blocked
            path_clear_down = False
            break

    # If no lower '0' was found or the path was blocked, condition fails
    if not found_down_0 or not path_clear_down:
        return False
        
    # If both upper and lower '0's were found with clear '6' paths in between
    return True

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input. 
    # This ensures that cells not explicitly changed by rules retain their original value,
    # and that all rule checks are performed on the original input state.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid to determine its output value
    for r in range(rows):
        for c in range(cols):
            # Get the value from the *original* input grid
            input_value = input_grid[r][c]

            # Apply transformation rules based on the input_value
            
            # Rule 1: If input is 9, output is 7
            if input_value == 9:
                output_grid[r][c] = 7
            
            # Rule 2: If input is 7, output is 6
            elif input_value == 7:
                output_grid[r][c] = 6
                
            # Rule 3: If input is 6, check for betweenness condition
            elif input_value == 6:
                # Check horizontal betweenness using the input grid
                is_between_horizontally = check_horizontal_betweenness(input_grid, r, c)
                # Check vertical betweenness using the input grid
                is_between_vertically = check_vertical_betweenness(input_grid, r, c)
                
                # If the cell is between 0s either horizontally OR vertically, output is 2
                if is_between_horizontally or is_between_vertically:
                    output_grid[r][c] = 2
                # Otherwise (if input is 6 but condition not met), output remains 6 (already set by deepcopy)
                
            # Rule 4: Default copy (e.g., for input 0)
            # No explicit action needed here, as output_grid was initialized as a copy.
            # If input_value is 0 or any other unspecified digit, output_grid[r][c] already holds that value.

    # Return the fully transformed grid
    return output_grid
```
