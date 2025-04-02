
## train_1

**input:**
```
3 0 3 0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 5 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0 5 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 5 5 5 5 5 5 0
```


## train_3

**input:**
```
3 0 0 3 0 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 0 0 0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on each row of the grid independently. In each row containing non-white pixels, the transformation identifies the horizontal extent spanned by these non-white pixels. It then fills this entire horizontal span (from the leftmost non-white pixel to the rightmost non-white pixel) with the color of the original non-white pixels. Rows containing only white pixels remain unchanged. The examples show cases where two non-white pixels of the same color exist in a row, separated by white pixels. The output fills the gap between them with that same color.

*   **Facts:**
    
```yaml
    task_type: pattern_completion
    scope: row-wise
    objects:
      - type: pixel
        properties:
          - color: (white: 0, green: 3, gray: 5)
          - position: (row, column)
      - type: row
        properties:
          - pixels: list of pixel colors
          - contains_non_white_pixels: boolean
    actions:
      - name: find_non_white_pixels
        on: row
        returns: list of column indices
      - name: find_min_column
        on: list of column indices
        returns: minimum column index
      - name: find_max_column
        on: list of column indices
        returns: maximum column index
      - name: get_pixel_color
        at: (row, column)
        returns: color value
      - name: fill_segment
        target: row segment
        from: column index
        to: column index
        with: color value
    relationships:
      - type: horizontal_span
        between: leftmost non-white pixel and rightmost non-white pixel in a row
    transformation:
      - for each row:
        - if the row contains non-white pixels:
          - find the minimum column index (`min_col`) of non-white pixels
          - find the maximum column index (`max_col`) of non-white pixels
          - determine the fill color (`C`) (e.g., from the pixel at `min_col`)
          - fill the row from `min_col` to `max_col` (inclusive) with color `C`
        - else (row is all white):
          - keep the row unchanged
    ```


*   **Natural Language Program:**
    1.  Iterate through each row of the input grid.
    2.  For the current row, find the column indices of all non-white pixels.
    3.  If any non-white pixels are found:
        a.  Identify the column index of the leftmost non-white pixel (`col_start`).
        b.  Identify the column index of the rightmost non-white pixel (`col_end`).
        c.  Get the color (`C`) of the non-white pixel(s) in that row. (Assumption based on examples: all non-white pixels in a processed row have the same color; use this color).
        d.  In the corresponding output row, change the color of all pixels from column `col_start` to `col_end` (inclusive) to color `C`.
    4.  If no non-white pixels are found in the current row, copy the row unchanged to the output grid.
    5.  Assemble the processed rows into the final output grid.
```python
"""
Iterate through each row of the input grid.
For each row, find the horizontal span between the leftmost and rightmost non-white pixels.
If non-white pixels exist in the row, fill the entire span (from the leftmost to the rightmost non-white pixel, inclusive) with the color of those non-white pixels.
If a row contains only white pixels, leave it unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    For each row, find the min and max column index of non-white pixels.
    Fill the range between min_col and max_col (inclusive) with the color
    of the non-white pixels in that row. Rows with only white pixels remain unchanged.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid_np.copy()
    
    # Get grid dimensions
    height, width = input_grid_np.shape

    # Iterate through each row
    for r in range(height):
        # Get the current row
        row = input_grid_np[r, :]
        
        # Find column indices of non-white pixels (value != 0)
        non_white_indices = np.where(row != 0)[0]

        # Check if there are any non-white pixels in the row
        if non_white_indices.size > 0:
            # Find the minimum column index (leftmost)
            min_col = np.min(non_white_indices)
            # Find the maximum column index (rightmost)
            max_col = np.max(non_white_indices)
            
            # Determine the fill color (assume all non-white pixels in the row
            # should resolve to a single color - use the color of the leftmost one)
            fill_color = row[min_col] 
            
            # Fill the segment in the output grid's corresponding row
            output_grid[r, min_col : max_col + 1] = fill_color
        # No need for an else block, as rows with only white pixels
        # are already correctly represented in the copied output_grid.

    # Convert back to list of lists if necessary, though numpy array is often preferred
    return output_grid.tolist()

```
```python
"""
Iterate through each row of the input grid (which is a 2D list of integers).
For each row, find the horizontal span between the leftmost and rightmost non-white pixels (pixels with value > 0).
If non-white pixels exist in the row, fill the entire span in the output grid's corresponding row (from the leftmost to the rightmost non-white pixel's column, inclusive) with the color of those non-white pixels. Assume all non-white pixels within a single row share the same color, based on the examples.
If a row contains only white pixels (value 0), copy it unchanged to the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling the horizontal span between the
    outermost non-white pixels in each row with their color.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid.
    # This handles rows with only white pixels correctly by default.
    output_grid = input_grid_np.copy()
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Get the current row
        row = input_grid_np[r, :]
        
        # Find the column indices of all non-white pixels (value != 0) in this row
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in this row
        if non_white_indices.size > 0:
            # Find the minimum column index (leftmost non-white pixel)
            min_col = np.min(non_white_indices)
            # Find the maximum column index (rightmost non-white pixel)
            max_col = np.max(non_white_indices)
            
            # Determine the fill color. Based on examples, all non-white pixels
            # in a row that needs filling have the same color. We can pick the
            # color of the leftmost non-white pixel.
            fill_color = row[min_col] 
            
            # Fill the segment in the output grid's corresponding row
            # The slice goes from min_col up to (but not including) max_col + 1
            output_grid[r, min_col : max_col + 1] = fill_color
            
    # Convert the final NumPy array back to a list of lists for the return value
    return output_grid.tolist()

```
```python
"""
Transforms the input grid by processing each row independently.
For each row, finds the horizontal span between the leftmost and rightmost non-white pixels.
If non-white pixels exist in the row, fills the entire span in the output grid's corresponding row 
(from the leftmost to the rightmost non-white pixel's column, inclusive) with the color of those 
non-white pixels. Assumes all non-white pixels within a single row share the same color, based on the examples.
If a row contains only white pixels (value 0), copies it unchanged to the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a row-wise transformation to fill horizontal segments.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid.
    # This ensures rows with only white pixels are handled correctly by default.
    output_grid = input_grid_np.copy()
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape

    # Iterate through each row of the grid using its index 'r'
    for r in range(height):
        # Get the current row from the input grid
        row = input_grid_np[r, :]
        
        # Find the column indices of all non-white pixels (value != 0) in this row
        # np.where returns a tuple of arrays (one for each dimension), we need the first element [0]
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in this row
        if non_white_indices.size > 0:
            # Find the minimum column index (leftmost non-white pixel)
            min_col = np.min(non_white_indices)
            # Find the maximum column index (rightmost non-white pixel)
            max_col = np.max(non_white_indices)
            
            # Determine the fill color. Based on examples, all non-white pixels
            # in a row that needs filling have the same color. We can safely pick the
            # color of the leftmost non-white pixel found.
            fill_color = row[min_col] 
            
            # Fill the segment in the output grid's corresponding row
            # The slice `min_col : max_col + 1` includes columns from min_col up to max_col.
            output_grid[r, min_col : max_col + 1] = fill_color
            
    # Convert the final NumPy array back to a list of lists for the return value
    return output_grid.tolist()

```
