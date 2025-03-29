
Previous Code:
```python
import numpy as np

"""
Transforms an input grid containing sparse colored pixels into an output grid with horizontal zones and vertical borders defined by those pixels.

1.  Identify all non-white pixels in the input grid, recording their color and row index. If no non-white pixels are found, return an all-white grid of the same dimensions.
2.  Determine the unique rows containing non-white pixels and associate each unique row with the color found in that row. If multiple colors exist in the same row, use the color of the first encountered non-white pixel in that row during a top-to-bottom, left-to-right scan (though examples suggest consistency or irrelevance of column).
3.  Sort these unique rows in ascending order. Let the sorted unique rows be `R_1, R_2, ..., R_n` and their corresponding colors be `C_1, C_2, ..., C_n`.
4.  Create an output grid of the same dimensions as the input, initialized to white (0).
5.  Draw a solid horizontal line of color `C_1` (color associated with the topmost row `R_1`) across the full width of the output grid at row 0 (the very top row).
6.  Draw a solid horizontal line of color `C_n` (color associated with the bottommost row `R_n`) across the full width of the output grid at the last row (`height - 1`).
7.  For each unique row `R_i` (from `i=1` to `n`), draw a solid horizontal line of color `C_i` across the full width of the output grid at row `R_i`.
8.  Draw vertical lines in the leftmost column (column 0) and the rightmost column (last column) to connect the horizontal lines:
    *   Fill the vertical segment from row 1 up to (but not including) row `R_1` with color `C_1`. This applies only if `R_1 > 1`.
    *   For each pair of consecutive unique rows `R_i` and `R_{i+1}` (where `i` goes from 1 to `n-1`), fill the vertical segment from row `R_i + 1` up to (but not including) row `R_{i+1}` with color `C_{i+1}` (the color associated with the lower row `R_{i+1}`). This applies only if `R_{i+1} > R_i + 1`.
    *   Fill the vertical segment from row `R_n + 1` up to (but not including) the last row (`height - 1`) with color `C_n`. This applies only if `height - 1 > R_n + 1`.
9.  Return the completed output grid.
"""

def transform(input_grid):
    """
    Applies the zone-filling transformation based on non-white input pixels.

    Args:
        input_grid (list of lists): The input grid containing pixels 0-9.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize with white (0)

    # 1 & 2. Identify non-white pixels and unique rows with their colors
    row_colors = {}
    pixel_locations = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:
                pixel_locations.append((r, c, color))
                # Store the first color encountered for this row
                if r not in row_colors:
                    row_colors[r] = color

    # Handle case with no non-white pixels
    if not row_colors:
        return output_grid.tolist()

    # 3. Sort unique rows and get corresponding (row, color) pairs
    sorted_rows = sorted(row_colors.keys())
    sorted_pixel_data = [(r, row_colors[r]) for r in sorted_rows]

    # Get colors for top and bottom boundaries/segments
    first_color = sorted_pixel_data[0][1]
    last_color = sorted_pixel_data[-1][1]

    # 4. Initialize output grid (already done)

    # 5. Draw top boundary line
    output_grid[0, :] = first_color

    # 6. Draw bottom boundary line
    output_grid[height - 1, :] = last_color

    # 7. Draw horizontal lines for each identified pixel's row
    for r, c in sorted_pixel_data:
        output_grid[r, :] = c

    # 8. Draw vertical borders
    # Segment above the first pixel row
    first_row = sorted_pixel_data[0][0]
    if first_row > 0: # Ensure there's space between row 0 and first_row
        # Vertical lines go from row 1 up to (but not including) first_row
        if 1 < first_row:
            output_grid[1:first_row, 0] = first_color
            output_grid[1:first_row, width - 1] = first_color

    # Segments between consecutive pixel rows
    for i in range(len(sorted_pixel_data) - 1):
        current_row = sorted_pixel_data[i][0]
        next_row = sorted_pixel_data[i+1][0]
        next_color = sorted_pixel_data[i+1][1]

        start_vert_row = current_row + 1
        end_vert_row = next_row # Slice goes up to, but not including, end_vert_row

        if start_vert_row < end_vert_row: # Only draw if there's space
            output_grid[start_vert_row:end_vert_row, 0] = next_color
            output_grid[start_vert_row:end_vert_row, width - 1] = next_color

    # Segment below the last pixel row
    last_row = sorted_pixel_data[-1][0]
    start_vert_row_final = last_row + 1
    end_vert_row_final = height - 1 # Slice goes up to, but not including, end_vert_row_final

    if start_vert_row_final < end_vert_row_final: # Only draw if there's space
        output_grid[start_vert_row_final:end_vert_row_final, 0] = last_color
        output_grid[start_vert_row_final:end_vert_row_final, width - 1] = last_color

    # 9. Return the completed grid
    return output_grid.tolist()
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
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
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
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.111111111111114

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
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
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
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.111111111111114

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
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
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
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.333333333333314

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
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
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
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.111111111111114
The metrics confirm the previous analysis:
*   **Example 1:** Rows 4, 5 (between R=3(Red) and R=7(Orange)) should be Red(2) but are Orange(7). Rows 8, 9 (between R=7(Orange) and R=12(Azure)) should be Orange(7) but are Azure(8).
*   **Example 2:** Row 2 (between R=1(Azure) and R=3(Blue)) should be Azure(8) but is Blue(1). Rows 4, 5 (between R=3(Blue) and R=7(Red)) should be Blue(1) but are Red(2). Row 8 (between R=7(Red) and R=9(Green)) should be Red(2) but is Green(3).
*   **Example 3:** Rows 3, 4 (between R=2(Green) and R=7(Red)) should be Green(3) but are Red(2). Row 8 (between R=7(Red) and R=9(Maroon)) should be Red(2) but is Maroon(9).
*   **Example 4:** Row 3 (between R=2(Magenta) and R=4(Red)) should be Magenta(6) but is Red(2). Rows 5, 6, 7 (between R=4(Red) and R=11(Azure)) should be Red(2) but are Azure(8).

The errors consistently occur in the vertical segments (first and last columns) between the horizontal lines drawn at the rows containing input pixels. The expected color for a segment between row `R_i` and `R_{i+1}` is the color associated with `R_i`, while the code used the color associated with `R_{i+1}`.## General Assessment

The provided code correctly identifies the rows containing non-white pixels in the input grid and draws horizontal lines of the corresponding color across the output grid at these specific rows. It also correctly draws the top and bottom boundary lines using the colors from the uppermost and lowermost identified rows, respectively.

However, the code fails because it incorrectly determines the color for the vertical segments in the first and last columns *between* these horizontal lines. The code currently colors the segment between row `R_i` and `R_{i+1}` (where `R_i` and `R_{i+1}` are the rows of consecutive non-white pixels) using the color associated with the *lower* row (`R_{i+1}`). The analysis of the expected outputs reveals that these segments should instead be colored using the color associated with the *upper* row (`R_i`).

The strategy to resolve this is to modify step 8 of the transformation logic: when filling the vertical segments between two consecutive horizontal lines (at rows `R_i` and `R_{i+1}`), the color used should be `C_i` (the color associated with row `R_i`), not `C_{i+1}`.

## Metrics

Metrics gathered using `analyze_diff` confirm the location and nature of the errors across all failed examples:

*   **Example 1:** 8 pixels off. Errors occur in columns 0 and 14 at rows 4, 5, 8, 9. Expected colors [2, 2, 2, 2, 7, 7, 7, 7] vs. Actual [7, 7, 7, 7, 8, 8, 8, 8].
*   **Example 2:** 8 pixels off. Errors occur in columns 0 and 14 at rows 2, 4, 5, 8. Expected colors [8, 8, 1, 1, 1, 1, 2, 2] vs. Actual [1, 1, 2, 2, 2, 2, 3, 3].
*   **Example 3:** 6 pixels off. Errors occur in columns 0 and 14 at rows 3, 4, 8. Expected colors [3, 3, 3, 3, 2, 2] vs. Actual [2, 2, 2, 2, 9, 9].
*   **Example 4:** 8 pixels off. Errors occur in columns 0 and 14 at rows 3, 5, 6, 7. Expected colors [6, 6, 2, 2, 2, 2, 2, 2] vs. Actual [2, 2, 8, 8, 8, 8, 8, 8].

These metrics consistently show that the vertical segment between the horizontal line at `R_i` (color `C_i`) and the line at `R_{i+1}` (color `C_{i+1}`) is incorrectly colored with `C_{i+1}` instead of the expected `C_i`.

## YAML Documentation


```yaml
task_description: Transforms a grid with sparse colored pixels into a grid with colored horizontal zones defined by these pixels.
input_features:
  - name: grid
    type: 2D array of integers (0-9)
    description: Represents a grid where most pixels are white (0) and a few are colored.
  - name: colored_pixels
    type: list of (row, column, color) tuples
    description: Non-white pixels in the input grid. Their row indices and colors are significant. Column indices are irrelevant for determining the transformation rule.
  - name: unique_rows
    type: list of (row, color) tuples
    description: The unique rows containing colored pixels, paired with the color found in that row (first encountered if multiple). Sorted by row index. Let these be (R_1, C_1), (R_2, C_2), ..., (R_n, C_n).
output_features:
  - name: zoned_grid
    type: 2D array of integers (0-9)
    description: Grid of the same dimensions as the input, filled with colored horizontal zones and vertical borders.
    properties:
      - height: Same as input grid height.
      - width: Same as input grid width.
      - background: White (0) in the interior, away from borders and horizontal lines.
      - horizontal_lines:
          - location: At rows R_1, R_2, ..., R_n.
          - color: Full width line with color C_i at row R_i.
      - top_boundary:
          - location: Row 0.
          - color: Full width line with color C_1.
      - bottom_boundary:
          - location: Last row (height - 1).
          - color: Full width line with color C_n.
      - vertical_borders:
          - location: Column 0 and last column (width - 1).
          - segments:
            - From row 1 to R_1 - 1: Color C_1.
            - From row R_i + 1 to R_{i+1} - 1: Color C_i (for i = 1 to n-1).
            - From row R_n + 1 to height - 2: Color C_n.
transformation:
  actions:
    - Find all non-white pixels in the input grid.
    - Identify the unique rows containing these pixels and associate each row with its color.
    - Sort these unique rows R_1, ..., R_n with corresponding colors C_1, ..., C_n.
    - Initialize an output grid of the same size with white (0).
    - Draw horizontal lines:
        - Draw line at row 0 with color C_1.
        - Draw line at row R_i with color C_i for all i from 1 to n.
        - Draw line at the last row with color C_n.
    - Draw vertical borders (columns 0 and width-1):
        - Fill rows 1 to R_1 - 1 with color C_1.
        - Fill rows R_i + 1 to R_{i+1} - 1 with color C_i (for i = 1 to n-1).
        - Fill rows R_n + 1 to height - 2 with color C_n.
  edge_cases:
    - If no non-white pixels are found in the input, return an all-white grid.
```


## Natural Language Program

1.  **Identify Key Rows and Colors**: Scan the input grid to find all non-white pixels. Record the row index and color of each. If there are no non-white pixels, return an all-white grid of the same dimensions as the input.
2.  **Determine Unique Row Data**: Create a list of unique row indices that contain non-white pixels. For each unique row, associate it with the color of the first non-white pixel encountered in that row (scanning left-to-right, top-to-bottom).
3.  **Sort Row Data**: Sort these unique rows in ascending order based on their row index. Let the sorted unique rows be `R_1, R_2, ..., R_n` and their corresponding colors be `C_1, C_2, ..., C_n`.
4.  **Initialize Output Grid**: Create a new grid with the same dimensions as the input grid, filled entirely with white (0).
5.  **Draw Horizontal Lines**:
    *   Fill the entire first row (row 0) of the output grid with color `C_1`.
    *   Fill the entire last row (row `height - 1`) of the output grid with color `C_n`.
    *   For each unique row `R_i` (from `i=1` to `n`), fill the entire row `R_i` of the output grid with color `C_i`.
6.  **Draw Vertical Borders**: Fill the pixels in the first column (column 0) and the last column (column `width - 1`) as follows:
    *   Fill the vertical segment from row 1 up to (but not including) row `R_1` with color `C_1`. This applies only if `R_1 > 1`.
    *   For each pair of consecutive unique rows `R_i` and `R_{i+1}` (where `i` goes from 1 to `n-1`), fill the vertical segment from row `R_i + 1` up to (but not including) row `R_{i+1}` with color `C_i` (the color associated with the *upper* row `R_i`). This applies only if `R_{i+1} > R_i + 1`.
    *   Fill the vertical segment from row `R_n + 1` up to (but not including) the last row (`height - 1`) with color `C_n`. This applies only if `height - 1 > R_n + 1`.
7.  **Return Output**: Return the completed output grid.
