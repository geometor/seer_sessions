
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 3 0 4 0 3 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 3 0 4 0 3 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 8 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 8 0 3 0 8 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 8 0 3 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 8 0 3 0 8 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 3 0 8 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 8 0 1 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 4 0 4 0 0 0
0 0 0 8 0 1 0 8 0 0
0 0 0 0 4 0 4 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves completing potentially incomplete symmetrical patterns of colored pixels against a white background. The input grids contain arrangements of colored pixels (non-zero values). The output grids contain the same initial pixels plus additional colored pixels, such that the final pattern exhibits point symmetry (180-degree rotational symmetry) and potentially axial symmetry (reflection across horizontal and vertical axes) relative to a specific center point. This center point appears to be the geometric center of the bounding box encompassing all non-white pixels in the input grid. For every colored pixel in the input, corresponding pixels are added (or ensured to exist) at locations symmetrical to it with respect to the calculated center point (reflection across the center, reflection across the horizontal line through the center, and reflection across the vertical line through the center).

*   **YAML Facts:**
    
```yaml
    task_description: Complete symmetrical patterns based on a central point.
    
    elements:
      - element: grid
        description: A 2D array of pixels with integer values 0-9 representing colors. Background is white (0).
      - element: pattern
        description: A configuration of non-white pixels within the grid.
      - element: bounding_box
        description: The smallest rectangle containing all non-white pixels.
        properties:
          - top_row: minimum row index of non-white pixels
          - left_col: minimum column index of non-white pixels
          - bottom_row: maximum row index of non-white pixels
          - right_col: maximum column index of non-white pixels
      - element: center_of_symmetry
        description: The central point used for reflections.
        calculation: Determined as the geometric center of the bounding box of non-white pixels; `center_row = (top_row + bottom_row) / 2`, `center_col = (left_col + right_col) / 2`.
    
    actions:
      - action: identify_non_white_pixels
        description: Locate all pixels in the input grid with a color value other than 0.
      - action: calculate_bounding_box
        description: Find the minimum and maximum row and column indices of the non-white pixels.
      - action: determine_center_of_symmetry
        description: Calculate the center point based on the bounding box coordinates.
      - action: reflect_pixels
        description: For each non-white pixel, calculate the coordinates of its symmetrical counterparts.
        details:
          - reflection_across_horizontal: `(2 * center_row - original_row, original_col)`
          - reflection_across_vertical: `(original_row, 2 * center_col - original_col)`
          - reflection_across_center: `(2 * center_row - original_row, 2 * center_col - original_col)`
      - action: populate_output_grid
        description: Create the output grid by copying the input grid and then adding the reflected pixels, ensuring the pixel at the reflected coordinates has the same color as the original pixel.
    
    relationships:
      - relationship: symmetry
        description: The output pattern is symmetrical with respect to the center_of_symmetry. Each non-white pixel in the input implies the existence of pixels of the same color at its symmetrical positions in the output.
    ```


*   **Natural Language Program:**
    1.  Start with the input grid.
    2.  Identify all pixels that are not white (color 0). If there are no non-white pixels, the output is identical to the input.
    3.  Determine the bounding box enclosing all non-white pixels by finding their minimum and maximum row and column indices (`min_r`, `min_c`, `max_r`, `max_c`).
    4.  Calculate the center of symmetry: `center_r = (min_r + max_r) / 2`, `center_c = (min_c + max_c) / 2`. (These divisions should result in integer or half-integer coordinates defining the center axis/point).
    5.  Create a copy of the input grid to serve as the basis for the output grid.
    6.  Iterate through each pixel `(r, c)` in the input grid that has a non-white color `clr`.
    7.  For each such pixel `(r, c)`, calculate the coordinates of its three symmetrical counterparts relative to the center `(center_r, center_c)`:
        a.  Horizontal reflection: `r_h = 2 * center_r - r`, `c_h = c`
        b.  Vertical reflection: `r_v = r`, `c_v = 2 * center_c - c`
        c.  Point reflection (center): `r_p = 2 * center_r - r`, `c_p = 2 * center_c - c`
    8.  Ensure that the calculated coordinates `(r_h, c_h)`, `(r_v, c_v)`, and `(r_p, c_p)` are valid integer indices within the grid boundaries.
    9.  For each valid symmetrical coordinate, set the color of the corresponding pixel in the output grid to `clr`. (This process effectively ensures that the original pixel `(r, c)` and its three symmetrical counterparts all have the color `clr` in the output grid).
    10. Return the modified grid as the output.
