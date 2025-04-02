
## train_1

**input:**
```
0 0 9 9 9 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 8 8 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 0 0 5 0 0 0 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 5 5 5 0 0 5 5 5 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are grids. Based on the number of elements (33) and the visual structure suggested by the examples, the grids are likely 11 rows by 3 columns (11x3).
    *   Each example features a white background (color 0) and one other color (maroon 9, azure 8, gray 5).
    *   The core transformation involves identifying specific non-white pixels in the input and modifying their entire row in the output.
    *   The non-white pixels that trigger this change appear to be *isolated*. An isolated pixel is one that is not adjacent (horizontally, vertically, or diagonally) to any other non-white pixel.
    *   When an isolated non-white pixel is found, its corresponding row in the output grid is filled entirely with that pixel's color.
    *   Non-white pixels that are *not* isolated (i.e., they are part of a larger shape or touch another non-white pixel) remain unchanged in the output.
    *   White pixels remain white unless they are part of a row that gets filled by the color of an isolated pixel.

*   **Facts:**
    
```yaml
    task_context:
      grid_representation: 2D array of integers (colors)
      grid_dimensions: inferred as 11x3 (height x width)
      colors_present:
        - 0: white (background)
        - non-zero: foreground colors (maroon, azure, gray in examples)
    
    objects:
      - type: pixel
        properties:
          color: integer 0-9
          position: (row, column)
          is_isolated: boolean (true if all 8 neighbors are white, false otherwise)
      - type: row
        properties:
          index: integer (0 to height-1)
          pixels: list of pixels in the row
    
    transformation:
      type: conditional_row_fill
      condition: applies to rows containing at least one isolated non-white pixel
      action:
        - identify all isolated non-white pixels in the input grid.
        - for each identified isolated pixel:
            - determine its color (C) and row index (R).
            - in the output grid, set all pixels in row R to color C.
      unchanged_elements:
        - rows containing no isolated non-white pixels remain identical to the input rows.
        - note: non-isolated non-white pixels within a modified row are overwritten.
    
    relationships:
      - pixel_neighbor: adjacency (horizontal, vertical, diagonal) used to determine isolation.
      - pixel_to_row: a pixel belongs to a specific row.
      - isolated_pixel_triggers_row_fill: an isolated pixel dictates the color fill for its entire row.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel of the input grid at position (row, column) that is not white (color > 0).
    3.  For each non-white pixel, check all 8 of its neighbors (up, down, left, right, and diagonals).
    4.  Determine if the current non-white pixel is "isolated": count how many of its neighbors are *not* white. If this count is zero, the pixel is isolated.
    5.  If a non-white pixel at (row, column) with color C is found to be isolated:
        a.  Modify the output grid by setting the color of *all* pixels in the `row`-th row to C.
    6.  After checking all non-white pixels, the final state of the output grid represents the result. (Note: If multiple isolated pixels exist in the same row, the last one processed by the iteration order would determine the final row color, but based on the examples, it seems only one isolated pixel exists per row that gets modified, or all isolated pixels in a row share the same color). A slightly better approach is to first identify all rows that need modification based on containing *any* isolated pixel, then perform the modification. Let's refine:
    
    **Refined Natural Language Program:**
    1. Create a list to store the row indices and colors of isolated pixels found: `isolated_pixels_info = []`.
    2. Iterate through each pixel of the input grid at position (row, col).
    3. If the pixel `input[row][col]` is not white:
        a. Check all 8 neighbors of `input[row][col]`.
        b. Count the number of non-white neighbors.
        c. If the count is 0, then the pixel is isolated. Record its row index and color: add `(row, input[row][col])` to `isolated_pixels_info`.
    4. Initialize the output grid as a copy of the input grid.
    5. Iterate through the recorded `isolated_pixels_info`. For each `(row, color)` pair:
        a. Set all pixels in the `row`-th row of the output grid to `color`.
    6. Return the final output grid.
```python
import numpy as np

"""
Identify isolated non-white pixels in the input grid. An isolated pixel is defined as a non-white pixel (value > 0) where all 8 of its adjacent neighbors (horizontal, vertical, and diagonal) are white (value 0). 
For each row containing at least one such isolated pixel, find the color of one of these isolated pixels (if multiple isolated pixels exist in the same row, any of their colors can be used, as the examples suggest they will have the same color or the effect is determined by one). 
Fill the entire corresponding row in the output grid with that color. 
Rows that do not contain any isolated non-white pixels remain unchanged from the input.
"""

def is_isolated(grid, r, c):
    """
    Checks if the pixel at (r, c) in the grid is isolated.
    An isolated pixel is non-white and has only white neighbors.
    Assumes the pixel at (r, c) is already checked to be non-white.
    """
    rows, cols = grid.shape
    # Iterate through all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the pixel itself
            if dr == 0 and dc == 0:
                continue
                
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If a neighbor is not white (0), the pixel is not isolated
                if grid[nr, nc] != 0:
                    return False
    # If all neighbors are white (or out of bounds), the pixel is isolated
    return True

def transform(input_grid):
    """
    Transforms the input grid based on isolated pixels.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Keep track of rows that have already been filled to avoid redundant checks/fills
    # Although not strictly necessary based on examples, it's slightly more efficient.
    filled_rows = set() 

    # Iterate through each pixel of the input grid
    for r in range(rows):
        # If row already processed, skip
        if r in filled_rows:
            continue
            
        for c in range(cols):
            pixel_color = input_np[r, c]
            
            # Check if the pixel is non-white
            if pixel_color != 0:
                # Check if the non-white pixel is isolated
                if is_isolated(input_np, r, c):
                    # If isolated, fill the entire row in the output grid with its color
                    output_np[r, :] = pixel_color
                    # Mark row as filled and break the inner loop for this row
                    filled_rows.add(r)
                    break # Move to the next row once an isolated pixel fills this one

    # Convert the final NumPy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid

```
```python
import numpy as np

"""
Identifies non-white pixels (value > 0) in the input grid that are "horizontally isolated". 
A pixel is horizontally isolated if its immediate left and right neighbors within the same row are both white (value 0). 
Pixels in the first or last column only need to check their single horizontal neighbor.
For each row containing at least one such horizontally isolated pixel, the entire row in the output grid is filled with the color of that horizontally isolated pixel. 
If multiple horizontally isolated pixels exist in the same row, the examples suggest they share the same color, so any one of their colors can be used.
Rows that do not contain any horizontally isolated non-white pixels remain unchanged from the input.
"""

def transform(input_grid):
    """
    Transforms the input grid based on horizontally isolated pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Dictionary to store which rows need modification and with which color
    rows_to_modify = {} 

    # Iterate through each pixel of the input grid
    for r in range(rows):
        # Skip rows already marked for modification (optimization)
        if r in rows_to_modify:
            continue

        for c in range(cols):
            pixel_color = input_np[r, c]
            
            # Check if the pixel is non-white
            if pixel_color != 0:
                # Check horizontal neighbors
                # Assume left neighbor is white if it's the first column (c=0)
                left_neighbor_white = (c == 0) or (input_np[r, c-1] == 0)
                # Assume right neighbor is white if it's the last column (c=cols-1)
                right_neighbor_white = (c == cols-1) or (input_np[r, c+1] == 0)
                
                # If both horizontal neighbors are white, the pixel is horizontally isolated
                if left_neighbor_white and right_neighbor_white:
                    # Record the row index and the color to fill with
                    rows_to_modify[r] = pixel_color
                    # Since we found a trigger for this row, we can move to the next row
                    break 

    # Apply the modifications to the output grid
    for row_index, fill_color in rows_to_modify.items():
        output_np[row_index, :] = fill_color

    # Convert the final NumPy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid
```
