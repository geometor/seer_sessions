
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
2 7 2 7 2 7 2 7 2 7 2
5 7 5 7 5 7 5 7 5 8 5
7 8 7 7 7 7 7 7 7 8 7
7 8 7 7 7 8 7 7 7 8 7
7 8 7 7 7 8 7 8 7 1 7
7 1 7 8 7 8 7 8 7 1 7
7 1 7 8 7 1 7 8 7 1 7
7 1 7 8 7 1 7 1 7 1 7
7 1 7 1 7 1 7 1 7 1 7
```


**output:**
```
7 8 7 8 7 8 7 8 7 8 7
7 8 7 8 7 8 7 8 7 8 7
2 8 2 8 2 8 2 8 2 8 2
5 1 5 1 5 1 5 1 5 1 5
7 1 7 9 7 1 7 1 7 1 7
7 1 7 9 7 1 7 9 7 1 7
7 1 7 9 7 9 7 9 7 1 7
7 9 7 9 7 9 7 9 7 1 7
7 9 7 9 7 9 7 9 7 9 7
7 9 7 9 7 9 7 9 7 9 7
7 9 7 9 7 9 7 9 7 9 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
2 7 2 8 2 7 2 7 2
5 7 5 8 5 8 5 8 5
7 8 7 1 7 8 7 8 7
7 8 7 1 7 1 7 1 7
7 1 7 1 7 1 7 1 7
```


**output:**
```
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 8 7 8 7 8 7 8 7
2 8 2 8 2 8 2 8 2
5 1 5 1 5 1 5 1 5
7 9 7 1 7 1 7 1 7
7 9 7 1 7 9 7 9 7
7 9 7 9 7 9 7 9 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
2 7 2 7 2 7 2 7 2 8 2 7 2
5 7 5 8 5 7 5 7 5 8 5 7 5
7 8 7 8 7 7 7 7 7 8 7 8 7
7 8 7 8 7 8 7 8 7 1 7 8 7
7 8 7 1 7 8 7 8 7 1 7 8 7
7 1 7 1 7 8 7 1 7 1 7 1 7
7 1 7 1 7 1 7 1 7 1 7 1 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 8 7 8 7 8 7 8 7 8 7 8 7
7 8 7 8 7 8 7 8 7 8 7 8 7
2 8 2 8 2 8 2 8 2 8 2 8 2
5 1 5 1 5 1 5 1 5 1 5 1 5
7 1 7 1 7 9 7 1 7 1 7 1 7
7 9 7 1 7 9 7 9 7 1 7 9 7
7 9 7 9 7 9 7 9 7 1 7 9 7
7 9 7 9 7 9 7 9 7 9 7 9 7
7 9 7 9 7 9 7 9 7 9 7 9 7
```

*   **Perception of the Elements:**
    *   The input and output grids have the same dimensions.
    *   The grids consist primarily of orange (7) pixels, with patterns embedded within.
    *   There are distinct vertical stripes. The even-numbered columns (0, 2, 4, ...) contain various colors (red (2), gray (5), azure (8), blue (1), orange (7)), while the odd-numbered columns (1, 3, 5, ...) in the input consist entirely of orange (7) pixels.
    *   Two specific rows act as markers or delimiters: one row contains red (2) pixels in its even columns, and the row immediately below it contains gray (5) pixels in its even columns. Let's call these the "red marker row" and the "gray marker row".
    *   The transformation heavily depends on the column index (even or odd) and the row index relative to these two marker rows.
    *   The output grid modifies the colors in both even and odd columns based on these relative positions.
    *   **Odd columns:** The orange (7) pixels in the odd columns are replaced by azure (8) in rows up to and including the red marker row, by blue (1) in the gray marker row, and by maroon (9) in all rows below the gray marker row.
    *   **Even columns:** The pixels in the even columns are mostly unchanged, except:
        *   In the gray marker row, any azure (8) pixel becomes blue (1).
        *   In rows below the gray marker row, any azure (8) or blue (1) pixel becomes maroon (9).
        *   Other colors (red (2), gray (5), orange (7)) in even columns remain unchanged.

*   **YAML Facts:**
    
```yaml
    grid_properties:
      - dimensions_preserved: True
      - background_color: 7 # orange, predominantly in odd columns initially

    objects:
      - type: marker_row
        color: 2 # red
        location: Found in even columns of a specific row (red_marker_row).
      - type: marker_row
        color: 5 # gray
        location: Found in even columns of the row immediately below red_marker_row (gray_marker_row).
      - type: column_type
        property: parity
        values: [even, odd]

    relationships:
      - marker_rows: The gray_marker_row is always directly below the red_marker_row.
      - row_regions: The transformation logic depends on whether a row is above/at the red_marker_row, is the gray_marker_row, or is below the gray_marker_row.
      - column_parity_dependency: Transformation rules differ significantly for odd and even columns.

    actions:
      - name: find_marker_rows
        input: input_grid
        output: row indices for red_marker_row and gray_marker_row.
      - name: transform_odd_columns
        conditions:
          - based on row index relative to marker rows
        color_changes:
          - if row <= red_marker_row: 7 -> 8 (azure)
          - if row == gray_marker_row: 7 -> 1 (blue)
          - if row > gray_marker_row: 7 -> 9 (maroon)
      - name: transform_even_columns
        conditions:
          - based on row index relative to marker rows AND original pixel color
        color_changes:
          - if row == gray_marker_row and color == 8 (azure): 8 -> 1 (blue)
          - if row > gray_marker_row and (color == 8 (azure) or color == 1 (blue)): color -> 9 (maroon)
          - otherwise: color remains unchanged
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Scan the input grid to find the row index containing red (2) pixels; this is the `red_marker_row_index`.
    3.  Scan the input grid to find the row index containing gray (5) pixels; this is the `gray_marker_row_index`. (This will always be `red_marker_row_index + 1`).
    4.  Iterate through each cell of the grid using its row index `r` and column index `c`.
    5.  **If the column index `c` is odd:**
        *   If the row index `r` is less than or equal to `red_marker_row_index`, set the output grid cell `output[r][c]` to azure (8).
        *   If the row index `r` is equal to `gray_marker_row_index`, set the output grid cell `output[r][c]` to blue (1).
        *   If the row index `r` is greater than `gray_marker_row_index`, set the output grid cell `output[r][c]` to maroon (9).
    6.  **If the column index `c` is even:**
        *   Get the original color `original_color = input[r][c]`.
        *   If the row index `r` is equal to `gray_marker_row_index` AND `original_color` is azure (8), set the output grid cell `output[r][c]` to blue (1).
        *   If the row index `r` is greater than `gray_marker_row_index` AND (`original_color` is azure (8) OR `original_color` is blue (1)), set the output grid cell `output[r][c]` to maroon (9).
        *   Otherwise (for all other conditions in even columns), the output cell `output[r][c]` retains its `original_color` (copied initially).
    7.  Return the modified output grid.
```python
import numpy as np

"""
Transforms the input grid based on row position relative to two marker rows (identified by red '2' and gray '5' pixels) and column parity (even/odd).

1.  Find the row index of the 'red marker row' (contains red '2' in even columns).
2.  Find the row index of the 'gray marker row' (contains gray '5' in even columns, directly below the red marker row).
3.  Iterate through each cell (r, c) of the input grid.
4.  If the column 'c' is odd:
    - If row 'r' is at or above the red marker row, set the output cell to azure '8'.
    - If row 'r' is the gray marker row, set the output cell to blue '1'.
    - If row 'r' is below the gray marker row, set the output cell to maroon '9'.
5.  If the column 'c' is even:
    - If row 'r' is the gray marker row and the input cell is azure '8', set the output cell to blue '1'.
    - If row 'r' is below the gray marker row and the input cell is azure '8' or blue '1', set the output cell to maroon '9'.
    - Otherwise, keep the original input cell value.
"""

def find_marker_rows(grid):
    """
    Finds the row indices of the red (2) and gray (5) marker rows.
    Assumes marker colors appear in even columns of their respective rows.
    """
    red_marker_row_index = -1
    gray_marker_row_index = -1
    height, width = grid.shape

    for r in range(height):
        found_red = False
        found_gray = False
        for c in range(0, width, 2): # Check only even columns
            if grid[r, c] == 2:
                found_red = True
            if grid[r, c] == 5:
                found_gray = True
        
        if found_red:
            red_marker_row_index = r
        if found_gray:
            gray_marker_row_index = r
            
        # Optimization: if both are found, we can potentially stop early 
        # if we assume they are consecutive and unique.
        # Given the examples, gray is always directly below red.
        if red_marker_row_index != -1 and gray_marker_row_index != -1:
            # Verify gray is directly below red
            if gray_marker_row_index == red_marker_row_index + 1:
                 break 
            else: # Reset if assumption is broken (though unlikely based on examples)
                 red_marker_row_index = -1 
                 gray_marker_row_index = -1
                 
    # If only red was found, assume gray is below it
    if red_marker_row_index != -1 and gray_marker_row_index == -1 and red_marker_row_index + 1 < height:
        # Check if the row below red actually contains gray markers
        is_actual_gray_row = False
        for c in range(0, width, 2):
            if grid[red_marker_row_index + 1, c] == 5:
                is_actual_gray_row = True
                break
        if is_actual_gray_row:
            gray_marker_row_index = red_marker_row_index + 1


    if red_marker_row_index == -1 or gray_marker_row_index == -1:
        # Handle cases where markers might not be found as expected, 
        # although the examples guarantee their presence.
        # For robustness, one might raise an error or return default indices.
        print("Warning: Marker rows not found or not structured as expected.")
        # Fallback or error handling could go here. Let's assume they are always found per task structure.
        # Re-scan specifically for gray if red was found but gray wasn't below it
        if red_marker_row_index != -1 and gray_marker_row_index == -1:
             for r in range(height):
                 for c in range(0, width, 2):
                     if grid[r, c] == 5:
                         gray_marker_row_index = r
                         break
                 if gray_marker_row_index != -1:
                     break


    return red_marker_row_index, gray_marker_row_index


def transform(input_grid):
    """
    Applies the transformation rule based on marker rows and column parity.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Find the marker row indices
    red_marker_row_index, gray_marker_row_index = find_marker_rows(input_grid_np)

    # Check if marker rows were found successfully
    if red_marker_row_index == -1 or gray_marker_row_index == -1:
        print("Error: Could not find marker rows. Returning input grid.")
        return input_grid # Or raise an exception

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            original_color = input_grid_np[r, c]

            # Check if the column index 'c' is odd
            if c % 2 != 0:
                # Apply rules for odd columns based on row position relative to markers
                if r <= red_marker_row_index:
                    output_grid[r, c] = 8  # azure
                elif r == gray_marker_row_index:
                    output_grid[r, c] = 1  # blue
                elif r > gray_marker_row_index:
                    output_grid[r, c] = 9  # maroon
            
            # Check if the column index 'c' is even
            else: # c % 2 == 0
                # Apply rules for even columns based on row position and original color
                if r == gray_marker_row_index and original_color == 8: # Azure in gray marker row
                    output_grid[r, c] = 1 # blue
                elif r > gray_marker_row_index and (original_color == 8 or original_color == 1): # Azure or Blue below gray marker row
                    output_grid[r, c] = 9 # maroon
                # Otherwise (all other cases in even columns), the color remains unchanged (already copied)

    # Convert numpy array back to list of lists for the expected output format
    return output_grid.tolist()
```
