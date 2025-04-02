*   **Perception:**
    *   The input grids contain three colors: white (0) as the background, blue (1) forming an object, and red (2) forming a line.
    *   The red object is always a straight line, either vertical or horizontal.
    *   The blue object is a distinct shape that does not touch the red line.
    *   In the output grid, the red line and the white background remain unchanged.
    *   The blue object moves its position. The shape of the blue object remains the same.
    *   The direction and distance of the blue object's movement seem to depend on the orientation of the red line and the relative position of the blue object to the red line.
    *   When the red line is vertical, the blue object moves 1 step horizontally away from the line (to the right in the examples).
    *   When the red line is horizontal, the blue object moves 2 steps vertically away from the line (downwards in the example).

*   **YAML Facts:**
    
```yaml
    task_description: Move a blue object away from a red line based on the line's orientation.
    elements:
      - object: background
        color: white (0)
        role: static_canvas
      - object: primary_shape
        color: blue (1)
        role: movable_object
        properties:
          - shape: variable (L-shape, plus, compound, U-shape in examples)
          - contiguity: contiguous block of blue pixels
      - object: constraint_line
        color: red (2)
        role: static_constraint
        properties:
          - shape: straight line (vertical or horizontal)
          - contiguity: contiguous block of red pixels
    relationships:
      - type: spatial
        description: The blue object is positioned relative to the red line (left/right or above/below).
      - type: interaction
        description: The red line dictates the movement of the blue object.
    actions:
      - action: identify_objects
        inputs: [input_grid]
        outputs: [blue_object_pixels, red_object_pixels]
      - action: determine_line_orientation
        inputs: [red_object_pixels]
        outputs: [orientation (vertical/horizontal)]
      - action: determine_relative_position
        inputs: [blue_object_pixels, red_object_pixels, orientation]
        outputs: [relative_pos (left/right/above/below)]
      - action: calculate_shift
        inputs: [orientation, relative_pos]
        outputs: [shift_vector (dx, dy)]
        logic:
          - if orientation is vertical, shift is (1, 0) if relative_pos is left, (-1, 0) if right.
          - if orientation is horizontal, shift is (0, 2) if relative_pos is above, (0, -2) if below.
      - action: apply_shift
        inputs: [input_grid, blue_object_pixels, shift_vector]
        outputs: [output_grid]
        logic: Create a new grid, copy the red line and background from the input, place the blue object at the shifted coordinates.
    ```


*   **Natural Language Program:**
    1.  Identify the set of coordinates occupied by the blue pixels (color 1) representing the blue object.
    2.  Identify the set of coordinates occupied by the red pixels (color 2) representing the red line.
    3.  Determine the orientation of the red line:
        *   If all red pixels share the same column index, the line is vertical.
        *   If all red pixels share the same row index, the line is horizontal.
    4.  Determine the shift vector (change in row `dy`, change in column `dx`):
        *   If the red line is vertical:
            *   Determine the column index of the red line (`red_col`).
            *   Find the average column index of the blue object pixels (`blue_avg_col`).
            *   If `blue_avg_col` < `red_col` (blue is left), set the shift vector to `(dx=1, dy=0)`.
            *   If `blue_avg_col` > `red_col` (blue is right), set the shift vector to `(dx=-1, dy=0)`.
        *   If the red line is horizontal:
            *   Determine the row index of the red line (`red_row`).
            *   Find the average row index of the blue object pixels (`blue_avg_row`).
            *   If `blue_avg_row` < `red_row` (blue is above), set the shift vector to `(dx=0, dy=2)`.
            *   If `blue_avg_row` > `red_row` (blue is below), set the shift vector to `(dx=0, dy=-2)`.
    5.  Create the output grid, identical in size to the input grid and initially filled with the background color (white, 0).
    6.  Copy the red line from the input grid to the output grid at its original position.
    7.  For each blue pixel at coordinate `(row, col)` in the input grid, place a blue pixel at `(row + dy, col + dx)` in the output grid.