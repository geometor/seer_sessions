
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8
8 8 8 8 8 8 7
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 8 8 8 8 7
8 8 8 8 8 8 8
```

## Perception

The task involves transforming an input grid of digits into an output grid. Key elements observed:
1.  **Grid Structure:** Both input and output are rectangular grids of single digits.
2.  **Background Color:** The digit '8' serves as a predominant background color.
3.  **Axis Row:** A unique row exists in each input grid, characterized by the presence of the digit '6' and potentially other non-'8' digits. This row remains unchanged in the output and acts as a horizontal axis of transformation. Let's call its index 'R'.
4.  **Axis Pattern:** The non-'6' digits within the axis row R form a pattern that seems crucial for the transformation.
5.  **Transformation Logic:** The output grid appears to be constructed by reflecting or projecting the axis pattern vertically, symmetrically around the axis row R.
6.  **Filtering/Masking:** The projection isn't a simple copy. The values from the input grid at both a cell's location `(r, c)` and its symmetric location `(r_sym, c)` relative to the axis R influence whether the axis pattern value `input[R, c]` appears at `output[r, c]`. Specifically, it appears that `output[r, c]` takes the value `input[R, c]` if the symmetrically opposite input cell `input[r_sym, c]` matches `input[R, c]`.

## Facts

```yaml
objects:
  - name: input_grid
    properties:
      - type: 2D array of integers (digits 0-9)
      - background_color: 8
      - contains_axis_row: true
  - name: output_grid
    properties:
      - type: 2D array of integers (digits 0-9)
      - dimensions: same as input_grid
      - background_color: 8
  - name: axis_row
    properties:
      - type: row vector within the input_grid
      - identifier: contains the digit 6
      - index: R
      - contains_axis_pattern: true
  - name: axis_pattern
    properties:
      - type: set of (value, column_index) pairs
      - derived_from: axis_row (values != 6)
  - name: cell
    properties:
      - row_index: r
      - column_index: c
      - value: integer (digit 0-9)
      - location: (r, c) in a grid
relationships:
  - type: symmetry
    between: cell (r, c) and cell (r_sym, c)
    where: r_sym = R + (R - r)
  - type: source
    subject: axis_pattern
    object: output_grid non-background values (excluding axis row)
actions:
  - name: identify_axis_row
    input: input_grid
    output: axis_row_index R
  - name: extract_axis_pattern
    input: input_grid[R]
    output: axis_pattern P
  - name: initialize_output
    produces: output_grid (filled with background color 8)
  - name: copy_axis_row
    source: input_grid[R]
    destination: output_grid[R]
  - name: populate_output_cell
    inputs:
      - output_grid cell (r, c)
      - input_grid cell (r, c)
      - input_grid cell (r_sym, c)
      - input_grid cell (R, c) (axis value)
    condition:
      - r != R
      - input[R, c] != 6
      - input[r_sym, c] == input[R, c] # Based on Hypothesis 15
    effect: sets output_grid[r, c] = input[R, c]
```

## Natural Language Program

1.  Identify the horizontal row in the `input_grid` that contains the digit '6'. Let the index of this row be `R`. This is the 'axis row'.
2.  Create a new `output_grid` with the same dimensions as the `input_grid`, initially filled entirely with the background color '8'.
3.  Copy the entire axis row `R` from the `input_grid` to the `output_grid` at row `R`.
4.  Iterate through each row `r` of the `input_grid`, excluding the axis row `R`.
5.  For each row `r`, calculate the index of the symmetrically opposite row `r_sym = R + (R - r)`.
6.  If `r_sym` is outside the bounds of the grid (less than 0 or greater than or equal to the grid height), skip processing for this row `r` (its corresponding row in the `output_grid` remains background '8').
7.  If `r_sym` is within the grid bounds, iterate through each column `c` from 0 to the grid width minus 1.
8.  Get the value from the axis row at this column: `val_axis = input_grid[R, c]`.
9.  If `val_axis` is equal to '6', skip processing for this column `c` (the cell `output_grid[r, c]` remains background '8').
10. Get the value from the symmetric input row at this column: `val_sym = input_grid[r_sym, c]`.
11. Compare `val_sym` with `val_axis`. If they are equal (`val_sym == val_axis`), set the corresponding cell in the `output_grid` to the axis value: `output_grid[r, c] = val_axis`.
12. If `val_sym` is not equal to `val_axis`, the cell `output_grid[r, c]` remains background '8'.
13. After iterating through all rows `r` (except `R`) and all columns `c`, the `output_grid` is complete.
```python
import copy

"""
Rule Description:

1.  Identify the horizontal 'axis' row in the input grid, which is the row containing the digit '6'. Let its index be `R`.
2.  Initialize the output grid with the same dimensions as the input, filled with the background digit '8'.
3.  Copy the axis row `R` from the input grid directly to the output grid at row `R`.
4.  For each cell `(r, c)` in the grid *not* on the axis row (`r != R`):
    a.  Determine the value on the axis row in the same column: `val_axis = input_grid[R][c]`.
    b.  If `val_axis` is '6', the output cell `output_grid[r][c]` remains '8'.
    c.  If `val_axis` is not '6', calculate the index of the symmetrically opposite row: `r_sym = R + (R - r)`.
    d.  Check if `r_sym` is a valid row index within the grid boundaries.
    e.  If `r_sym` is valid, get the value from the input grid at the symmetric position: `val_sym = input_grid[r_sym][c]`.
    f.  Compare the symmetric value `val_sym` with the axis value `val_axis`.
    g.  If `val_sym == val_axis`, then set the output cell `output_grid[r][c]` to `val_axis`.
    h.  If `r_sym` is invalid or if `val_sym != val_axis`, the output cell `output_grid[r][c]` remains '8'.
"""

def find_axis_row(grid: list[list[int]]) -> int:
    """Finds the index of the row containing the digit 6."""
    for r, row in enumerate(grid):
        if 6 in row:
            return r
    # Should not happen based on problem description/examples
    return -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on reflection across an axis row
    and a matching condition with the symmetrically opposite cell.
    """
    
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the axis row index
    axis_row_index = find_axis_row(input_grid)
    if axis_row_index == -1:
         # Fallback or error handling if no axis row found
         # Based on examples, axis always exists.
         # Returning a copy or raising error might be options.
         # For now, assume it exists per problem structure.
         pass 

    # Initialize output_grid with background color 8
    output_grid = [[8 for _ in range(width)] for _ in range(height)]

    # Copy the axis row directly
    if 0 <= axis_row_index < height:
        output_grid[axis_row_index] = copy.deepcopy(input_grid[axis_row_index])

    # Iterate through each cell not on the axis row
    for r in range(height):
        if r == axis_row_index:
            continue

        for c in range(width):
            # Get the value from the axis row at this column
            val_axis = input_grid[axis_row_index][c]

            # If axis value is 6, output remains 8 (already initialized)
            if val_axis == 6:
                continue

            # Calculate symmetric row index
            r_sym = axis_row_index + (axis_row_index - r)

            # Check if symmetric row is within bounds
            if 0 <= r_sym < height:
                # Get value from symmetric position in input grid
                val_sym = input_grid[r_sym][c]

                # Condition: If symmetric value matches axis value
                if val_sym == val_axis:
                    # Set output cell to the axis value
                    output_grid[r][c] = val_axis
            # Else (r_sym out of bounds or val_sym != val_axis), 
            # output remains 8 (already initialized)

    return output_grid

```

Previous Code:
```python
import copy

"""
Rule Description:

1.  Identify the horizontal 'axis' row in the input grid, which is the row containing the digit '6'. Let its index be `R`.
2.  Initialize the output grid with the same dimensions as the input, filled with the background digit '8'.
3.  Copy the axis row `R` from the input grid directly to the output grid at row `R`.
4.  For each cell `(r, c)` in the grid *not* on the axis row (`r != R`):
    a.  Determine the value on the axis row in the same column: `val_axis = input_grid[R][c]`.
    b.  If `val_axis` is '6', the output cell `output_grid[r][c]` remains '8'.
    c.  If `val_axis` is not '6', calculate the index of the symmetrically opposite row: `r_sym = R + (R - r)`.
    d.  Check if `r_sym` is a valid row index within the grid boundaries.
    e.  If `r_sym` is valid, get the value from the input grid at the symmetric position: `val_sym = input_grid[r_sym][c]`.
    f.  Compare the symmetric value `val_sym` with the axis value `val_axis`.
    g.  If `val_sym == val_axis`, then set the output cell `output_grid[r][c]` to `val_axis`.
    h.  If `r_sym` is invalid or if `val_sym != val_axis`, the output cell `output_grid[r][c]` remains '8'.
"""

def find_axis_row(grid: list[list[int]]) -> int:
    """Finds the index of the row containing the digit 6."""
    for r, row in enumerate(grid):
        if 6 in row:
            return r
    # Should not happen based on problem description/examples
    return -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on reflection across an axis row
    and a matching condition with the symmetrically opposite cell.
    """
    
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the axis row index
    axis_row_index = find_axis_row(input_grid)
    if axis_row_index == -1:
         # Fallback or error handling if no axis row found
         # Based on examples, axis always exists.
         # Returning a copy or raising error might be options.
         # For now, assume it exists per problem structure.
         pass 

    # Initialize output_grid with background color 8
    output_grid = [[8 for _ in range(width)] for _ in range(height)]

    # Copy the axis row directly
    if 0 <= axis_row_index < height:
        output_grid[axis_row_index] = copy.deepcopy(input_grid[axis_row_index])

    # Iterate through each cell not on the axis row
    for r in range(height):
        if r == axis_row_index:
            continue

        for c in range(width):
            # Get the value from the axis row at this column
            val_axis = input_grid[axis_row_index][c]

            # If axis value is 6, output remains 8 (already initialized)
            if val_axis == 6:
                continue

            # Calculate symmetric row index
            r_sym = axis_row_index + (axis_row_index - r)

            # Check if symmetric row is within bounds
            if 0 <= r_sym < height:
                # Get value from symmetric position in input grid
                val_sym = input_grid[r_sym][c]

                # Condition: If symmetric value matches axis value
                if val_sym == val_axis:
                    # Set output cell to the axis value
                    output_grid[r][c] = val_axis
            # Else (r_sym out of bounds or val_sym != val_axis), 
            # output remains 8 (already initialized)

    return output_grid

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.93491124260356

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.666666666666657

## Example 3:
Input:
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8
8 8 8 8 8 8 7
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 8 8 8 8 7
8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.32653061224488
Okay, let's analyze the results and refine the approach.

## General Assessment and Strategy

The previous code implemented the hypothesis: `output[r][c] = val_axis` if `input[r_sym][c] == val_axis`. The results clearly show this hypothesis is incorrect, as the generated output often resembles the input grid rather than the expected reflected/transformed output.

The core idea of finding an axis row (containing '6') and performing a symmetric operation seems sound, as the axis row itself is consistently copied correctly, and the modifications in the output are symmetric around this axis.

The key is to correctly identify the condition under which a cell `(r, c)` (where `r` is not the axis row index `R`) takes the value `val_axis = input[R][c]`. The failures indicate that simply checking if the symmetrically opposite input cell `input[r_sym][c]` matches `val_axis` is insufficient.

**Strategy:**
1.  **Analyze Failures:** Examine the specific cells where the previous code's output differs from the expected output.
2.  **Compare Input and Output:** Look for patterns comparing `input[r][c]`, `input[r_sym][c]`, and `input[R][c]` for cells where `output[r][c]` equals `input[R][c]` versus where it equals the background '8'.
3.  **Formulate New Hypothesis:** Develop a revised rule based on the analysis. Initial thoughts revolved around propagation or different masking conditions, but a closer look suggests a modified symmetric condition might work.
4.  **Test New Hypothesis:** Mentally walk through the examples with the new hypothesis before proposing the final natural language program.

**Analysis leading to Hypothesis 13:**
*   Comparing Hypothesis 5 (symmetric match: `input[r_sym][c] == val_axis`) with expected outputs showed it failed when the symmetric cell did *not* match the axis value, yet the output *did* take the axis value (e.g., Ex1 `output[2][8]=1` when `input[10][8]=8` and `val_axis=1`). This suggests the rule needs to be broader.
*   Comparing Hypothesis 12 (symmetric match OR symmetric is background: `input[r_sym][c] == val_axis` OR `input[r_sym][c] == 8`) worked for many previously failed cases but introduced new failures where both the original cell *and* the symmetric cell matched the axis value (e.g., Ex1 `output[4][1]=8` when H12 predicted 5 because `input[4][1]=5`, `val_axis=5`, and `input[8][1]=5`).
*   This led to Hypothesis 13, which uses the broader condition from H12 but adds an explicit exception: if both the original cell and its symmetric counterpart already match the axis color, the output should revert to the background color '8'.

## Metrics

Let's analyze the previous code's failures based on the provided results:

*   **Example 1:**
    *   Input Size: 13x13
    *   Axis Row (R): 6
    *   Pixels Off: 16
    *   Expected non-8, non-6 values outside axis: 24 (count of 5, 2, 7, 1 instances)
    *   Code's non-8, non-6 values outside axis: 16 (count of 5, 2, 7, 1 instances in its output)
    *   Analysis: The code missed placing the axis value in 8 locations above the axis and 8 locations below the axis, specifically where the symmetric cell did not match the axis value (e.g., `output[2][8]` should be 1 but `input[10][8]` is 8). It also incorrectly placed the axis value in 8 locations (4 above, 4 below) where the symmetric cell *did* match the axis value, but the original cell *also* matched (e.g., `output[4][1]` should be 8, but code put 5 because `input[8][1]=5`). Total difference involves these 16 cells.
*   **Example 2:**
    *   Input Size: 15x15
    *   Axis Row (R): 7
    *   Pixels Off: 12
    *   Analysis: Similar pattern of failure. Code likely missed cases where `input[r_sym][c]` was 8 (like `output[3][8]=1` where `input[11][8]=8`) and incorrectly included cases where `input[r][c] == input[r_sym][c] == val_axis` (like `output[5][4]=8` where code put 7 because `input[9][4]=7`).
*   **Example 3:**
    *   Input Size: 7x7
    *   Axis Row (R): 3
    *   Pixels Off: 4
    *   Analysis: Code failed to place '7' at `output[1][6]` and `output[5][6]` because the symmetric cells (`input[5][6]` and `input[1][6]`) were 8, not 7. It correctly placed '4', '1', '1', '7' in rows 2 and 4 because the symmetric cells matched.

## Facts

```yaml
objects:
  - name: input_grid
    properties:
      - type: 2D array of integers (digits 0-9)
      - background_color: 8
      - contains_axis_row: true
  - name: output_grid
    properties:
      - type: 2D array of integers (digits 0-9)
      - dimensions: same as input_grid
      - background_color: 8
  - name: axis_row
    properties:
      - type: row vector within the input_grid
      - identifier: contains the digit 6
      - index: R
  - name: cell
    properties:
      - row_index: r
      - column_index: c
      - value: integer (digit 0-9)
      - location: (r, c) in a grid
relationships:
  - type: symmetry
    between: cell (r, c) and cell (r_sym, c)
    where: r_sym = R + (R - r)
actions:
  - name: find_axis_row
    input: input_grid
    output: axis_row_index R
  - name: initialize_output
    produces: output_grid (filled with background color 8)
  - name: copy_axis_row
    source: input_grid[R]
    destination: output_grid[R]
  - name: calculate_output_cell_value
    inputs:
      - current cell coordinates: (r, c)
      - axis_row_index: R
      - input_grid
    preconditions:
      - r != R
    process:
      - get axis value: val_axis = input_grid[R][c]
      - if val_axis == 6, output is 8
      - calculate symmetric row: r_sym = R + (R - r)
      - if r_sym is out of bounds, output is 8
      - get symmetric value: val_sym = input_grid[r_sym][c]
      - get original value: val_orig = input_grid[r][c]
      - determine condition: rule_applies = (val_sym == val_axis) or (val_sym == 8)
      - determine exception: is_exception = (val_orig == val_axis) and (val_sym == val_axis)
      - if rule_applies and not is_exception, output is val_axis
      - else, output is 8
    output: value for output_grid[r][c]
```

## Natural Language Program

1.  Identify the horizontal row in the `input_grid` that contains the digit '6'. Let the index of this row be `R`. This is the 'axis row'.
2.  Create a new `output_grid` with the same dimensions as the `input_grid`, initially filled entirely with the background color '8'.
3.  Copy the entire axis row `R` from the `input_grid` to the `output_grid` at row `R`.
4.  Iterate through each row `r` of the `input_grid`, excluding the axis row `R`.
5.  For each row `r`, iterate through each column `c` from 0 to the grid width minus 1.
6.  Get the value from the axis row at this column: `val_axis = input_grid[R][c]`.
7.  If `val_axis` is equal to '6', the corresponding cell `output_grid[r][c]` remains background '8'. Skip to the next column.
8.  Calculate the index of the symmetrically opposite row: `r_sym = R + (R - r)`.
9.  Check if `r_sym` is a valid row index (within the grid boundaries). If `r_sym` is invalid, the cell `output_grid[r][c]` remains background '8'. Skip to the next column.
10. Get the value from the input grid at the symmetric position: `val_sym = input_grid[r_sym][c]`.
11. Get the value from the input grid at the current cell's original position: `val_orig = input_grid[r][c]`.
12. Check if the reflection rule applies: Does the symmetric value match the axis value (`val_sym == val_axis`) OR is the symmetric value the background color (`val_sym == 8`)?
13. Check for the exception case: Does the original value match the axis value (`val_orig == val_axis`) AND does the symmetric value also match the axis value (`val_sym == val_axis`)?
14. If the reflection rule applies (Step 12 is true) AND the exception case does NOT apply (Step 13 is false), then set the output cell to the axis value: `output_grid[r][c] = val_axis`.
15. Otherwise (if the rule does not apply OR if the exception case applies), the cell `output_grid[r][c]` remains background '8'.
16. After iterating through all rows `r` (except `R`) and all columns `c`, the `output_grid` is complete.
```python
import copy

"""
The transformation identifies a horizontal 'axis' row in the input grid, characterized by the presence of the digit '6'. 
The output grid is initialized with a background color ('8') and the axis row is copied directly from the input. 
For all other cells (r, c) not on the axis row, the output value is determined by comparing the input values at the cell's original position (r, c), 
its symmetrically opposite position (r_sym, c) relative to the axis row, and the axis value at the same column (R, c).
Specifically, the output cell output_grid[r][c] takes the value val_axis = input_grid[R][c] if:
1. val_axis is not '6'.
2. The symmetric row r_sym = R + (R - r) is within the grid bounds.
3. The value at the symmetric position val_sym = input_grid[r_sym][c] either matches the axis value (val_sym == val_axis) OR is the background color (val_sym == 8).
4. An exception case is NOT met: the exception occurs if both the original value val_orig = input_grid[r][c] and the symmetric value val_sym already match the axis value (val_orig == val_axis and val_sym == val_axis).
If the conditions are met and the exception does not apply, output_grid[r][c] becomes val_axis. Otherwise, it remains the background color '8'.
"""

def find_axis_row(grid: list[list[int]]) -> int:
    """Finds the index of the row containing the digit 6."""
    for r, row in enumerate(grid):
        if 6 in row:
            return r
    # This case should ideally not be reached based on problem constraints
    # If it could happen, raising an error or returning None might be better.
    return -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the axis row index
    axis_row_index = find_axis_row(input_grid)
    # Assuming axis row always exists based on examples
    if axis_row_index == -1:
        # Handle error or return default if axis not found, though unexpected
        return copy.deepcopy(input_grid) # Or raise ValueError("Axis row not found")

    # Initialize output_grid with background color 8
    output_grid = [[8 for _ in range(width)] for _ in range(height)]

    # Copy the axis row directly
    if 0 <= axis_row_index < height:
        output_grid[axis_row_index] = copy.deepcopy(input_grid[axis_row_index])

    # Iterate through each cell not on the axis row
    for r in range(height):
        if r == axis_row_index:
            continue

        for c in range(width):
            # Get the value from the axis row at this column
            val_axis = input_grid[axis_row_index][c]

            # If axis value is 6, output remains 8 (already initialized). Skip.
            if val_axis == 6:
                continue

            # Calculate symmetric row index
            r_sym = axis_row_index + (axis_row_index - r)

            # Check if symmetric row is within bounds
            if 0 <= r_sym < height:
                # Get value from symmetric position in input grid
                val_sym = input_grid[r_sym][c]
                # Get value from original position in input grid
                val_orig = input_grid[r][c]

                # Check if the reflection rule applies
                rule_applies = (val_sym == val_axis) or (val_sym == 8)
                
                # Check for the exception case
                is_exception = (val_orig == val_axis) and (val_sym == val_axis)

                # If the rule applies AND it's not the exception case, set output to axis value
                if rule_applies and not is_exception:
                    output_grid[r][c] = val_axis
                # Else (rule doesn't apply OR exception applies), output remains 8 (already initialized)

            # Else (r_sym out of bounds), output remains 8 (already initialized)

    return output_grid
```
