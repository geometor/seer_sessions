
## train_1

**input:**
```
2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
```


## train_3

**input:**
```
7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain a white background (color 0) with a few scattered pixels of a single non-white color (red=2, azure=8, orange=7).
    *   In the rows containing non-white pixels, there are always exactly two such pixels.
    *   The output grids maintain the original positions of the non-white pixels.
    *   The key transformation is filling the horizontal space *between* the pair of non-white pixels in each relevant row with the same non-white color.
    *   Rows that were entirely white in the input remain entirely white in the output.
    *   The transformation acts independently on each row.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_features:
      - grid: 2D array of integers (0-9)
      - background_color: white (0)
      - foreground_objects:
          - type: isolated pixels
          - count_per_row_pattern: exactly two non-white pixels per row (if any non-white pixels are present in that row)
          - color: consistent non-white color within each example (e.g., red in train_1, azure in train_2)
    output_features:
      - grid: 2D array of integers (0-9)
      - background_color: white (0)
      - transformed_objects:
          - type: horizontal line segments
          - color: same as the non-white color from the input row
          - location: spans between the original pair of non-white pixels in each relevant row
    transformation_logic:
      - scope: row-wise
      - condition: process rows containing exactly two non-white pixels of the same color.
      - action: fill the segment between the leftmost and rightmost non-white pixel (inclusive) with that non-white color.
      - unchanged: rows with zero, one, or more than two non-white pixels, or pixels of different non-white colors, remain unchanged.
    relationships:
      - The output line segment's color is determined by the color of the pair of pixels in the input row.
      - The output line segment's start and end columns are determined by the column indices of the pair of pixels in the input row.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each row of the input grid.
    3.  For the current row, identify all non-white pixels, recording their color and column index.
    4.  Check if there are exactly two non-white pixels in the row and if they share the same color.
    5.  If the condition in step 4 is true:
        a.  Determine the non-white color (`fill_color`).
        b.  Find the minimum column index (`min_col`) among the two non-white pixels.
        c.  Find the maximum column index (`max_col`) among the two non-white pixels.
        d.  In the corresponding row of the output grid, set the color of all pixels from column `min_col` to `max_col` (inclusive) to `fill_color`.
    6.  If the condition in step 4 is false, leave the corresponding row in the output grid unchanged (it's already a copy from step 1).
    7.  Return the modified output grid.
```python
import numpy as np

"""
Transforms the input grid by processing each row independently. 
If a row contains exactly two pixels of the same non-white color, 
it fills the horizontal segment between these two pixels (inclusive) 
with that same color. Rows that do not meet this condition remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(num_rows):
        row = input_grid[r, :]
        
        # Find non-white pixels in the current row: their indices and colors
        non_white_indices = np.where(row != 0)[0]
        non_white_colors = row[non_white_indices]

        # Check if there are exactly two non-white pixels
        if len(non_white_indices) == 2:
            # Check if the two non-white pixels have the same color
            color1 = non_white_colors[0]
            color2 = non_white_colors[1]
            
            if color1 == color2:
                # Determine the fill color
                fill_color = color1
                
                # Find the minimum and maximum column indices
                min_col = non_white_indices.min()
                max_col = non_white_indices.max()
                
                # Fill the segment in the output grid's corresponding row
                output_grid[r, min_col : max_col + 1] = fill_color
                
        # If the condition (exactly two non-white pixels of the same color) is not met,
        # the row in the output_grid remains unchanged (as it started as a copy).

    return output_grid
```
```python
import numpy as np

"""
Transforms the input grid by processing each row independently. 
If a row contains exactly two pixels of the same non-white color, 
it fills the horizontal segment between these two pixels (inclusive) 
with that same color. Rows that do not meet this condition remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Extract the current row
        row = input_grid[r, :]
        
        # Find the indices (columns) of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are exactly two non-white pixels in this row
        if len(non_white_indices) == 2:
            # Get the colors of the two non-white pixels
            color1 = row[non_white_indices[0]]
            color2 = row[non_white_indices[1]]
            
            # Check if the two non-white pixels have the same color
            if color1 == color2:
                # Determine the fill color (which is the color of the two pixels)
                fill_color = color1
                
                # Find the minimum (leftmost) and maximum (rightmost) column indices
                # np.min and np.max work directly on the array of indices
                min_col = np.min(non_white_indices)
                max_col = np.max(non_white_indices)
                
                # Fill the segment in the corresponding row of the output grid
                # Slicing is inclusive of the start index and exclusive of the end index,
                # so we use max_col + 1 to include the pixel at max_col.
                output_grid[r, min_col : max_col + 1] = fill_color
                
        # If the conditions (exactly two non-white pixels, same color) are not met,
        # the row in the output_grid remains unchanged because it started as a copy.

    # Return the modified output grid
    return output_grid
```
