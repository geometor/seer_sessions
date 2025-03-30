
Previous Code:
```python
import numpy as np

"""
Identifies whether the input grid has horizontal (top/bottom) or vertical (left/right) single-pixel thick borders of uniform, non-white, distinct colors.
If borders are found, iterates through the grid looking for blue pixels (color 1).
For each blue pixel found, it checks its adjacent white pixels (color 0) that are within the non-border area.
If the borders are horizontal, a white pixel directly above a blue pixel is changed to the top border's color, and a white pixel directly below is changed to the bottom border's color.
If the borders are vertical, a white pixel directly to the left of a blue pixel is changed to the left border's color, and a white pixel directly to the right is changed to the right border's color.
The original blue pixels and the border pixels remain unchanged.
If no valid borders are identified, the original grid is returned.
"""

def is_uniform_and_non_white(arr):
    """Checks if a 1D numpy array is uniform (all elements same) and not color 0 (white)."""
    if arr.size == 0:
        return False, -1 # Cannot be uniform if empty
    first_val = arr[0]
    if first_val == 0: # Check if the color is white
        return False, -1
    # Check if all elements are the same as the first element
    is_uniform = np.all(arr == first_val)
    return is_uniform, first_val

def transform(input_grid):
    """
    Applies the border-based color transformation to white pixels adjacent to blue pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    border_type = None
    color1 = -1
    color2 = -1

    # Check for horizontal borders (top and bottom rows)
    # Ensure grid is tall enough for distinct top/bottom borders and content area
    if height >= 3:
        top_row = input_np[0, :]
        bottom_row = input_np[height - 1, :]
        top_uniform, top_color = is_uniform_and_non_white(top_row)
        bottom_uniform, bottom_color = is_uniform_and_non_white(bottom_row)

        # Check if both are uniform, non-white, and different from each other
        if top_uniform and bottom_uniform and top_color != bottom_color:
            border_type = 'horizontal'
            color1 = top_color  # color_top
            color2 = bottom_color # color_bottom

    # If horizontal borders not found or not valid, check for vertical borders
    # Ensure grid is wide enough for distinct left/right borders and content area
    if border_type is None and width >= 3:
        left_col = input_np[:, 0]
        right_col = input_np[:, width - 1]
        left_uniform, left_color = is_uniform_and_non_white(left_col)
        right_uniform, right_color = is_uniform_and_non_white(right_col)

        # Check if both are uniform, non-white, and different from each other
        if left_uniform and right_uniform and left_color != right_color:
            border_type = 'vertical'
            color1 = left_color # color_left
            color2 = right_color # color_right

    # If no valid borders found, return the original grid copy
    if border_type is None:
        return output_grid.tolist()

    # Apply transformations based on border type
    if border_type == 'horizontal':
        color_top = color1
        color_bottom = color2
        # Iterate through the inner grid (excluding borders)
        for r in range(1, height - 1):
            for c in range(width):
                # Find blue pixels (trigger pixels)
                if input_np[r, c] == 1:
                    # Check pixel above (must be within inner grid, i.e., r-1 >= 1)
                    if r - 1 >= 1 and input_np[r - 1, c] == 0:
                        output_grid[r - 1, c] = color_top
                    # Check pixel below (must be within inner grid, i.e., r+1 <= height-2)
                    if r + 1 <= height - 2 and input_np[r + 1, c] == 0:
                        output_grid[r + 1, c] = color_bottom

    elif border_type == 'vertical':
        color_left = color1
        color_right = color2
        # Iterate through the inner grid (excluding borders)
        for r in range(height):
             for c in range(1, width - 1):
                 # Find blue pixels (trigger pixels)
                if input_np[r, c] == 1:
                    # Check pixel left (must be within inner grid, i.e., c-1 >= 1)
                    if c - 1 >= 1 and input_np[r, c - 1] == 0:
                        output_grid[r, c - 1] = color_left
                    # Check pixel right (must be within inner grid, i.e., c+1 <= width-2)
                    if c + 1 <= width - 2 and input_np[r, c + 1] == 0:
                        output_grid[r, c + 1] = color_right

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 8 0 0 0 0 0 8 0 0 0 0
0 0 1 0 8 0 0 0 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 1
0 0 3 0 0 0 0 0 1 0 0 0 3
0 0 0 0 0 0 0 0 3 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 8 0 0 0 0 0 8 0 0 0 0
0 0 1 0 8 0 0 0 1 0 0 0 0
0 0 3 0 1 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0 0 3 0 0 0
0 0 8 0 0 3 0 0 0 0 0 0 8
0 0 1 0 0 0 0 0 8 0 0 0 1
0 0 3 0 0 0 0 0 1 0 0 0 3
0 0 0 0 0 0 0 0 3 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.256410256410277

## Example 2:
Input:
```
2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
2 2 2 2 2 2 2 2 2 2
0 2 0 0 0 0 0 0 2 0
0 1 0 2 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 1 0 0 0 2 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 4 0 0 0 0 1 0 0 0
0 0 0 0 0 0 4 0 1 0
0 0 0 0 0 0 0 0 4 0
4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
2 2 2 2 2 2 2 2 2 2
0 2 0 0 0 0 0 0 2 0
0 1 0 2 0 0 0 0 1 0
0 4 0 1 0 0 0 0 4 0
0 0 2 4 0 0 0 0 0 0
0 0 1 0 0 0 2 0 0 0
0 0 4 2 0 0 1 0 0 0
0 0 0 1 0 0 4 0 0 0
0 2 0 4 0 0 0 0 0 0
0 1 0 0 0 0 2 0 0 0
0 4 0 0 0 0 1 0 2 0
0 0 0 0 0 0 4 0 1 0
0 0 0 0 0 0 0 0 4 0
4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.857142857142861

## Example 3:
Input:
```
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 1 0 0 4
3 0 1 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 1 0 0 0 0 0 4
3 0 0 0 0 1 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 1 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 1 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
```
Expected Output:
```
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 1 4 0 4
3 3 1 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 3 1 0 0 0 0 0 4
3 0 0 0 0 1 4 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 1 4 0 4
3 0 0 0 0 0 0 0 0 4
3 3 1 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
```
Transformed Output:
```
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 3 1 4 0 4
3 3 1 4 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 3 1 4 0 0 0 0 4
3 0 0 0 3 1 4 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
3 0 0 0 0 3 1 4 0 4
3 0 0 0 0 0 0 0 0 4
3 3 1 4 0 0 0 0 0 4
3 0 0 0 0 0 0 0 0 4
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.0
**General Assessment**

The previous code correctly identified the presence of horizontal or vertical borders and their colors. It also correctly identified the trigger pixel color (blue) and the target pixel color (white). However, it failed because it applied the transformation rule too broadly. The code painted *any* adjacent white pixel (above/below for horizontal borders, left/right for vertical borders) with the corresponding border color, provided the target pixel was within the inner grid boundaries.

Analysis of the expected outputs reveals a more specific condition: a white pixel adjacent to a blue pixel is only painted if it lies in the direction of the *closest* border relative to the blue pixel's position. For instance, with horizontal borders, if a blue pixel is closer to the top border than the bottom border, only a white pixel directly *above* it (if present and within the inner grid) will be painted with the top border's color. A white pixel below it would remain unchanged. The converse applies if the blue pixel is closer to the bottom border. A similar logic applies to vertical borders based on closeness to the left or right border. The provided examples do not include cases where a blue pixel is exactly equidistant from the two relevant borders.

**Metrics**

Manual analysis of the examples confirms the "closest border" hypothesis:

*   **Example 1 (Horizontal, H=12):** Blue pixels in rows r=2, 3, 5 are closer to the top (r=0) than the bottom (r=11). They correctly cause painting *above*. Blue pixels in rows r=6, 8, 9 are closer to the bottom; they correctly cause painting *below*.
*   **Example 2 (Horizontal, H=14):** Blue pixels in rows r=2, 3, 5, 6 are closer to the top (r=0) than the bottom (r=13). They correctly cause painting *above*. Blue pixels in rows r=7, 9, 10, 11 are closer to the bottom; they correctly cause painting *below*.
*   **Example 3 (Vertical, W=10):** Blue pixels in columns c=2, 3 are closer to the left (c=0) than the right (c=9). They correctly cause painting *left*. Blue pixels in columns c=5, 6 are closer to the right; they correctly cause painting *right*.

The discrepancies (`Pixels Off`) between the `Transformed Output` and `Expected Output` in the failed tests correspond exactly to the instances where the previous code painted a white pixel adjacent to a blue pixel, but that pixel was *not* in the direction of the closest border.

**Facts (YAML)**


```yaml
task_type: object_transformation

grid_properties:
  - dimensionality: 2D
  - value_range: 0-9 (colors)
  - size_constraints: 1x1 to 30x30

input_features:
  - border:
      property: potential_presence
      type: single_pixel_thick
      location: top/bottom (horizontal) OR left/right (vertical)
      color: uniform, non-white, distinct_pair (e.g., top color != bottom color)
  - inner_grid:
      definition: area excluding the identified borders
      contains:
        - background_pixels: color white (0)
        - trigger_pixels: color blue (1)

output_features:
  - borders: unchanged from input
  - trigger_pixels: unchanged from input (blue pixels remain blue)
  - background_pixels: some white pixels within the inner grid are repainted
  - painted_pixels:
      origin: white pixels from the inner grid
      condition: must be orthogonally adjacent to a blue trigger pixel
      color_source: determined by the closest border to the adjacent blue pixel
      location_constraint: must remain within the inner grid boundaries

transformation_rule:
  - name: border_proximity_painting
  - steps:
      1. Identify border type (horizontal or vertical) and the two distinct border colors (C1, C2). If no valid borders, return input.
      2. Define the inner grid area (excluding borders).
      3. Iterate through each cell (r, c) within the inner grid.
      4. If cell (r, c) contains a blue pixel (1):
          a. Determine the closest border:
             - Horizontal borders (height H): If r < (H-1)-r, closest is top. If r > (H-1)-r, closest is bottom.
             - Vertical borders (width W): If c < (W-1)-c, closest is left. If c > (W-1)-c, closest is right.
          b. Check the adjacent white pixel *in the direction of the closest border*:
             - If closest is top: Check cell (r-1, c).
             - If closest is bottom: Check cell (r+1, c).
             - If closest is left: Check cell (r, c-1).
             - If closest is right: Check cell (r, c+1).
          c. If the checked adjacent cell exists, is within the inner grid boundaries, and is white (0):
             - Paint this adjacent cell with the color of the closest border.

edge_cases:
  - No valid borders found: return input grid unchanged.
  - Blue pixel on the edge of the inner grid: painting only occurs if the adjacent white pixel towards the closest border is also within the inner grid.
  - Blue pixel exactly equidistant from borders: Not observed in training examples. Behavior undefined by examples, but logical assumption might be to paint neither or both (less likely given observed pattern).
```


**Natural Language Program**

1.  Examine the input grid to identify if it has either a pair of uniform, non-white, distinct-colored horizontal borders (top and bottom rows) or a pair of uniform, non-white, distinct-colored vertical borders (left and right columns). The grid must be at least 3x1 (for horizontal) or 1x3 (for vertical) to accommodate borders and an inner area. If no such border pair exists, return the input grid unchanged.
2.  Store the colors of the identified borders (e.g., `color_top`, `color_bottom` or `color_left`, `color_right`).
3.  Define the "inner grid" as the portion of the grid excluding the border rows/columns.
4.  Create a copy of the input grid to serve as the output grid.
5.  Iterate through each cell `(r, c)` of the input grid that falls within the inner grid boundaries.
6.  If the cell `(r, c)` contains a blue pixel (color 1):
    a.  **If horizontal borders were found:** Calculate the distance from the blue pixel's row `r` to the top border (row 0) and the bottom border (row `height-1`).
        i.  If the blue pixel is closer to the top border (`r < (height-1) - r`), check the cell directly above it at `(r-1, c)`. If this cell is within the inner grid (`r-1 >= 1`) and contains a white pixel (color 0), change its color in the output grid to `color_top`.
        ii. If the blue pixel is closer to the bottom border (`r > (height-1) - r`), check the cell directly below it at `(r+1, c)`. If this cell is within the inner grid (`r+1 <= height-2`) and contains a white pixel (color 0), change its color in the output grid to `color_bottom`.
    b.  **If vertical borders were found:** Calculate the distance from the blue pixel's column `c` to the left border (column 0) and the right border (column `width-1`).
        i.  If the blue pixel is closer to the left border (`c < (width-1) - c`), check the cell directly to its left at `(r, c-1)`. If this cell is within the inner grid (`c-1 >= 1`) and contains a white pixel (color 0), change its color in the output grid to `color_left`.
        ii. If the blue pixel is closer to the right border (`c > (width-1) - c`), check the cell directly to its right at `(r, c+1)`. If this cell is within the inner grid (`c+1 <= width-2`) and contains a white pixel (color 0), change its color in the output grid to `color_right`.
7.  Return the modified output grid.
