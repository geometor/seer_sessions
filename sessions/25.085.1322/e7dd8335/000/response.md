*   **Perception:**
    *   The input grids contain a background of white pixels (0) and a single connected object composed of blue pixels (1).
    *   The output grids are largely identical to the input grids, with the key difference being that some blue pixels (1) in the original object have been changed to red pixels (2).
    *   The blue object varies in shape and position across examples but generally forms rectangular outlines or structures.
    *   The transformation consistently affects the lower portion of the blue object. Pixels below a certain horizontal line within the object's bounds are recolored.
    *   The dividing line appears to be related to the horizontal midpoint of the blue object's vertical extent. Blue pixels strictly below this midpoint row are changed to red.

*   **Facts:**
    
```yaml
    elements:
      - item: grid
        properties:
          - contains: pixels
          - background_color: white (0)
      - item: object
        properties:
          - color: blue (1)
          - contiguous: true
          - shape: variable (often rectangular or frame-like)
          - vertical_extent: defined by minimum and maximum row indices containing blue pixels
          - horizontal_midpoint_row: calculated based on the vertical extent (floor((min_row + max_row) / 2))
      - item: transformation
        properties:
          - input_color: blue (1)
          - output_color: red (2)
          - condition: applies to blue pixels located in rows strictly below the object's horizontal_midpoint_row
          - scope: affects only the blue object pixels
          - preserves: background pixels (white), blue pixels at or above the midpoint row
    ```


*   **Natural Language Program:**
    1.  Identify all pixels with the color blue (1) in the input grid.
    2.  Determine the minimum (`min_row`) and maximum (`max_row`) row indices occupied by these blue pixels.
    3.  Calculate the horizontal midpoint row index: `mid_row = floor((min_row + max_row) / 2)`.
    4.  Create a copy of the input grid to serve as the output grid.
    5.  Iterate through each pixel of the input grid.
    6.  If a pixel at `(row, col)` has the color blue (1) AND its row index `row` is greater than `mid_row`, change the color of the corresponding pixel in the output grid to red (2).
    7.  Otherwise, keep the pixel's color the same as in the input grid.
    8.  Return the modified grid as the output.