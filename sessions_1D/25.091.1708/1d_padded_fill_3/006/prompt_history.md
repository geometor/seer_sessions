
## train_1

**input:**
```
0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0
```

*   **Perception:**
    *   The input grids contain a white background (0) and scattered pixels of a single non-white color (red, magenta, or blue in the examples).
    *   The output grids retain the same dimensions and the same white background.
    *   The key transformation happens within rows that contain non-white pixels in the input.
    *   In these rows, a horizontal line of the *same* non-white color is drawn in the output.
    *   This line spans horizontally from the column of the leftmost non-white pixel to the column of the rightmost non-white pixel within that specific row.
    *   All pixels between these start and end columns (inclusive) in that row are filled with the non-white color.
    *   Rows that are entirely white in the input remain entirely white in the output.
    *   The transformation appears to be row-independent.

*   **YAML Facts:**
    
```yaml
    task_type: line_drawing
    focus: row_based_transformation
    objects:
      - type: background
        color: white (0)
        role: static
      - type: colored_pixels
        color: non-white (1, 2, 6 in examples)
        role: markers
        properties:
          - scattered_distribution
    actions:
      - name: identify_row_extents
        inputs: row, colored_pixels
        outputs: min_col_index, max_col_index, color
        description: For each row containing colored_pixels, find the minimum and maximum column index of those pixels and identify their color.
      - name: draw_horizontal_line
        inputs: row_index, min_col_index, max_col_index, color
        outputs: modified_row
        description: In the output grid's corresponding row, fill pixels from min_col_index to max_col_index (inclusive) with the identified color.
      - name: copy_row
        inputs: row
        outputs: identical_row
        description: If a row contains no colored_pixels, copy it unchanged to the output.
    relationships:
      - type: containment
        description: Colored pixels are contained within specific rows.
      - type: boundary
        description: The leftmost and rightmost colored pixels in a row define the horizontal boundaries for the line drawn in the output.
      - type: color_preservation
        description: The color of the pixels in the input determines the color of the line drawn in the output for that row.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output grid with the same dimensions as the input grid, filled with white (0).
    2.  Iterate through each row of the input grid, keeping track of the current row index.
    3.  For the current row:
        a.  Find all non-white pixels and record their column indices and color.
        b.  If no non-white pixels are found in the row, proceed to the next row (the corresponding output row remains white).
        c.  If non-white pixels are found:
            i.  Determine the color of these pixels (assume only one non-white color per row based on examples).
            ii. Find the minimum column index (`min_col`) among the non-white pixels.
            iii. Find the maximum column index (`max_col`) among the non-white pixels.
            iv. In the output grid, for the current row index, set the color of all pixels from column `min_col` to `max_col` (inclusive) to the identified non-white color.
    4.  After processing all rows, return the completed output grid.
```python
"""
Transforms an input grid by processing each row independently. 
For each row in the input grid:
1. Find all non-white pixels (value > 0).
2. If non-white pixels exist:
   a. Identify their color (assuming only one non-white color per row).
   b. Find the minimum column index (leftmost) and maximum column index (rightmost) of these non-white pixels.
   c. In the corresponding row of the output grid, draw a horizontal line of that color from the minimum column index to the maximum column index (inclusive).
3. If a row contains only white pixels (value = 0), the corresponding row in the output grid remains all white.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row-based horizontal line drawing transformation.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid. 
    # This handles rows that are entirely white correctly.
    output_grid = np.copy(input_grid) 
    height, width = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_grid[r, :]
        
        # Find the column indices of non-white pixels in the current row
        non_white_indices = np.where(row > 0)[0]

        # Check if there are any non-white pixels in this row
        if non_white_indices.size > 0:
            # Determine the color (use the color of the first non-white pixel found)
            color = row[non_white_indices[0]]
            
            # Find the minimum (leftmost) and maximum (rightmost) column index
            min_col = np.min(non_white_indices)
            max_col = np.max(non_white_indices)
            
            # Fill the corresponding row in the output grid with the color 
            # between min_col and max_col (inclusive)
            output_grid[r, min_col : max_col + 1] = color
        # else: 
            # If the row was all white, the output_grid row (copied from input) is already correct.

    return output_grid

```
```python
"""
Transforms an input grid by processing each row independently.
For each row in the input grid:
1. Find the column indices of all non-white pixels (value > 0).
2. If there are two or more non-white pixels in the row:
   a. Identify the color of the first non-white pixel found.
   b. Find the column index of the first (leftmost) non-white pixel.
   c. Find the column index of the second non-white pixel from the left.
   d. In the corresponding row of the output grid, draw a horizontal line segment 
      using the identified color, starting from the first non-white pixel's column 
      and ending at the second non-white pixel's column (inclusive).
3. If a row contains fewer than two non-white pixels, the corresponding row in 
   the output grid is identical to the input row.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row-based horizontal line drawing transformation based on the 
    first two non-white pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    # This handles rows with 0 or 1 non-white pixels correctly, as they
    # should remain unchanged according to the rule interpretation.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_grid[r, :]
        
        # Find the column indices of non-white pixels in the current row
        # These indices are already sorted because np.where scans left-to-right.
        non_white_indices = np.where(row > 0)[0]

        # Check if there are at least two non-white pixels in this row
        if non_white_indices.size >= 2:
            # Determine the color (use the color of the first non-white pixel)
            color = row[non_white_indices[0]]
            
            # Get the column index of the first non-white pixel (leftmost)
            start_col = non_white_indices[0]
            
            # Get the column index of the second non-white pixel
            end_col = non_white_indices[1]
            
            # Fill the corresponding row segment in the output grid with the color 
            # between start_col and end_col (inclusive)
            # Note: Slicing is exclusive of the end index, so use end_col + 1
            output_grid[r, start_col : end_col + 1] = color
        # else: 
            # If the row has fewer than 2 non-white pixels, the output_grid row 
            # (copied from input) is already correct.

    return output_grid
```
```python
"""
Transforms an input grid by processing each row independently.
For each row in the input grid:
1. Find all non-white pixels (value > 0).
2. If non-white pixels exist:
   a. Identify their color (assuming only one non-white color per row based on examples).
   b. Find the minimum column index (leftmost) of these non-white pixels.
   c. Find the maximum column index (rightmost) of these non-white pixels.
   d. In the corresponding row of the output grid, draw a horizontal line of that color, filling all pixels from the minimum column index to the maximum column index (inclusive).
3. If a row contains only white pixels (value = 0), the corresponding row in the output grid remains all white.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row-based horizontal line drawing transformation based on the
    full extent of non-white pixels in each row.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    # This ensures that rows containing only white pixels (0) are correctly
    # represented in the output without extra steps.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(height):
        # Get the current row
        row = input_grid[r, :]

        # Find the column indices of non-white pixels in this row
        # np.where returns a tuple of arrays, we need the first element for 1D rows
        non_white_indices = np.where(row > 0)[0]

        # Check if any non-white pixels were found in this row
        if non_white_indices.size > 0:
            # Determine the color from the first non-white pixel found
            # (Assuming consistent color within the row based on examples)
            color = row[non_white_indices[0]]

            # Find the minimum (leftmost) column index among non-white pixels
            min_col = np.min(non_white_indices)

            # Find the maximum (rightmost) column index among non-white pixels
            max_col = np.max(non_white_indices)

            # Fill the segment in the corresponding output row with the determined color
            # Slicing is exclusive of the end index, so use max_col + 1
            output_grid[r, min_col : max_col + 1] = color
        # else:
            # If non_white_indices is empty, the row was all white in the input.
            # Since output_grid was initialized as a copy, this row is already
            # correctly all white in the output. No action needed.

    # Return the modified grid
    return output_grid
```
