
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 6 0
0 0 0 0 0 0 6 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0
6 0 0 6 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 6 6 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Grid Structure:** Both input and output grids have the same dimensions (10x10 in the examples).
2.  **Color Palette:** The grids primarily use white (0) as the background color and magenta (6) as the foreground or active color.
3.  **Transformation Focus:** The transformation seems to operate on the magenta pixels within each row independently. The vertical position (row index) of magenta pixels does not change.
4.  **Core Action:** Magenta pixels within each row are shifted horizontally towards the left edge of the grid.
5.  **Rule Identification:** By comparing the input and output rows containing magenta pixels, it appears that all magenta pixels from a specific row in the input are collected and then placed at the beginning (leftmost columns) of the same row in the output. The relative horizontal order of these magenta pixels within the row is preserved. For example, if a row had magenta pixels at columns 2, 5, and 6, the output row would have magenta pixels at columns 0, 1, and 2.
6.  **Consistency:** This pattern holds true for both `train_1` and `train_2`. Rows that are entirely white in the input remain entirely white in the output.

## Facts


```yaml
task_elements:
  - type: grid
    properties:
      - background_color: white (0)
      - foreground_color: magenta (6)
      - dimensions: constant between input and output
transformation:
  - type: rearrangement
    scope: row-wise
    target: magenta pixels
    action: horizontal shift to the left
    constraints:
      - preserve relative horizontal order within the row
      - preserve row index (vertical position)
      - preserve count of magenta pixels per row
  - effect: All magenta pixels in a row are consolidated at the leftmost columns of that row.
input_output_relationship:
  - Each row in the output is derived solely from the corresponding row in the input.
  - The number of magenta pixels in any given row of the output grid is equal to the number of magenta pixels in the corresponding row of the input grid.
```


## Natural Language Program

1.  Create a new output grid with the same dimensions as the input grid, initially filled with the background color (white, 0).
2.  Process the input grid row by row.
3.  For each row:
    a.  Initialize an empty list to store the magenta pixels found in this row.
    b.  Iterate through the columns of the current row in the input grid.
    c.  If a cell contains a magenta pixel (6), add it to the list of magenta pixels for this row.
    d.  Iterate through the collected list of magenta pixels for this row.
    e.  Place each magenta pixel from the list into the corresponding row of the output grid, starting at column 0 and incrementing the column index for each placed pixel.
4.  Return the completed output grid.
```python
import numpy as np

"""
Transforms an input grid by processing each row independently. 
For each row, all magenta (6) pixels are identified and then moved 
to the leftmost positions of that same row in the output grid, 
maintaining their count but not necessarily their original relative order 
(though in this specific transformation, since they are all the same color, 
relative order doesn't matter). 
The rest of the cells in the row become white (0).
"""

def transform(input_grid):
    """
    Applies the row-wise left-consolidation transformation to a grid.

    Args:
        input_grid (list of lists or numpy array): The input grid containing integers 0-9.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_np.shape

    # Initialize output_grid with the same dimensions as input, filled with background color (0)
    output_grid = np.zeros_like(input_np)

    # Process each row independently
    for r in range(num_rows):
        # Get the current row from the input grid
        input_row = input_np[r, :]

        # Count the number of magenta pixels (value 6) in the current row
        magenta_count = np.count_nonzero(input_row == 6)

        # If there are any magenta pixels in this row
        if magenta_count > 0:
            # Place the counted number of magenta pixels at the beginning (left side) of the corresponding row in the output grid
            output_grid[r, :magenta_count] = 6

    return output_grid.tolist() # Return as list of lists per ARC standard

```
