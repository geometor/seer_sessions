
## train_1

**input:**
```
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
8 8 0 0 8 8 0 8 8 0 8 0
8 2 2 0 8 2 2 2 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
```


## train_2

**input:**
```
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
0 8 0 8 8 2 2 2 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
```


## train_3

**input:**
```
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 8 8 0 0 0 8 8 8 8 0 8
8 8 2 2 0 2 2 2 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
```


## train_4

**input:**
```
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 8 8 0 8
0 8 0 0 2 2 2 8 0 8
0 8 0 0 0 0 0 8 0 8
0 8 0 0 0 0 0 8 0 8
0 8 0 0 0 0 0 8 0 8
0 8 0 0 0 0 0 8 0 8
```

Okay, I will analyze the provided examples and generate the requested deliverables.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) containing numerical values.
2.  **Grid Dimensions:** The grid dimensions can vary between examples, but for a given example, the output grid always has the same dimensions as the input grid.
3.  **Cell Values (Colors):** The grids contain three distinct values: 0 (likely representing black/background), 8 (grey), and 2 (blue).
4.  **Input Structure:**
    *   The input grids typically have a block of identical rows at the top, characterized by repeating vertical patterns of the value 8.
    *   Below this top block, there is usually at least one row of all 0s.
    *   Further down, there is a small, localized cluster of the value 2 (blue).
    *   The rest of the grid cells are 0.
5.  **Output Structure:**
    *   The output grid retains all the original values (0s, 8s, and 2s) from the input grid in their original positions.
    *   The key difference is the addition of new 8s (grey cells) in the output.
6.  **Transformation Pattern:** The new 8s appear to form vertical lines. These lines are located in columns that contained 8s within the initial top block of the input grid. The new vertical lines start from the row immediately following the top block and extend downwards to the bottom of the grid. Existing 0s in these columns (below the top block) are replaced by 8s, while existing 2s or original 8s remain unchanged.

**YAML Facts:**


```yaml
Task: Fill columns downwards with a specific color based on header pattern.

Input:
  Type: Grid
  Properties:
    - Contains integers representing colors (0, 2, 8).
    - Has a distinct top block of rows with a repeating pattern, primarily featuring the color 8.
    - Contains a small cluster of color 2 somewhere below the top block.
    - Color 0 acts as a background.

Output:
  Type: Grid
  Properties:
    - Same dimensions as the input grid.
    - Preserves all elements (0, 2, 8) from the input grid.
    - Contains additional elements of color 8.

Transformation:
  Action: Add color 8 elements to the grid.
  Rule:
    1. Identify the top block of identical rows starting from row 0. Let the last row index of this block be 'last_top_row'.
    2. Identify all column indices that contain the color 8 within this top block (rows 0 to 'last_top_row'). Let this set be 'target_columns'.
    3. Create the output grid by copying the input grid.
    4. For each column index 'c' in 'target_columns':
       Iterate through rows from 'last_top_row + 1' down to the last row of the grid.
       Set the value of the cell at (row, c) in the output grid to 8.
  Relationships:
    - The locations of the new 8s depend directly on the column positions of the 8s in the initial top block of the input grid.
    - The vertical extension of the new 8s starts immediately below the identified top block.
    - Original non-zero elements (8s and 2s) in the input are preserved in the output.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Determine the extent of the top block of identical rows: Find the index of the first row (`first_different_row_index`) that is not identical to the first row (row 0). The last row of the top block (`last_top_row`) is `first_different_row_index - 1`. (If all rows are identical, handle this edge case, though it doesn't appear in examples).
3.  Identify the target columns: Create a set of column indices containing any '8's within the rows 0 to `last_top_row` of the input grid.
4.  Fill downwards: For each `column_index` in the set of target columns:
    *   Iterate through each `row_index` starting from `last_top_row + 1` up to the total number of rows minus 1.
    *   Set the cell value at `output_grid[row_index][column_index]` to 8.
5.  Return the modified output grid.
```python
import copy

def find_last_top_row(grid: list[list[int]]) -> int:
    """
    Finds the index of the last row belonging to the initial block of identical top rows.

    Args:
        grid: The input grid.

    Returns:
        The index of the last row in the top block. Returns -1 if the grid is empty
        or 0 if there's only one row or the first two rows differ.
    """
    if not grid:
        return -1
    if len(grid) == 1:
        return 0

    first_row = grid[0]
    last_top_row = 0
    for r in range(1, len(grid)):
        if grid[r] == first_row:
            last_top_row = r
        else:
            break
    return last_top_row

def find_target_columns(grid: list[list[int]], last_top_row: int, target_value: int) -> set[int]:
    """
    Finds the indices of columns containing the target_value within the specified top rows.

    Args:
        grid: The input grid.
        last_top_row: The index of the last row to check.
        target_value: The value to search for in the columns.

    Returns:
        A set of column indices containing the target_value in the top block.
    """
    if not grid or last_top_row < 0:
        return set()

    num_cols = len(grid[0])
    target_columns = set()
    for c in range(num_cols):
        for r in range(last_top_row + 1):
             # Check bounds just in case, although grid should be rectangular
            if c < len(grid[r]) and grid[r][c] == target_value:
                target_columns.add(c)
                break # Move to the next column once found
    return target_columns

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying columns containing '8' in the top
    block of identical rows and filling those columns with '8' from below the
    block downwards, preserving existing non-zero values.

    1. Initialize the output grid as a copy of the input grid.
    2. Determine the extent of the top block of identical rows: Find the index
       of the first row (`first_different_row_index`) that is not identical
       to the first row (row 0). The last row of the top block
       (`last_top_row`) is `first_different_row_index - 1`.
    3. Identify the target columns: Create a set of column indices containing
       any '8's within the rows 0 to `last_top_row` of the input grid.
    4. Fill downwards: For each `column_index` in the set of target columns:
       - Iterate through each `row_index` starting from `last_top_row + 1`
         up to the total number of rows minus 1.
       - Set the cell value at `output_grid[row_index][column_index]` to 8,
         but only if the original value was 0 (preserves 2s).
         *Correction based on examples*: The examples show that 0s are overwritten by 8s,
         but existing 2s and original 8s below the top block remain. The logic should
         simply set the value to 8 regardless of the original value below the top block,
         as the output examples show only 8s in these filled columns below the top block,
         except where the initial '2's were. *Further Correction:* Re-examining train_1 output,
         cell (5,1) is 2 in input and 2 in output. cell (5,0) is 0 in input and 8 in output.
         It seems only 0s are replaced by 8s in the target columns below the top block.

    5. Return the modified output grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    # Initialize output_grid as a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) # Assume rectangular grid

    # 1. Determine the extent of the top block of identical rows
    last_top_row = find_last_top_row(input_grid)

    # 2. Identify the target columns containing '8' in the top block
    target_columns = find_target_columns(input_grid, last_top_row, 8)

    # 3. Fill downwards in target columns below the top block
    # Start filling from the row immediately after the top block
    start_fill_row = last_top_row + 1
    for c in target_columns:
        for r in range(start_fill_row, num_rows):
            # Only change the cell if it's currently 0
            # This preserves existing 2s and any original 8s below the top block
            if output_grid[r][c] == 0:
                 output_grid[r][c] = 8

    # Return the modified grid
    return output_grid
```
