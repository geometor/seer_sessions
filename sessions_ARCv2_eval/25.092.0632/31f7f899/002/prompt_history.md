
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8
8 8 8 8 8 8 7
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 8 8 8 8 7
8 8 8 8 8 8 8
```

Okay, let's analyze the provided examples for this task.

### Perception

1.  **Grid Structure:** The input and output are grids of varying sizes (13x13, 15x15, 7x7).
2.  **Background Color:** The dominant color in all grids is azure (8), acting as a background.
3.  **Separator Line:** A distinct, single horizontal line of magenta (6) pixels is present in all input grids. This line remains unchanged in the output grids.
4.  **Other Objects/Pixels:** Various other colored pixels (gray 5, red 2, orange 7, blue 1, yellow 4, maroon 9) exist in the input grids, typically located above or below the magenta line.
5.  **Transformation:** The core transformation involves a vertical "filling" or "propagation" effect within each column. Colors other than the background (azure 8) and the separator (magenta 6) seem to spread vertically towards the magenta line.
6.  **Propagation Details:**
    *   The propagation occurs independently in each column.
    *   Colors spread both upwards (from below the magenta line towards it) and downwards (from above the magenta line towards it).
    *   The propagation replaces only the background (azure 8) pixels. Existing non-background, non-separator pixels remain unless overwritten by a *propagating* color in that column section.
    *   The color that propagates in a given direction (up or down) within a column is determined by the non-background, non-separator pixel closest to the magenta line in that direction.
    *   The magenta line itself acts as a barrier, stopping the propagation.

### Facts


```yaml
Grid Properties:
  - Background Color: azure (8)
  - Grid Size: Variable (e.g., 13x13, 15x15, 7x7)

Objects:
  - Type: Separator Line
    Properties:
      - Color: magenta (6)
      - Orientation: Horizontal
      - Thickness: 1 pixel
      - Role: Acts as a barrier to vertical propagation. Remains unchanged in the output.
  - Type: Propagating Pixels
    Properties:
      - Color: Any color except azure (8) and magenta (6).
      - Location: Can be anywhere except on the separator line itself.
      - Role: Source of color for vertical propagation within their column.
  - Type: Background Pixels
    Properties:
      - Color: azure (8)
      - Role: Can be replaced by propagating colors.

Relationships & Actions:
  - Action: Vertical Color Propagation
    Actor: Propagating Pixels
    Target: Background Pixels (azure 8)
    Constraint: Occurs within the same column as the source pixel.
    Direction:
      - Towards the separator line from above.
      - Towards the separator line from below.
    Rule:
      - For each column, find the non-background, non-separator pixel closest to the separator line from above. Propagate this color downwards, replacing background pixels, until the row just above the separator line.
      - For each column, find the non-background, non-separator pixel closest to the separator line from below. Propagate this color upwards, replacing background pixels, until the row just below the separator line.
    Boundary: Propagation stops at the separator line.
```


### Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the background color, which is azure (8).
3.  Identify the separator color, which is magenta (6).
4.  Locate the row index (`separator_row`) of the horizontal magenta (6) line.
5.  Iterate through each column index (`col`) of the grid.
6.  **Process Above Separator:**
    a.  Scan downwards from `row = separator_row - 1` to `row = 0`.
    b.  Find the first pixel `(row, col)` whose color is neither the background color (8) nor the separator color (6). Let this color be `color_above` and its row index be `source_row_above`.
    c.  If such a `color_above` is found:
        i. Iterate from `r = source_row_above` up to `separator_row - 1`.
        ii. If the pixel `(r, col)` in the *output* grid currently has the background color (8), change its color to `color_above`.
7.  **Process Below Separator:**
    a.  Scan upwards from `row = separator_row + 1` to the last row of the grid.
    b.  Find the first pixel `(row, col)` whose color is neither the background color (8) nor the separator color (6). Let this color be `color_below` and its row index be `source_row_below`.
    c.  If such a `color_below` is found:
        i. Iterate from `r = source_row_below` down to `separator_row + 1`.
        ii. If the pixel `(r, col)` in the *output* grid currently has the background color (8), change its color to `color_below`.
8.  Return the modified output grid. (The separator row remains unchanged as it was copied initially and is never targeted for modification).
```python
import numpy as np
import copy

"""
Transforms the input grid based on vertical color propagation towards a horizontal separator line.

1. Identifies the background color (azure, 8) and the separator color (magenta, 6).
2. Locates the row index of the horizontal magenta (6) separator line.
3. Iterates through each column of the grid.
4. For each column:
    a. Finds the non-background, non-separator color closest to the separator line from above. If found, propagates this color downwards, replacing background pixels, until the row just above the separator line.
    b. Finds the non-background, non-separator color closest to the separator line from below. If found, propagates this color upwards, replacing background pixels, until the row just below the separator line.
5. The separator line itself remains unchanged.
"""

def transform(input_grid):
    """
    Applies the vertical color propagation transformation.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Define known colors
    background_color = 8
    separator_color = 6

    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)
    height, width = output_grid.shape

    # Find the separator row
    separator_row = -1
    for r in range(height):
        if np.all(input_grid[r, :] == separator_color) or separator_color in input_grid[r, :]: # Check if the whole row or part of the row contains the separator color
             # More robust check: find the first row containing the separator color
             rows_with_separator = np.where(np.any(input_grid == separator_color, axis=1))[0]
             if len(rows_with_separator) > 0:
                 separator_row = rows_with_separator[0] # Assume the first occurrence is the separator line
                 break
    
    if separator_row == -1:
        # Handle cases where no separator is found (e.g., return input?)
        # For this specific task based on examples, a separator is always expected.
        # If not found, it might indicate an issue or an edge case not covered.
        # Let's assume it's always present based on training data.
        print("Warning: Separator row not found. Returning original grid.")
        return input_grid


    # Iterate through each column
    for c in range(width):
        # --- Process Above Separator ---
        color_above = None
        source_row_above = -1
        # Scan downwards from just above the separator to the top
        for r in range(separator_row - 1, -1, -1):
            pixel_color = input_grid[r, c]
            if pixel_color != background_color and pixel_color != separator_color:
                color_above = pixel_color
                source_row_above = r
                break # Found the closest color source above

        # If a color source was found above, propagate it downwards
        if color_above is not None:
            # Iterate from the source row up to (but not including) the separator row
            # In the original description, it says propagate *downwards*. Let's adjust.
            # Propagate from the found source row towards the separator
            # It should fill the background pixels between the source and the separator
            for r_fill in range(source_row_above + 1, separator_row):
                 if output_grid[r_fill, c] == background_color:
                     output_grid[r_fill, c] = color_above
            # Correction: The natural language said "Iterate from r = source_row_above up to separator_row - 1".
            # Let's re-read: "Propagate this color downwards, replacing background pixels, until the row just above the separator line."
            # This means fill from source_row_above + 1 to separator_row - 1.
            # Let's rethink the loop based on the *output* examples.
            # Example 1, col 1: gray(5) at (2,1) propagates down to row 5.
            # Example 1, col 6: red(2) at (3,6) propagates down to row 5.
            # Example 1, col 8: blue(1) at (5,8) propagates down to row 5.
            # It seems the color *below* the source gets filled.
            # Let's try filling from source_row_above + 1 to separator_row - 1
            for r_fill in range(source_row_above + 1, separator_row):
                 if output_grid[r_fill, c] == background_color:
                     output_grid[r_fill, c] = color_above


        # --- Process Below Separator ---
        color_below = None
        source_row_below = -1
        # Scan upwards from just below the separator to the bottom
        for r in range(separator_row + 1, height):
            pixel_color = input_grid[r, c]
            if pixel_color != background_color and pixel_color != separator_color:
                color_below = pixel_color
                source_row_below = r
                break # Found the closest color source below

        # If a color source was found below, propagate it upwards
        if color_below is not None:
            # Propagate upwards from the source row towards the separator
            # Fill background pixels between the source and the separator
            # Iterate from source_row_below - 1 down to separator_row + 1
            for r_fill in range(source_row_below - 1, separator_row, -1):
                 if output_grid[r_fill, c] == background_color:
                     output_grid[r_fill, c] = color_below

    return output_grid
```
