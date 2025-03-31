
## train_1

**input:**
```
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 8 0 0 0 8 0 0 0 2
0 8 0 0 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
8 0 0 0 8 0 0 0 0 2
8 0 0 0 8 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0
0 0 0 8 0 0 0 0 0 2
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
```


## train_2

**input:**
```
0 8 0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 8 0 8 0 8 0 0
0 8 0 0 0 8 0 8 0 8 0 0
0 8 0 0 0 8 0 8 0 8 0 0
0 8 0 0 0 8 0 8 0 8 0 0
2 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
2 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0
```

*   **Perception:**
    *   The task involves transforming grids containing white (0), azure (8), and red (2) pixels.
    *   The transformation logic appears to depend on the initial positions of the azure and red pixels.
    *   Two distinct transformation modes are observed based on the input configuration:
        1.  **Mode 1 (Examples 1 & 2):** Triggered when azure pixels are present in the first row (row 0). Azure pixels in the first row define a vertical pattern. This pattern propagates downwards. When a row containing a red pixel (acting as a trigger) is encountered in the input, the pattern shifts one column to the left for subsequent rows. The propagated azure pattern only colors pixels that were originally white in the input grid; existing non-white pixels (like the red triggers) are preserved.
        2.  **Mode 2 (Example 3):** Triggered when no azure pixels are in the first row, but azure pixels *are* present in the first column (column 0). Each azure pixel in the first column at row `r` triggers the drawing of three horizontal, 4-pixel-wide azure blocks in the output: one starting at `(r, 0)`, one at `(r-1, 4)`, and one at `(r-2, 8)`. These blocks overwrite existing pixels in the output grid at their locations. All other pixels from the input grid (like the red pixels in Example 3) are preserved in their original positions unless overwritten by the drawn blocks.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    colors_used:
      - white (0)
      - azure (8)
      - red (2)
    rules:
      - condition: Azure (8) pixels exist in the first row (row 0).
        mode: vertical_shift
        elements:
          - role: pattern_definition
            color: azure (8)
            location: first row (row 0)
            property: column indices define the initial pattern
          - role: trigger
            color: red (2)
            location: any row
            action: causes the pattern to shift left by 1 column in subsequent rows
          - role: background
            color: white (0)
            action: can be overwritten by the azure pattern
          - role: preserved_pixels
            color: non-white pixels from input (e.g., red triggers)
            action: are not overwritten by the azure pattern
        transformation:
          - Initialize output grid as a copy of the input.
          - Identify initial azure column pattern from row 0.
          - Iterate through rows top to bottom.
          - Maintain the current column pattern.
          - For each row `r`:
            - Apply the current pattern: for each column `c` in the pattern, if `input[r, c]` is white (0), set `output[r, c]` to azure (8).
            - Check if input row `r` contains any red (2) pixels.
            - If yes, update the pattern for subsequent rows by shifting all column indices left by 1 (discarding negative indices).
      - condition: No azure (8) pixels in row 0, but azure (8) pixels exist in the first column (col 0).
        mode: horizontal_blocks
        elements:
          - role: trigger
            color: azure (8)
            location: first column (col 0) at row `r`
            action: initiates drawing of three horizontal blocks
          - role: drawn_object
            color: azure (8)
            shape: horizontal block, 4 pixels wide
            placement:
              - Starts at (r, 0)
              - Starts at (r-1, 4) if r-1 >= 0
              - Starts at (r-2, 8) if r-2 >= 0
          - role: background/preserved_pixels
            color: all input pixels
            action: are preserved unless overwritten by the drawn azure blocks
        transformation:
          - Initialize output grid as a copy of the input.
          - Find all rows `r` where `input[r, 0]` is azure (8).
          - For each such `r`, draw the three specified 4-pixel horizontal azure blocks in the output grid, checking row boundary conditions (r-1 >= 0, r-2 >= 0). These blocks overwrite existing content.
      - condition: Fallback (neither of the above conditions met).
        transformation: Output grid is identical to the input grid. (Inferred, no examples provided).
    ```


*   **Natural Language Program:**
    1.  Examine the input grid. Check if any azure (8) pixels are present in the first row (row 0).
    2.  **If azure pixels are in the first row:**
        a.  Initialize the output grid as a copy of the input grid.
        b.  Determine the set of column indices containing azure pixels in the first row. This is the initial `current_pattern`.
        c.  Iterate through each row `r` from 0 to the grid height minus 1.
        d.  For the current row `r`, iterate through each column index `c` in the `current_pattern`. If the pixel at `input[r, c]` is white (0), set the corresponding pixel `output[r, c]` to azure (8).
        e.  Check if the input grid's row `r` contains any red (2) pixels.
        f.  If red pixels are present in row `r`, update the `current_pattern` for the *next* iteration (row `r+1`) by subtracting 1 from each column index and discarding any resulting negative indices. Otherwise, the `current_pattern` remains unchanged for the next row.
        g.  Proceed to the next row with the potentially updated `current_pattern`.
    3.  **If no azure pixels are in the first row:**
        a.  Check if any azure (8) pixels are present in the first column (column 0).
        b.  **If azure pixels are in the first column:**
            i.  Initialize the output grid as a copy of the input grid.
            ii. Find all row indices `r` such that `input[r, 0]` is azure (8).
            iii. For each such row index `r`:
                -   Draw a horizontal block of 4 azure pixels in the output grid from `(r, 0)` to `(r, 3)`.
                -   If `r-1` is a valid row index (>= 0), draw a horizontal block of 4 azure pixels from `(r-1, 4)` to `(r-1, 7)`.
                -   If `r-2` is a valid row index (>= 0), draw a horizontal block of 4 azure pixels from `(r-2, 8)` to `(r-2, 11)`.
                -   These drawing operations overwrite any previous content in those output grid cells.
        c.  **If no azure pixels are in the first column either:**
            i.  The output grid is identical to the input grid.
    4.  Return the final output grid.
```python
import numpy as np
import copy

"""
Transforms an input grid based on the positions of azure (8) and red (2) pixels, following one of two modes or a fallback:

1.  **Mode 1 (Vertical Shift):** Triggered if azure (8) pixels exist in the first row (row 0).
    *   An initial vertical pattern is defined by the columns of azure pixels in the first row.
    *   This pattern propagates downwards. For each row, white (0) pixels in the input grid at the pattern's columns are changed to azure (8) in the output grid.
    *   If a row in the *input* grid contains a red (2) pixel, the pattern for subsequent rows shifts one column to the left (negative indices are discarded).
    *   Non-white pixels from the input (like the red triggers) are preserved unless overwritten by the propagated pattern (which only happens if they were white initially).

2.  **Mode 2 (Horizontal Blocks):** Triggered if Mode 1 is not met and azure (8) pixels exist in the first column (col 0).
    *   Each azure pixel in the first column at row `r` triggers the drawing of three horizontal, 4-pixel-wide azure blocks in the output grid:
        *   Block 1: Starts at `(r, 0)`
        *   Block 2: Starts at `(r-1, 4)` (if `r-1 >= 0`)
        *   Block 3: Starts at `(r-2, 8)` (if `r-2 >= 0`)
    *   These blocks overwrite any existing content in the output grid at their locations. All other input pixels are preserved.

3.  **Fallback:** If neither Mode 1 nor Mode 2 conditions are met, the output grid is identical to the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid as a 2D list of integers.

    Returns:
        list[list[int]]: The transformed grid as a 2D list of integers.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)

    # --- Check conditions and apply transformations ---

    # Condition for Mode 1: Azure (8) in the first row (row 0)
    first_row = input_np[0, :]
    if 8 in first_row:
        # --- Mode 1: Vertical Shift ---
        
        # Find initial pattern columns from the first row
        current_pattern_cols = set(np.where(first_row == 8)[0])

        # Iterate through rows from top to bottom
        for r in range(rows):
            # Apply the current pattern to this row in the output grid
            # Only change pixels that were originally white (0)
            for c in current_pattern_cols:
                # Ensure column index is valid before accessing
                if 0 <= c < cols:
                    if input_np[r, c] == 0:
                        output_np[r, c] = 8
            
            # Check if the *input* grid's current row `r` contains any red (2) pixels
            # This determines the pattern for the *next* row
            if 2 in input_np[r, :]:
                # Update pattern for the next row by shifting all columns left by 1
                next_pattern_cols = set()
                for c in current_pattern_cols:
                    if c - 1 >= 0: # Discard resulting negative indices
                        next_pattern_cols.add(c - 1)
                # Update the pattern for the next iteration
                current_pattern_cols = next_pattern_cols 
                
        # Return the result for Mode 1
        return output_np.tolist() 

    # Condition for Mode 2: No azure in row 0, BUT azure (8) in the first column (col 0)
    # This check only happens if Mode 1 condition was false
    first_col = input_np[:, 0]
    if 8 in first_col:
        # --- Mode 2: Horizontal Blocks ---
        
        # Find all trigger row indices `r` where input[r, 0] is azure (8)
        trigger_rows = np.where(first_col == 8)[0]

        # For each trigger row, draw the three horizontal blocks
        for r in trigger_rows:
            # Draw Block 1: starts at (r, 0), length 4
            # Overwrites existing pixels in output_np
            for c_offset in range(4):
                 c = 0 + c_offset
                 if c < cols: # Check column boundary
                     output_np[r, c] = 8
                 
            # Draw Block 2: starts at (r-1, 4), length 4
            if r - 1 >= 0: # Check row boundary
                 for c_offset in range(4):
                     c = 4 + c_offset
                     if c < cols: # Check column boundary
                         output_np[r - 1, c] = 8

            # Draw Block 3: starts at (r-2, 8), length 4
            if r - 2 >= 0: # Check row boundary
                 for c_offset in range(4):
                     c = 8 + c_offset
                     if c < cols: # Check column boundary
                         output_np[r - 2, c] = 8

        # Return the result for Mode 2
        return output_np.tolist()

    # --- Fallback ---
    # If neither Mode 1 nor Mode 2 conditions were met,
    # return the initial copy of the input grid.
    return output_np.tolist()
```
