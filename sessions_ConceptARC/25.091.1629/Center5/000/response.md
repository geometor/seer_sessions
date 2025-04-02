*   **Perception of the elements:**
    *   Each input grid contains a single prominent straight line object (either horizontal or vertical) and one or more smaller objects ("dots").
    *   The background is consistently white (0).
    *   The line object remains stationary from input to output.
    *   The dot objects move from their input position to a new position in the output.
    *   The movement (direction and distance) of the dots appears related to their position relative to the midpoint of the line object.

*   **YAML documenting facts:**
    
```yaml
    task_description: Move secondary objects based on their position relative to the midpoint of the primary line object.
    
    elements:
      - role: background
        color: white (0)
      - role: primary_object
        description: The single largest connected component of non-background color, forming a straight line (horizontal or vertical). This object remains static.
        properties:
          - orientation: horizontal or vertical
          - start_coordinate: (row, col) of one end
          - end_coordinate: (row, col) of the other end
          - midpoint_coordinate: Calculated middle point along the line's axis.
      - role: secondary_objects
        description: All other connected components of non-background color ("dots" or small shapes). These objects move.
        properties:
          - centroid_coordinate: The average row and column of all pixels belonging to these secondary objects.
    
    transformation:
      - action: identify_objects
        inputs: input_grid
        outputs: primary_object, secondary_objects
      - action: calculate_properties
        inputs: primary_object, secondary_objects
        outputs: line_orientation, line_midpoint, dots_centroid
      - action: determine_movement_vector
        inputs: line_orientation, line_midpoint, dots_centroid
        outputs: move_direction, move_magnitude
        logic:
          - If line is horizontal:
            - magnitude = absolute difference between dots_centroid.column and line_midpoint.column
            - direction = right if dots_centroid.column < line_midpoint.column else left
          - If line is vertical:
            - magnitude = absolute difference between dots_centroid.row and line_midpoint.row
            - direction = down if dots_centroid.row < line_midpoint.row else up
      - action: apply_movement
        inputs: input_grid, secondary_objects, move_direction, move_magnitude
        outputs: output_grid
        logic:
          - Copy input grid to output grid.
          - Erase secondary objects from their original positions in the output grid (set to background color).
          - Draw secondary objects in their new positions in the output grid, shifted by the calculated direction and magnitude.
    
    examples:
      - train_1:
          primary_object: Horizontal blue line (cols 0-6, row 3). Midpoint col = 3.
          secondary_objects: Two green dots (col 2). Centroid col = 2.
          movement: Centroid (2) < Midpoint (3) -> Move Right. Magnitude = |2 - 3| = 1. Move right by 1.
      - train_2:
          primary_object: Vertical red line (rows 3-9, col 1). Midpoint row = 6.
          secondary_objects: Yellow-Red-Yellow shape (row 3). Centroid row = 3.
          movement: Centroid (3) < Midpoint (6) -> Move Down. Magnitude = |3 - 6| = 3. Move down by 3.
      - train_3:
          primary_object: Horizontal magenta line (cols 1-7, row 5). Midpoint col = 4.
          secondary_objects: Two azure dots (col 7). Centroid col = 7.
          movement: Centroid (7) > Midpoint (4) -> Move Left. Magnitude = |7 - 4| = 3. Move left by 3.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct non-background colored objects (connected components) in the input grid.
    2.  Determine the largest object; this is the "line". All other objects are "dots".
    3.  Find the orientation (horizontal or vertical) and the two end coordinates of the line.
    4.  Calculate the midpoint coordinate of the line along its main axis (column for horizontal, row for vertical).
    5.  Calculate the centroid coordinate (average row and column) of all pixels belonging to the "dot" objects.
    6.  Compare the centroid coordinate to the line's midpoint coordinate along the line's main axis:
        *   If the line is horizontal: Calculate the magnitude as the absolute difference between the centroid's column and the line's midpoint column. Determine the direction: move right if the centroid column is less than the midpoint column, otherwise move left.
        *   If the line is vertical: Calculate the magnitude as the absolute difference between the centroid's row and the line's midpoint row. Determine the direction: move down if the centroid row is less than the midpoint row, otherwise move up.
    7.  Create the output grid by copying the input grid.
    8.  In the output grid, change the color of the original pixels belonging to the "dot" objects to the background color (white - 0).
    9.  Draw the "dot" objects in their new positions by shifting each original dot pixel according to the calculated direction and magnitude.