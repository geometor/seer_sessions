
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```


## train_2

**input:**
```
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception**

The input and output grids have the same dimensions in each example. The transformation operates row by row. In the input grids, some rows contain exactly two pixels of the same non-white color (orange or azure in the examples), while the rest of the row is white. Other rows are entirely white. In the output grids, for the rows that contained two non-white pixels in the input, the segment between these two pixels (inclusive) is filled with the same non-white color. Rows that were entirely white in the input remain entirely white in the output. The transformation essentially draws a horizontal line segment connecting the pair of colored pixels found on each relevant row.

**Facts**


```yaml
Input_Output_Relationship:
  - Grid_Dimensions: Input and output grids have the same height and width.
  - Color_Palette: Output grid uses only colors present in the input grid.
  - Transformation_Scope: Operates independently on each row.

Row_Processing:
  - Condition: Identify rows containing exactly two pixels of the same non-white color.
  - Identification:
      - Find the color (C) of these two pixels.
      - Find the column indices (col1, col2) of these two pixels (where col1 < col2).
  - Action:
      - In the output grid's corresponding row, change the color of all pixels from column col1 to col2 (inclusive) to color C.
  - Default_Case: Rows not meeting the condition (e.g., all white, fewer/more than two non-white pixels, or two non-white pixels of different colors) are copied unchanged to the output. (Based on examples, only all-white rows and rows with exactly two same-colored non-white pixels are shown).

Objects:
  - Background: White pixels (color 0).
  - Markers: Non-white pixels (e.g., orange (7), azure (8)). Act as endpoints for filling.
  - Segments: Horizontal lines of non-white pixels created in the output.

Properties:
  - Marker_Color: The specific non-white color (7 or 8).
  - Marker_Position: Row and column index.
  - Row_State: Characterized by the count and color(s) of non-white pixels within it.

Relationships:
  - Pairing: Two non-white pixels on the same row with the same color form a pair.
  - Span: The horizontal distance between the paired pixels defines the segment to be filled.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid.
3.  For the current row, find all non-white pixels and record their colors and column indices.
4.  Check if there are exactly two non-white pixels in the row and if they both have the same color.
5.  If the condition in step 4 is met:
    a.  Identify the color (let's call it `fill_color`).
    b.  Identify the column indices of the two pixels (let's call them `start_col` and `end_col`, ensuring `start_col` is the smaller index).
    c.  In the corresponding row of the output grid, set the color of all pixels from `start_col` to `end_col` (inclusive) to `fill_color`.
6.  If the condition in step 4 is not met, the corresponding row in the output grid remains unchanged (as it was copied from the input initially).
7.  After processing all rows, return the modified output grid.
```python
import numpy as np

def transform(input_grid):
    """
    Processes a grid row by row. If a row contains exactly two pixels of the same 
    non-white color, it fills the segment between these two pixels (inclusive) 
    with that color. Otherwise, the row remains unchanged.

    1. Initialize the output grid as a copy of the input grid.
    2. Iterate through each row of the input grid.
    3. For the current row, find all non-white pixels and record their colors and column indices.
    4. Check if there are exactly two non-white pixels in the row and if they both have the same color.
    5. If the condition is met:
        a. Identify the fill color.
        b. Identify the start and end column indices of the two pixels.
        c. In the corresponding row of the output grid, set the color of all pixels 
           from the start column to the end column (inclusive) to the fill color.
    6. If the condition is not met, the corresponding row in the output grid remains unchanged.
    7. Return the modified output grid.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)
    
    num_rows, num_cols = input_array.shape

    # Iterate through each row
    for r in range(num_rows):
        row = input_array[r, :]
        
        # Find non-white pixels (color != 0) in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are exactly two non-white pixels
        if len(non_white_indices) == 2:
            col1, col2 = non_white_indices
            color1 = row[col1]
            color2 = row[col2]
            
            # Check if the two non-white pixels have the same color
            if color1 == color2:
                fill_color = color1
                start_col = min(col1, col2)
                end_col = max(col1, col2)
                
                # Fill the segment in the output grid's corresponding row
                output_array[r, start_col : end_col + 1] = fill_color
                
    # Convert the numpy array back to a list of lists before returning
    return output_array.tolist()

```
```python
"""
Processes a 2D grid row by row. If a row contains exactly two pixels of the same 
non-white color, it fills the horizontal segment between these two pixels 
(inclusive) with that color in the output grid. Otherwise, the row is copied 
unchanged from the input to the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the row-filling rule.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input_grid, so unchanged rows are preserved
    output_array = np.copy(input_array)
    
    num_rows, _ = input_array.shape

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row
        row = input_array[r, :]
        
        # Find the column indices of all non-white pixels (color != 0) in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if the condition is met: exactly two non-white pixels in the row
        if len(non_white_indices) == 2:
            # Get the column indices of the two non-white pixels
            col1, col2 = non_white_indices
            # Get the colors of these two pixels
            color1 = row[col1]
            color2 = row[col2]
            
            # Check if the two non-white pixels have the same color
            if color1 == color2:
                # This row meets the criteria for filling
                fill_color = color1
                # Determine the start and end columns for filling (inclusive)
                start_col = min(col1, col2)
                end_col = max(col1, col2)
                
                # Fill the segment in the corresponding row of the output grid
                # Use slicing: [start_col : end_col + 1] includes end_col
                output_array[r, start_col : end_col + 1] = fill_color
                
    # Convert the final numpy array back to a list of lists before returning
    return output_array.tolist()

```
