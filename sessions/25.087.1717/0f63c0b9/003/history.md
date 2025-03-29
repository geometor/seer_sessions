
Previous Code:
```python
import numpy as np

"""
Transforms an input grid containing sparse colored pixels into an output grid with horizontal zones defined by those pixels.

1. Identify all non-white pixels in the input grid, recording their color and row index.
2. Sort these pixels based on their row index (top to bottom).
3. Initialize an output grid of the same dimensions as the input, filled with white (0).
4. Iterate through the sorted pixels. For each pixel (color C, row R):
    a. Draw a solid horizontal line of color C across the full width at row R in the output grid.
    b. Determine the starting row for the vertical borders. This is the row immediately after the previous pixel's row (or row 0 if it's the first pixel).
    c. Draw vertical lines of color C in the leftmost (column 0) and rightmost (last column) columns, from the starting row up to (but not including) row R.
5. After processing all pixels, identify the color (C_last) and row (R_last) of the last (lowest) pixel.
6. Draw vertical lines of color C_last in the leftmost and rightmost columns from row R_last + 1 up to (but not including) the final row.
7. Draw a solid horizontal line of color C_last across the full width at the very last row of the output grid.
"""

def transform(input_grid):
    """
    Applies the described zone-filling transformation to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid containing pixels 0-9.

    Returns:
        np.array: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize with background color 0 (white)

    # 1. Identify all non-white pixels
    pixels = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:
                pixels.append({'color': color, 'row': r, 'col': c})

    # Handle case with no non-white pixels (return empty grid)
    if not pixels:
        return output_grid

    # 2. Sort pixels by row index
    sorted_pixels = sorted(pixels, key=lambda p: p['row'])

    # 3. Initialize output grid (already done)

    # 4. Iterate through sorted pixels and draw zones
    previous_row = -1
    for pixel in sorted_pixels:
        color = pixel['color']
        row = pixel['row']

        # a. Draw solid horizontal line
        output_grid[row, :] = color

        # b. Determine start row for vertical borders
        start_row_borders = previous_row + 1

        # c. Draw vertical borders
        # Ensure start index is not greater than end index before slicing
        if start_row_borders < row:
            output_grid[start_row_borders:row, 0] = color  # Left border
            output_grid[start_row_borders:row, width - 1] = color # Right border

        # Update previous_row for the next iteration
        previous_row = row

    # 5. Get info for the last pixel
    last_pixel = sorted_pixels[-1]
    last_color = last_pixel['color']
    last_row = last_pixel['row']

    # 6. Draw remaining vertical borders below the last pixel's row
    start_row_final_borders = last_row + 1
    # Ensure start index is not greater than end index before slicing
    if start_row_final_borders < height - 1:
         output_grid[start_row_final_borders:height - 1, 0] = last_color # Left border
         output_grid[start_row_final_borders:height - 1, width - 1] = last_color # Right border

    # 7. Draw final solid horizontal line at the bottom
    output_grid[height - 1, :] = last_color

    return output_grid.tolist() # Return as list of lists per ARC standard
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
7 0 0 0 0 0 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 0 0 0 0 0 7
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
7 0 0 0 0 0 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.666666666666686

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 1
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.666666666666686

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
```
Transformed Output:
```
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 0 0 0 0 0 0 0 0 0 0 0 0 0 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
```
Match: False
Pixels Off: 19
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.888888888888886

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 0 0 0 0 0 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 0 0 0 0 0 6
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
6 0 0 0 0 0 0 0 0 0 0 0 0 0 6
6 0 0 0 0 0 0 0 0 0 0 0 0 0 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
2 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.666666666666686
## General Assessment

The provided code attempts to implement a transformation where non-white pixels in the input define horizontal zones in the output. The core logic correctly identifies these key pixels, sorts them by row, and draws horizontal lines at these rows. It also attempts to draw vertical lines connecting these horizontal segments at the grid's left and right edges.

However, the comparison between the `Transformed Output` and `Expected Output` reveals consistent errors across all examples:

1.  **Missing Top Boundary Line:** The expected output always has a solid horizontal line at the very top row (row 0) matching the color of the *highest* non-white pixel in the input. The current code doesn't create this line.
2.  **Missing Bottom Boundary Line:** Similarly, the expected output always has a solid horizontal line at the very bottom row (last row) matching the color of the *lowest* non-white pixel. The current code doesn't create this line correctly.
3.  **Incorrect Vertical Line Colors:** The vertical lines connecting two horizontal lines (at rows `R_i` and `R_{i+1}`) should take the color of the *lower* horizontal line (at `R_{i+1}`), not the upper one as implemented in the current code. The vertical lines *above* the topmost pixel's line should take the color of that topmost pixel. The vertical lines *below* the bottommost pixel's line should take the color of that bottommost pixel.

The strategy is to adjust the natural language program and subsequent code to explicitly handle the top and bottom boundary lines and correct the logic for determining the color of the vertical segments between horizontal lines.

## Metrics

Let's analyze the input pixels and the structure for each example:

**Example 1:**
- Input Pixels: Red (2) at row 3, Orange (7) at row 7, Azure (8) at row 12.
- Height: 15, Width: 15
- Expected Zones (Top to Bottom):
    - Row 0: Red (Top boundary)
    - Rows 1-2: Red vertical borders
    - Row 3: Red horizontal line
    - Rows 4-6: Orange vertical borders (Color from row 7 line)
    - Row 7: Orange horizontal line
    - Rows 8-11: Azure vertical borders (Color from row 12 line)
    - Row 12: Azure horizontal line
    - Row 13: Azure vertical borders
    - Row 14: Azure (Bottom boundary)
- Code Errors: Missing row 0 (Red), wrong vertical colors (Red instead of Orange, Orange instead of Azure), missing row 14 (Azure), incorrect vertical extent below row 12.

**Example 2:**
- Input Pixels: Azure (8) at row 1, Blue (1) at row 3, Red (2) at row 7, Green (3) at row 9.
- Height: 15, Width: 15
- Expected Zones (Top to Bottom):
    - Row 0: Azure (Top boundary)
    - Row 1: Azure horizontal line (No vertical segment above as R1=1)
    - Row 2: Blue vertical borders (Color from row 3 line)
    - Row 3: Blue horizontal line
    - Rows 4-6: Red vertical borders (Color from row 7 line)
    - Row 7: Red horizontal line
    - Row 8: Green vertical borders (Color from row 9 line)
    - Row 9: Green horizontal line
    - Rows 10-13: Green vertical borders
    - Row 14: Green (Bottom boundary)
- Code Errors: Missing row 0 (Azure), wrong vertical colors (Azure instead of Blue, Blue instead of Red, Red instead of Green), missing row 14 (Green), incorrect vertical extent below row 9.

**Example 3:**
- Input Pixels: Green (3) at row 2, Red (2) at row 7, Maroon (9) at row 9.
- Height: 15, Width: 15
- Expected Zones (Top to Bottom):
    - Row 0: Green (Top boundary)
    - Row 1: Green vertical borders
    - Row 2: Green horizontal line
    - Rows 3-6: Red vertical borders (Color from row 7 line)
    - Row 7: Red horizontal line
    - Row 8: Maroon vertical borders (Color from row 9 line)
    - Row 9: Maroon horizontal line
    - Rows 10-13: Maroon vertical borders
    - Row 14: Maroon (Bottom boundary)
- Code Errors: Missing row 0 (Green), wrong vertical colors (Green instead of Red, Red instead of Maroon), missing row 14 (Maroon), incorrect vertical extent below row 9.

**Example 4:**
- Input Pixels: Magenta (6) at row 2, Red (2) at row 4, Azure (8) at row 11.
- Height: 15, Width: 15
- Expected Zones (Top to Bottom):
    - Row 0: Magenta (Top boundary)
    - Row 1: Magenta vertical borders
    - Row 2: Magenta horizontal line
    - Row 3: Red vertical borders (Color from row 4 line)
    - Row 4: Red horizontal line
    - Rows 5-10: Azure vertical borders (Color from row 11 line)
    - Row 11: Azure horizontal line
    - Rows 12-13: Azure vertical borders
    - Row 14: Azure (Bottom boundary)
- Code Errors: Missing row 0 (Magenta), wrong vertical colors (Magenta instead of Red, Red instead of Azure), missing row 14 (Azure), incorrect vertical extent below row 11.

The pattern of errors is consistent across all examples, confirming the assessment.

## YAML Facts


```yaml
task_description: Create horizontal zones based on the row and color of non-white pixels in the input.
grid_properties:
  - dimensions: Input and output grids have the same height and width.
  - background_color: White (0) is the background color for empty areas between vertical borders.
input_elements:
  - object: Non-white pixel
    properties:
      - color: The specific color (1-9) of the pixel.
      - row_index: The row where the pixel is located.
      - column_index: The column where the pixel is located (Note: column seems irrelevant for the transformation rule).
    constraints:
      - There can be multiple non-white pixels.
      - Pixels can share the same row (though not observed in examples, the logic should handle it, likely using the first encountered per row if sorted by column too, or just using the row index).
      - If no non-white pixels exist, the output is all white (implicitly handled by initialization).
transformation:
  - action: Identify and sort non-white pixels
    source: Input grid
    criteria: Pixels with color != 0.
    sorting: Primarily by row index (ascending). Let the sorted pixels be P_1, P_2, ..., P_n with colors C_1, ..., C_n and rows R_1, ..., R_n.
  - action: Initialize output grid
    target: Output grid
    properties: Same dimensions as input, filled with white (0).
  - action: Draw top boundary line
    target: Output grid
    location: Row 0, full width.
    color: C_1 (color of the highest pixel P_1).
  - action: Draw horizontal lines
    target: Output grid
    for_each: Sorted pixel P_i (from i=1 to n)
    location: Row R_i, full width.
    color: C_i.
  - action: Draw vertical border segments
    target: Output grid
    location: Column 0 and the last column.
    segments:
      - segment: Above first pixel line (P_1)
        rows: From 1 up to (but not including) R_1.
        color: C_1.
        condition: Only if R_1 > 1.
      - segment: Between pixel lines (P_i and P_{i+1})
        rows: From R_i + 1 up to (but not including) R_{i+1}.
        color: C_{i+1} (color of the lower horizontal line).
        condition: Only if R_{i+1} > R_i + 1.
        iteration: For i from 1 to n-1.
      - segment: Below last pixel line (P_n)
        rows: From R_n + 1 up to (but not including) the last row (height - 1).
        color: C_n.
        condition: Only if (height - 1) > R_n + 1.
  - action: Draw bottom boundary line
    target: Output grid
    location: Last row (height - 1), full width.
    color: C_n (color of the lowest pixel P_n).
output_structure:
  - The output consists of horizontal colored stripes connected by vertical colored stripes at the left and right edges.
  - The horizontal stripes are located at the rows corresponding to input non-white pixels, plus the top and bottom boundaries.
  - The color of a vertical segment between two horizontal stripes is determined by the color of the lower stripe.
  - The color of the top boundary and the vertical segment just below it matches the highest input pixel's color.
  - The color of the bottom boundary and the vertical segment just above it matches the lowest input pixel's color.

```


## Natural Language Program

1.  Identify all non-white pixels in the input grid, recording their color and row index. If no non-white pixels are found, return an all-white grid of the same dimensions.
2.  Sort these pixels based primarily on their row index (top to bottom). If multiple pixels share the same row, their relative order doesn't matter for this specific transformation. Let the sorted unique rows be `R_1, R_2, ..., R_n` and their corresponding colors be `C_1, C_2, ..., C_n` (using the color of any pixel found at that row, assuming consistency or taking the first encountered).
3.  Create an output grid of the same dimensions as the input, initialized to white (0).
4.  Draw a solid horizontal line of color `C_1` (color associated with the topmost row `R_1`) across the full width of the output grid at **row 0**.
5.  Draw a solid horizontal line of color `C_n` (color associated with the bottommost row `R_n`) across the full width of the output grid at the **last row** (`height - 1`).
6.  For each unique row `R_i` (from `i=1` to `n`) identified in step 2, draw a solid horizontal line of color `C_i` across the full width of the output grid at row `R_i`.
7.  Draw vertical lines in the leftmost column (column 0) and the rightmost column (last column) to connect the horizontal lines:
    *   Fill the vertical segment from row 1 up to (but not including) row `R_1` with color `C_1`.
    *   For each pair of consecutive unique rows `R_i` and `R_{i+1}` (where `i` goes from 1 to `n-1`), fill the vertical segment from row `R_i + 1` up to (but not including) row `R_{i+1}` with color `C_{i+1}` (the color associated with the lower row `R_{i+1}`).
    *   Fill the vertical segment from row `R_n + 1` up to (but not including) the last row (`height - 1`) with color `C_n`.
8.  Return the completed output grid.
