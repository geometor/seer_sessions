
## train_1

**input:**
```
8 8 0 0 0
0 0 6 2 0
0 6 2 2 0
0 0 6 6 0
0 0 6 0 0
```


**output:**
```
8 8 8 8 8
0 0 6 2 0
0 6 2 2 0
0 0 6 6 0
0 0 6 0 0
```


## train_2

**input:**
```
0 7 0 0 7
0 7 0 7 0
0 0 5 0 0
0 0 3 3 0
0 0 0 0 0
```


**output:**
```
5 5 5 5 5
0 7 0 7 0
0 0 5 0 0
0 0 3 3 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 8 0
4 0 4 0 8
0 9 0 8 9
0 0 8 9 0
0 8 0 0 9
```


**output:**
```
4 4 4 4 4
4 0 4 0 8
0 9 0 8 9
0 0 8 9 0
0 8 0 0 9
```

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) of single-digit integers. The examples shown are 5x5 grids.
2.  **Transformation Scope:** The transformation primarily affects the first row of the grid. All other rows (from the second row downwards) appear to be copied directly from the input to the output without modification.
3.  **First Row Modification:** The first row of the output grid is uniformly filled with a single digit.
4.  **Determining the Fill Value:** The digit used to fill the first row of the output is determined by scanning the *input* grid. The scanning process proceeds column by column, from left to right. Within each column, it scans row by row, from top to bottom. The first non-zero digit encountered during this scan is the value used to fill the entire first row of the output.

**Facts:**


```yaml
task_elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (e.g., 5x5 in examples)
      - cells: contain single-digit integers (0-9)
      - structure: rows and columns
  - object: input_grid
    relation: source data for transformation
  - object: output_grid
    relation: result of transformation applied to input_grid
    properties:
      - same dimensions as input_grid
actions:
  - action: copy_rows
    source: input_grid
    destination: output_grid
    details: Rows from index 1 to the end are copied verbatim.
  - action: determine_fill_value
    source: input_grid
    process:
      - scan columns from left (index 0) to right.
      - within each column, scan rows from top (index 0) to bottom.
      - identify the value of the first cell encountered that is not zero.
    result: fill_value (an integer)
  - action: modify_first_row
    target: output_grid
    details: Replace every element in the first row (index 0) with the determined fill_value.
relationships:
  - The output grid's rows from index 1 onwards are identical to the input grid's corresponding rows.
  - The output grid's first row's content depends entirely on the first non-zero value found in the input grid using a column-major, row-minor scanning order.
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Create a copy of the input grid to serve as the basis for the output grid.
3.  Initialize a variable `fill_value` to zero (or null).
4.  Iterate through the columns of the input grid, starting from the leftmost column (index 0) and moving to the right.
5.  For the current column, iterate through its rows, starting from the top row (index 0) and moving downwards.
6.  Check the value of the cell at the current row and column.
7.  If the cell value is not zero:
    a.  Set the `fill_value` to this cell's value.
    b.  Stop scanning immediately (both the inner row loop and the outer column loop).
8.  If the scanning completes without finding a non-zero value, the `fill_value` remains at its initial state (likely zero, though examples don't cover this case explicitly; assuming the task guarantees at least one non-zero value if modification occurs, or perhaps the first row remains unchanged if all input values are zero). Based on the examples, it seems a non-zero value is always found.
9.  Iterate through all the cells in the first row (index 0) of the output grid.
10. Set the value of each cell in the first row of the output grid to the determined `fill_value`.
11. Return the modified output grid.
```python
import copy

"""
Transformation Rule:
1. Copy the input grid to create the output grid.
2. Scan the input grid column by column, from left to right. Within each column, scan row by row, from top to bottom.
3. Find the first non-zero value encountered during this scan. This value becomes the 'fill_value'.
4. Replace all elements in the first row (row index 0) of the output grid with the 'fill_value'.
5. If no non-zero value is found in the input grid, the output grid remains identical to the input grid (specifically, the first row remains unchanged).
"""

def find_first_non_zero_column_major(grid):
    """
    Scans the grid column by column, then row by row, to find the first non-zero value.

    Args:
        grid: A list of lists representing the 2D grid of integers.

    Returns:
        The first non-zero value found, or None if all values are zero or the grid is empty.
    """
    if not grid or not grid[0]: # Check for empty grid or grid with empty rows
        return None
        
    height = len(grid)
    width = len(grid[0])
    
    # Iterate through columns first
    for j in range(width):
        # Then iterate through rows within the current column
        for i in range(height):
            if grid[i][j] != 0:
                return grid[i][j] # Return the first non-zero value found
                
    return None # Return None if no non-zero value is found

def transform(input_grid):
    """
    Applies the transformation rule: copies the grid, finds the first non-zero
    value scanning column-major, and fills the first row of the output grid
    with that value.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the 2D output grid.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []
        
    # 1. Initialize output_grid as a deep copy of the input_grid
    #    This preserves rows 1 onwards automatically.
    output_grid = copy.deepcopy(input_grid)
    
    # 2. Determine the fill_value by scanning the input grid
    fill_value = find_first_non_zero_column_major(input_grid)
    
    # 3. Modify the first row of the output grid if a non-zero fill_value was found
    if fill_value is not None:
        width = len(output_grid[0])
        # Iterate through the columns of the first row
        for j in range(width):
            output_grid[0][j] = fill_value
            
    # 4. Return the modified output grid
    return output_grid

```
