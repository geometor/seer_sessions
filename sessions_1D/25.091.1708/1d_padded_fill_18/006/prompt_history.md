
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0
```


## train_3

**input:**
```
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    The input grids are primarily composed of the background color white (0), with a few scattered pixels of a single non-background color (azure (8), blue (1), or orange (7) in the examples). The non-background pixels appear in distinct rows. The output grids retain the same dimensions as the input. The transformation operates row by row. For each row in the input grid that contains non-background pixels, the output grid fills the horizontal segment between the leftmost and rightmost occurrences of that non-background color in that row with the same color. Rows containing only the background color remain unchanged.

*   **Facts**:
    
```yaml
    task_type: shape_completion
    scope: row-wise
    objects:
      - type: background_pixel
        color: white (0)
      - type: colored_pixel
        color: non-white (e.g., azure, blue, orange)
        properties:
          - row_index
          - column_index
    actions:
      - identify_rows_with_colored_pixels
      - for_each_identified_row:
          - find_colored_pixel_color: C
          - find_min_column_index: min_col
          - find_max_column_index: max_col
          - fill_horizontal_segment:
              from: (row_index, min_col)
              to: (row_index, max_col)
              color: C
    relationships:
      - pixels within the same row
      - leftmost and rightmost colored pixels define the bounds of the filled segment in a row
    state_changes:
      - background_pixels within the identified horizontal segment [min_col, max_col] in a relevant row change to the colored_pixel_color C.
      - colored_pixels remain the same color.
      - background_pixels outside the identified segments remain white.
      - rows with only background_pixels remain unchanged.
    assumptions:
      - Within a single row containing colored pixels, all colored pixels share the same color.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each row of the input grid.
    3.  For the current row, identify the indices of all columns containing non-white pixels.
    4.  If no non-white pixels are found in the current row, proceed to the next row.
    5.  If non-white pixels are found:
        a.  Determine the color (`C`) of the first non-white pixel encountered in the row (based on the assumption that all non-white pixels in a relevant row share the same color).
        b.  Find the minimum column index (`min_col`) among the non-white pixels in this row.
        c.  Find the maximum column index (`max_col`) among the non-white pixels in this row.
        d.  In the corresponding row of the output grid, change the color of all pixels from column `min_col` to `max_col` (inclusive) to color `C`.
    6.  After processing all rows, return the modified output grid.
```python
"""
For each row in the input grid:
1. Identify if any non-white pixels exist in the row.
2. If non-white pixels exist:
    a. Determine the color (C) of these pixels (assuming they are all the same color within a row).
    b. Find the column index of the leftmost non-white pixel (min_col).
    c. Find the column index of the rightmost non-white pixel (max_col).
    d. Fill the segment of the row in the output grid from min_col to max_col (inclusive) with color C.
3. If no non-white pixels exist, the row remains unchanged.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills the horizontal segment between the leftmost and rightmost non-white pixels
    in each row with the color of those pixels.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        row = input_grid[r, :]
        # Find the indices of non-white pixels (color != 0)
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in this row
        if len(non_white_indices) > 0:
            # Find the minimum and maximum column indices of non-white pixels
            min_col = np.min(non_white_indices)
            max_col = np.max(non_white_indices)

            # Get the color from the first non-white pixel found in this row
            # Assumes all non-white pixels in a relevant row have the same color
            fill_color = row[min_col]

            # Fill the segment in the output grid row
            output_grid[r, min_col : max_col + 1] = fill_color

    return output_grid
```
```python
"""
For each row in the input grid:
1. Identify if any non-white pixels (pixels with value != 0) exist in the row.
2. If non-white pixels exist:
    a. Determine the color (C) of these pixels (using the color of the leftmost one).
    b. Find the column index of the leftmost non-white pixel (min_col).
    c. Find the column index of the rightmost non-white pixel (max_col).
    d. In the output grid's corresponding row, fill the horizontal segment from min_col to max_col (inclusive) with color C.
3. If no non-white pixels exist in the row, the row remains unchanged in the output grid.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills the horizontal segment between the leftmost and rightmost non-white pixels
    in each row with the color of those pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Get the current row from the input grid
        row = input_grid[r, :]
        
        # Find the indices (columns) of non-white pixels (color != 0) in the current row
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in this row
        if len(non_white_indices) > 0:
            # Find the minimum (leftmost) column index of non-white pixels
            min_col = np.min(non_white_indices)
            # Find the maximum (rightmost) column index of non-white pixels
            max_col = np.max(non_white_indices)

            # Get the color from the first (leftmost) non-white pixel found in this row
            # Assumes all non-white pixels in a relevant row have the same color,
            # or at least that the leftmost color determines the fill color.
            fill_color = row[min_col]

            # Fill the segment in the corresponding output grid row
            # The slice includes min_col and max_col
            output_grid[r, min_col : max_col + 1] = fill_color
        # If no non-white pixels are found, the row in output_grid remains as copied from input_grid

    return output_grid
```
```python
"""
Identify the single non-white color (C) present in the input grid. Find the minimum (global_min_col) and maximum (global_max_col) column indices across all pixels of color C. Identify all rows (target_rows) that contain at least one pixel of color C. Initialize the output grid as a copy of the input. For each row index r, if r is in target_rows, fill the segment in the output grid's row r from global_min_col to global_max_col (inclusive) with color C. Rows not in target_rows remain unchanged.
"""

import numpy as np

def find_non_white_pixels(grid):
    """Finds the coordinates and color of non-white pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None, None, None  # No non-white pixels found
    
    # Assuming only one non-white color exists
    color = grid[rows[0], cols[0]]
    coordinates = list(zip(rows, cols))
    return color, coordinates, (rows, cols) # Return color, list of (r,c) tuples, and separate row/col arrays

def get_global_bounds(col_indices):
    """Calculates the minimum and maximum column indices."""
    if not col_indices.size: # Check if the array is empty
         return None, None
    min_col = np.min(col_indices)
    max_col = np.max(col_indices)
    return min_col, max_col

def get_target_rows(row_indices):
    """Finds the unique row indices containing non-white pixels."""
    return np.unique(row_indices)


def transform(input_grid):
    """
    Fills horizontal segments in specific rows based on the global horizontal
    extent of a single non-white color.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the non-white pixels, their color, and their coordinates
    primary_color, _, indices = find_non_white_pixels(input_grid)
    
    # If no non-white pixels are found, return the original grid copy
    if primary_color is None:
        return output_grid
        
    row_indices, col_indices = indices

    # Calculate the global minimum and maximum column indices for the primary color
    global_min_col, global_max_col = get_global_bounds(col_indices)

    # Identify the unique rows containing the primary color
    target_rows = get_target_rows(row_indices)

    # Iterate through the identified target rows
    for r in target_rows:
        # Fill the horizontal segment in the output grid for the current target row
        # using the global column bounds and the primary color
        # Ensure slicing includes the max_col index
        output_grid[r, global_min_col : global_max_col + 1] = primary_color

    return output_grid
```
