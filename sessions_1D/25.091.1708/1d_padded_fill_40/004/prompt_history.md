
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
```


## train_3

**input:**
```
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain mostly white pixels (0) and a few isolated non-white pixels (blue=1, green=3, orange=7).
    *   In each example, the non-white pixels appear in different rows but seem to maintain a consistent column alignment within that example.
    *   The output grids retain the same dimensions as the input grids.
    *   The transformation operates row by row.
    *   For each row in the input grid:
        *   If the row contains only white pixels, the corresponding output row is identical (all white).
        *   If the row contains a non-white pixel, locate the column index of that pixel. The output row is modified such that all pixels from that column index to the rightmost column are filled with the color of the non-white pixel found in the input row. All pixels to the left of that starting column index remain white.
    *   The color of the non-white pixel in the input row determines the color used for filling in the output row.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    transformation_scope: row-wise
    background_color: 0 # white
    objects:
      - type: pixel
        properties:
          - color (non-zero)
          - position (row_index, column_index)
    row_processing:
      condition: presence of a non-white pixel in the input row
      action:
        - identify the first non-white pixel from left to right
        - record its color (C) and column index (idx)
        - generate output row:
          - pixels from column 0 to idx-1 are set to white (0)
          - pixels from column idx to the last column are set to color C
      fallback (if no non-white pixel):
        - copy the input row to the output row (all white)
    grid_properties:
      - dimensions remain constant between input and output
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output grid with the same dimensions as the input grid.
    2.  Iterate through each row of the input grid, keeping track of the row index.
    3.  For the current row:
        a.  Initialize a variable `first_non_white_col` to -1 and `fill_color` to 0 (white).
        b.  Scan the row from left to right (column 0 to the last column).
        c.  If a non-white pixel is encountered at column `c`:
            i.  Set `first_non_white_col` to `c`.
            ii. Set `fill_color` to the color of the pixel at `(row_index, c)`.
            iii. Stop scanning the current row (break the inner loop).
        d.  Construct the corresponding row for the output grid:
            i.  If `first_non_white_col` is -1 (meaning the input row was all white), fill the output row entirely with white (0).
            ii. If `first_non_white_col` is not -1, fill the output row from column `first_non_white_col` to the last column with `fill_color`. Fill columns 0 to `first_non_white_col - 1` with white (0).
    4.  Return the completed output grid.
```python
import numpy as np

"""
Processes each row of the input grid independently.
If a row contains only white pixels (0), the corresponding output row is also all white.
If a row contains a non-white pixel, find the column index of the first (leftmost) non-white pixel. 
The corresponding output row is filled with white pixels up to (but not including) this column index. 
From this column index to the end of the row, the output row is filled with the color of that first non-white pixel found in the input row.
The grid dimensions remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the first non-white pixel in each row.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_np.shape

    # Initialize the output grid with the same shape, filled with white (0)
    output_np = np.zeros_like(input_np)

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row
        row = input_np[r, :]
        
        # Find the indices of all non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in the row
        if non_white_indices.size > 0:
            # Find the column index of the first (leftmost) non-white pixel
            first_non_white_col = non_white_indices[0]
            
            # Get the color of this first non-white pixel
            fill_color = row[first_non_white_col]
            
            # Fill the corresponding output row from this column index onwards with the fill color
            output_np[r, first_non_white_col:] = fill_color
        # else: 
            # If the row contains only white pixels, the corresponding output row
            # remains all white (0), which is its initialized state. No action needed.

    # Convert the NumPy array back to a list of lists for the final output
    return output_np.tolist()
```
```python
import numpy as np

"""
Processes each row of the input grid independently to produce the output grid.
The output grid has the same dimensions as the input grid.
The background color is white (0).

For each row in the input grid:
1. If the row contains only white pixels (0), the corresponding output row is also all white.
2. If the row contains exactly two non-white pixels:
    a. Identify the column index of the leftmost non-white pixel (start_col).
    b. Identify the column index of the rightmost non-white pixel (end_col).
    c. Determine the color (fill_color) of these non-white pixels (they have the same color in the examples).
    d. The corresponding output row is filled with white pixels (0) everywhere except for the segment between start_col and end_col (inclusive). This segment is filled with fill_color.
3. Cases with a number of non-white pixels other than zero or two are not explicitly handled based on the provided examples, but the logic implicitly leaves the output row white if the condition in step 2 isn't met.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling segments in rows based on pairs of non-white pixels.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_np.shape

    # Initialize the output grid with the same shape, filled with the background color (white = 0)
    output_np = np.zeros_like(input_np)

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row
        row = input_np[r, :]
        
        # Find the indices (columns) of all non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]

        # Check if exactly two non-white pixels were found in the row
        if len(non_white_indices) == 2:
            # Get the column index of the first (leftmost) non-white pixel
            start_col = non_white_indices[0]
            # Get the column index of the second (rightmost) non-white pixel
            end_col = non_white_indices[1]
            
            # Get the color of the first non-white pixel (assuming both have the same color)
            fill_color = row[start_col]
            
            # Fill the corresponding segment in the output row
            # The slice includes start_col and end_col
            output_np[r, start_col : end_col + 1] = fill_color
            
        # Else (if the row has 0, 1, or >2 non-white pixels): 
            # The corresponding output row remains all white (0), 
            # which is its initialized state. No explicit action needed.

    # Convert the NumPy array back to a list of lists for the final output format
    return output_np.tolist()
```
