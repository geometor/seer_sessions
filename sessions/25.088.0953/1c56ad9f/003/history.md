
Previous Code:
```python
import numpy as np

"""
Transforms the input grid by applying a row-dependent horizontal shift to the pixels of the single non-white object.

1.  Create a new output grid of the same dimensions as the input, filled with white (0).
2.  Identify all non-white pixels in the input grid, which constitute the single object.
3.  Find the row index of the topmost pixel of this object (`object_top_row`).
4.  For each non-white pixel at input coordinates (row, col) with color `c`:
    a.  Calculate its relative row index: `relative_row = row - object_top_row`.
    b.  Determine the horizontal shift based on `relative_row % 4`:
        - shift 0 if `relative_row % 4` is 0 or 2.
        - shift -1 (left) if `relative_row % 4` is 1.
        - shift +1 (right) if `relative_row % 4` is 3.
    c.  Calculate the target column: `new_col = col + shift`.
    d.  If `new_col` is within the grid's horizontal boundaries, set the pixel at (row, new_col) in the output grid to the object's color `c`.
5.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a row-dependent horizontal shift to the non-white object in the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to a NumPy array for efficient operations
    inp = np.array(input_grid, dtype=int)
    height, width = inp.shape

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(inp)

    # Find the coordinates of all non-white pixels (the object)
    object_pixels_r, object_pixels_c = np.where(inp > 0)

    # If there's no object, return the empty grid
    if object_pixels_r.size == 0:
        return output_grid.tolist()

    # Find the topmost row of the object
    object_top_row = np.min(object_pixels_r)

    # Iterate through each pixel of the object
    for r, c in zip(object_pixels_r, object_pixels_c):
        # Get the color of the current pixel
        color = inp[r, c]

        # Calculate the row index relative to the object's top
        relative_row = r - object_top_row

        # Determine the shift amount based on the relative row index modulo 4
        shift_index = relative_row % 4
        if shift_index == 1:
            shift_amount = -1  # Shift left
        elif shift_index == 3:
            shift_amount = 1   # Shift right
        else:  # shift_index is 0 or 2
            shift_amount = 0   # No shift

        # Calculate the new column position
        new_c = c + shift_amount

        # Check if the new column is within the grid boundaries
        if 0 <= new_c < width:
            # Place the pixel's color at the new position in the output grid
            output_grid[r, new_c] = color

    # Convert the NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0
0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 5 5 0 0 5 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 5 0 0 5 5 0 0 5 0 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 5 0 0 5 5 0 0 5 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 5 0 0 5 5 0 0 5 0 0 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 5 0 0 5 5 0 0 5 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 5 5 0 0 5 0 0
0 0 0 0 5 0 0 5 5 0 0 5 0 0 0
0 0 0 5 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 44
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 19.555555555555557

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 64
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 28.444444444444457
**General Assessment**

The previous code correctly identified the core transformation mechanism: applying a horizontal shift to each row of the single non-white object based on its relative row index (`relative_row`) within the object. The code implemented a specific repeating shift pattern `[0, -1, 0, 1]` based on `relative_row % 4`, which successfully solved Examples 1 and 2.

However, this fixed pattern failed for Examples 3 and 4, indicating that the specific sequence of shifts is not constant but varies between examples. Analysis reveals that the shift pattern is determined by the *color* of the object. The previous code needs to be updated to select the correct shift pattern based on the object's color before applying the shifts row by row.

**Metrics and Analysis**

Let's analyze the shift patterns for each example:

*   **Example 1:**
    *   Input Object Color: Green (3)
    *   Object Top Row: 4
    *   Observed Shifts (relative\_row % 4 = 0, 1, 2, 3): `[0, -1, 0, +1]`
    *   Code Result: Match

*   **Example 2:**
    *   Input Object Color: Red (2)
    *   Object Top Row: 3
    *   Observed Shifts (relative\_row % 4 = 0, 1, 2, 3): `[0, -1, 0, +1]`
    *   Code Result: Match

*   **Example 3:**
    *   Input Object Color: Gray (5)
    *   Object Top Row: 2
    *   Observed Shifts (relative\_row % 4 = 0, 1, 2, 3): `[-1, 0, +1, 0]`
    *   Code Result: Mismatch (Applied `[0, -1, 0, +1]`)

*   **Example 4:**
    *   Input Object Color: Azure (8)
    *   Object Top Row: 2
    *   Observed Shifts (relative\_row % 4 = 0, 1, 2, 3): `[+1, 0, -1, 0]`
    *   Code Result: Mismatch (Applied `[0, -1, 0, +1]`)

**Summary of Color-Dependent Shift Patterns:**

*   Red (2): `[0, -1, 0, 1]`
*   Green (3): `[0, -1, 0, 1]`
*   Gray (5): `[-1, 0, 1, 0]`
*   Azure (8): `[1, 0, -1, 0]`

The core logic remains the same: identify the object, find its top row, and iterate through its pixels. The key change is that the shift amount for a pixel at `(r, c)` depends not only on `(r - object_top_row) % 4` but also on the object's color.

**Facts**


```yaml
task_description: Apply a horizontal shift to each row of the single non-white object. The specific shift sequence depends on the object's color.

grid_properties:
  - background_color: white (0)
  - dimensions_preserved: true

object_properties:
  - type: single contiguous block of non-white pixels
  - color_preservation: color of the object remains unchanged
  - shape_preservation: shape is distorted horizontally by row shifts, but vertical structure is maintained.

transformation:
  - name: row_wise_horizontal_shift
  - steps:
      1: Identify the single non-white object and its color (`object_color`).
      2: Determine the row index of the topmost pixel of the object (`object_top_row`).
      3: Select the appropriate 4-element shift pattern based on `object_color`:
          - Red (2) or Green (3): `[0, -1, 0, 1]` (No shift, Left, No shift, Right)
          - Gray (5): `[-1, 0, 1, 0]` (Left, No shift, Right, No shift)
          - Azure (8): `[1, 0, -1, 0]` (Right, No shift, Left, No shift)
      4: Create an empty output grid of the same dimensions as the input, filled with white (0).
      5: For each non-white pixel `p` at input coordinates `(r, c)`:
          a: Calculate its relative row index: `relative_row = r - object_top_row`.
          b: Determine the index into the shift pattern: `shift_index = relative_row % 4`.
          c: Get the horizontal shift amount from the selected pattern: `shift_amount = pattern[shift_index]`.
          d: Calculate the target column: `new_c = c + shift_amount`.
          e: If `new_c` is within the grid's width boundaries:
             - Set the pixel at `(r, new_c)` in the output grid to the `object_color`.
      6: Return the output grid.
```


**Natural Language Program**

1.  Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Identify the single contiguous block of non-white pixels (the object) in the input grid. Determine its color (`object_color`). If no object exists, return the empty output grid.
3.  Find the row index of the topmost pixel of the object (`object_top_row`).
4.  Define a mapping from the object's color to a specific 4-element sequence of horizontal shifts:
    *   If `object_color` is Red (2) or Green (3), the shift sequence is `[0, -1, 0, 1]`.
    *   If `object_color` is Gray (5), the shift sequence is `[-1, 0, 1, 0]`.
    *   If `object_color` is Azure (8), the shift sequence is `[1, 0, -1, 0]`.
5.  Iterate through each non-white pixel `p` of the object, located at input coordinates `(row, col)`.
6.  For each pixel `p`:
    a.  Calculate its row index relative to the object's top: `relative_row = row - object_top_row`.
    b.  Determine the index within the shift sequence using the modulo operator: `shift_index = relative_row % 4`.
    c.  Retrieve the corresponding horizontal shift amount from the sequence selected in step 4: `shift_amount = sequence[shift_index]`.
    d.  Calculate the new column coordinate for the pixel: `new_col = col + shift_amount`.
    e.  Check if `new_col` is a valid column index within the grid's width.
    f.  If `new_col` is valid, place the pixel's original color (`object_color`) at coordinates `(row, new_col)` in the output grid.
7.  Return the completed output grid.
