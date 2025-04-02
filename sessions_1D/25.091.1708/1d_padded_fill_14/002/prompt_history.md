
## train_1

**input:**
```
0 6 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 4 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming 2D grids. Each input grid consists of several rows, and each row contains exactly two pixels of the same non-white color, separated by white pixels. The remaining pixels in the grid are white. The transformation operates row by row. For each row, the segment horizontally connecting the two non-white pixels (inclusive) is filled with that same non-white color in the output grid. The dimensions of the grid remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      - dimensions_preserved: True
      - background_color: white (0)
    row_processing:
      - independent: True
    input_row_pattern:
      - object: pair_of_pixels
        properties:
          - color: non-white (varies per example: magenta, green, yellow)
          - count: 2
          - separation: variable number of white pixels
          - alignment: horizontal
      - object: other_pixels
        properties:
          - color: white (0)
    output_row_pattern:
      - action: fill_segment
        parameters:
          - start_pixel: first non-white pixel in the input row
          - end_pixel: second non-white pixel in the input row
          - color: the non-white color from the input row
        target: the segment between and including the start and end pixels
      - object: other_pixels
        properties:
          - color: white (0)
    relationships:
      - The output row's non-white segment corresponds directly to the positions of the two non-white pixels in the input row.
      - The color used for filling is identical to the color of the pair of pixels in the input row.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output grid with the same dimensions as the input grid, filled with white pixels.
    2.  Iterate through each row of the input grid.
    3.  For the current row:
        a.  Find the column indices of the two non-white pixels. Let these be `col1` and `col2`, where `col1` is the smaller index.
        b.  Identify the color of these non-white pixels. Let this be `fill_color`.
        c.  In the corresponding row of the output grid, change the color of all pixels from column `col1` to column `col2` (inclusive) to `fill_color`.
    4.  Return the completed output grid.
```python
"""
Processes each row of the input grid independently. 
Finds the first and last occurrence of a non-white pixel in a row.
Fills the segment between these two pixels (inclusive) with the non-white color found in that row.
If a row contains no non-white pixels or only one, it remains unchanged (filled with white).
"""

import numpy as np

def transform(input_grid):
    """
    Fills the horizontal segment between the first and last non-white pixel in each row
    with that row's non-white color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape
    
    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid) 

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_grid[r, :]
        
        # Find the indices of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are at least two non-white pixels in the row
        if len(non_white_indices) >= 2:
            # Get the column index of the first non-white pixel
            col1 = non_white_indices[0]
            # Get the column index of the last non-white pixel
            col2 = non_white_indices[-1]
            
            # Get the color of the first non-white pixel (assuming all non-white pixels in a row are the same color as per examples)
            fill_color = row[col1]
            
            # Fill the segment between col1 and col2 (inclusive) in the output row with the fill_color
            output_grid[r, col1 : col2 + 1] = fill_color
        elif len(non_white_indices) == 1:
             # If only one non-white pixel, copy it to the output
             col = non_white_indices[0]
             output_grid[r, col] = row[col]
        # If no non-white pixels, the output row remains white (already initialized)

    return output_grid
```
