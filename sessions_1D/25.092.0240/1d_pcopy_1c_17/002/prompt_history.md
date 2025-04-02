
## train_1

**input:**
```
0 2 2 2 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 0 0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids are mostly white (background).
    *   Each input contains a dominant color (red, yellow, or gray).
    *   The topmost non-white pixels in the input always form a contiguous horizontal line. Let's call this the "reference line".
    *   Below the reference line, there might be one or more isolated pixels of the same dominant color.
    *   In the output, the reference line remains unchanged.
    *   For rows below the reference line in the input that contain *at least one* pixel of the dominant color, the corresponding row segment in the output is filled entirely with the dominant color, matching the horizontal extent (column start and end) of the reference line.
    *   If a row below the reference line does not contain any pixel of the dominant color in the input, it remains unchanged in the output.
    *   Pixels outside the column range of the reference line are unaffected.

*   **Facts:**
    
```yaml
    task_context:
      - Grid Transformation: Modifying pixels based on spatial relationships and color identity.
      - Color Focus: Operations primarily concern one non-white color per example, determined by the topmost structure.
      - Background: White pixels (0) are treated as background and are generally not modified unless specifically filled.
    
    elements:
      - type: Reference Line
        description: The topmost contiguous horizontal sequence of non-white pixels in the input grid.
        properties:
          - color: The single non-white color of the pixels in the line (e.g., red, yellow, gray). Let's call this C.
          - row_index: The row where this line occurs. Let's call this R.
          - column_range: The start and end column indices of the line. Let's call this [min_col, max_col].
      - type: Trigger Pixel
        description: Any pixel in a row below R (row index > R) that has the color C.
        properties:
          - color: Must be color C.
          - row_index: Must be greater than R.
          - column_index: Any column index.
      - type: Affected Row Segment
        description: A horizontal segment in the output grid corresponding to a row that contained a Trigger Pixel in the input.
        properties:
          - color: All pixels in this segment are set to color C.
          - row_index: Same as the row index of the Trigger Pixel(s) in that row.
          - column_range: Spans from min_col to max_col (inclusive), matching the Reference Line's column range.
    
    relationships:
      - The Reference Line defines the target color (C) and the horizontal boundaries ([min_col, max_col]) for modifications in subsequent rows.
      - The presence of at least one Trigger Pixel in a row `r > R` activates the transformation for that row.
      - The transformation fills the Affected Row Segment in the output grid for row `r` using color C and column range [min_col, max_col].
    
    actions:
      - Identify: Find the Reference Line (topmost horizontal non-white segment). Extract its color C, row R, and column range [min_col, max_col].
      - Scan: Iterate through rows below R (r > R).
      - Check: For each row r, determine if any pixel has color C.
      - Fill: If a check is positive for row r, modify the output grid by setting pixels from (r, min_col) to (r, max_col) to color C.
      - Copy: Unmodified pixels (including the reference line, rows below R without trigger pixels, and pixels outside the [min_col, max_col] range) retain their original values from the input.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Scan the input grid row by row from top to bottom to find the first row containing any non-white pixels.
    3.  Identify the contiguous horizontal segment of non-white pixels in this first non-white row. This is the "reference line".
    4.  Record the color (C), the row index (R), the starting column index (min_col), and the ending column index (max_col) of the reference line.
    5.  Iterate through each row `r` below the reference line (i.e., for `r` from `R + 1` to the last row).
    6.  For the current row `r`, check if there exists *any* pixel in the input grid at `(r, c)` (for any column `c`) that has the color C.
    7.  If such a pixel exists in row `r`, then modify the output grid: set all pixels from column `min_col` to `max_col` (inclusive) in row `r` to color C.
    8.  If no pixel of color C exists in row `r` in the input, the row `r` in the output grid remains unchanged from the initial copy.
    9.  Return the modified output grid.
```python
import numpy as np
import copy

def find_reference_line(grid):
    """
    Finds the topmost contiguous horizontal segment of non-white pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (color, row_index, min_col, max_col) or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        non_white_indices = np.where(grid[r] != 0)[0]
        if len(non_white_indices) > 0:
            # Check for contiguity (simple check: is the range of indices equal to the count?)
            min_c = np.min(non_white_indices)
            max_c = np.max(non_white_indices)
            
            # Extract the segment and check if all colors are the same and non-white
            segment = grid[r, min_c : max_c + 1]
            if np.all(segment != 0):
                 # More robust contiguity check: ensure no zeros within the min/max bounds
                if np.all(grid[r, min_c : max_c + 1] != 0):
                     # Check if all elements in the segment are the same color
                     if len(np.unique(segment)) == 1:
                          color = segment[0]
                          return color, r, min_c, max_c

    return None # No reference line found

def transform(input_grid_list):
    """
    Transforms the input grid based on the following rules:
    1. Find the topmost contiguous horizontal line of a single non-white color (the "reference line").
    2. Identify its color (C), row (R), start column (min_col), and end column (max_col).
    3. For each row below R (r > R):
       a. Check if any pixel in that row (in the input grid) has the color C.
       b. If yes, fill the segment in the output grid from (r, min_col) to (r, max_col) with color C.
       c. Otherwise, keep the row as it is.
    4. Rows R and above, and pixels outside the min_col to max_col range in rows below R (if not filled), remain unchanged.
    """
    input_grid = np.array(input_grid_list)
    output_grid = copy.deepcopy(input_grid)
    rows, cols = input_grid.shape

    # Find the reference line
    reference_info = find_reference_line(input_grid)

    if reference_info is None:
        # No reference line found, return the original grid
        return output_grid.tolist()

    color_c, row_r, min_col, max_col = reference_info

    # Iterate through rows below the reference line
    for r in range(row_r + 1, rows):
        # Check if any pixel in the current input row 'r' has color C
        trigger_found = False
        for c in range(cols):
            if input_grid[r, c] == color_c:
                trigger_found = True
                break # Found one, no need to check further in this row

        # If a trigger pixel was found, fill the corresponding segment in the output grid
        if trigger_found:
            for c_fill in range(min_col, max_col + 1):
                 # Ensure we don't write out of bounds, although min/max_col should be valid
                 if c_fill < cols:
                     output_grid[r, c_fill] = color_c

    return output_grid.tolist()
```
