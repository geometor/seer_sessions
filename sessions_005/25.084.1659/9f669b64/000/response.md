*   **Perception:**
    *   Each task involves a grid with a background color (orange/7) and typically three distinct colored objects.
    *   Comparing the input and output grids reveals that one object remains static (stable object).
    *   Another object changes its position but retains its shape and color (moving object).
    *   The third object changes its shape, splitting into two separate pieces (split object).
    *   There's a clear interaction: the moving object seems to "push" the split object apart as it moves towards an edge of the grid.
    *   The direction of the split (horizontal or vertical) is perpendicular to the direction of the moving object's primary movement.
    *   The gap created in the split object matches the dimension (width or height) of the moving object along the axis perpendicular to the split.
    *   The moving object's final position is at the edge of the grid (top, bottom, left, or right), aligned with its original position along the axis parallel to its movement.
    *   The two parts of the split object are shifted outwards from the gap created by the moving object. The shift distance appears related to half the size of the gap.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_properties:
        - background_color: 7 (orange)
        - dimensions: 10x10 in all examples
      object_count: 3 distinct non-background objects per example.

    objects:
      - role: stable
        description: An object that does not change position or shape.
        example_train_1: Azure rectangle (8)
        example_train_2: Magenta shape (6)
        example_train_3: Red shape (2)
      - role: moving
        description: An object that changes position but retains its shape and color. Moves towards one of the four grid edges.
        properties: [color, shape, original_position, destination_position, direction_of_movement]
        example_train_1: Green rectangle (3), moves Up to top edge.
        example_train_2: Blue rectangle (1), moves Down to bottom edge.
        example_train_3: Blue rectangle (1), moves Left to left edge.
      - role: split
        description: An object that is split into two pieces by the action of the moving object.
        properties: [color, original_shape, original_position, final_shapes, final_positions]
        example_train_1: Maroon rectangle (9), splits horizontally.
        example_train_2: Azure rectangle (8), splits horizontally.
        example_train_3: Yellow line (4), splits vertically.

    relationships_and_actions:
      - action: identify_roles
        description: Determine which object is stable, moving, and split by comparing input and output.
      - action: determine_movement
        input: moving_object
        output: direction (Up, Down, Left, Right), destination_edge
        description: Identify the primary direction and target edge for the moving object.
      - action: determine_split_axis
        input: direction_of_movement
        output: split_axis (Horizontal, Vertical)
        rule: Split axis is perpendicular to movement direction.
      - action: calculate_gap
        input: moving_object, split_axis
        output: gap_dimension, gap_location
        rule:
          - If split is Horizontal, gap_width = moving_object.width, gap_columns = moving_object.original_columns.
          - If split is Vertical, gap_height = moving_object.height, gap_rows = moving_object.original_rows.
      - action: perform_split
        input: split_object, gap_dimension, gap_location, split_axis
        output: two_split_pieces
        rule:
          - shift_distance = gap_dimension / 2
          - If Horizontal split: shift left part left by shift_distance, shift right part right by shift_distance.
          - If Vertical split: shift top part up by shift_distance, shift bottom part down by shift_distance.
      - action: place_moving_object
        input: moving_object, destination_edge
        output: final_position
        rule: Place object at the destination edge, aligned with its original position along the axis parallel to movement.
      - action: construct_output
        input: background_color, stable_object, two_split_pieces, moved_object_at_destination
        output: final_grid
        rule: Draw background, stable object, split pieces, and moved object in their final positions. Original position of the moving object becomes background.

    ```


*   **Natural Language Program:**
    1.  Identify the background color (typically the most frequent color).
    2.  Identify all distinct contiguous non-background colored objects in the input grid.
    3.  By comparing the input and output grids, determine the roles of the three objects:
        *   **Stable Object:** The object whose position and pixels remain identical in the output.
        *   **Moving Object:** The object whose pixels change location but maintain the same relative shape and color. Find its original bounding box.
        *   **Split Object:** The object whose pixels change location and form two separate pieces in the output. Find its original bounding box.
    4.  Determine the primary direction of movement (Up, Down, Left, or Right) for the **Moving Object** by observing its displacement towards a grid edge.
    5.  Determine the axis of the split for the **Split Object**: if movement is vertical (Up/Down), the split is horizontal; if movement is horizontal (Left/Right), the split is vertical.
    6.  Calculate the gap dimension: this is the width of the **Moving Object** if the split is horizontal, or the height of the **Moving Object** if the split is vertical.
    7.  Calculate the gap location: these are the original columns covered by the **Moving Object** if the split is horizontal, or the original rows covered by the **Moving Object** if the split is vertical.
    8.  Calculate the shift distance required for the split: `shift = gap_dimension / 2`.
    9.  Create the output grid, initially filled with the background color.
    10. Draw the **Stable Object** onto the output grid at its original position.
    11. Split the **Split Object**:
        *   If splitting horizontally: For each pixel of the **Split Object**, if its column is less than the minimum gap column, draw it shifted left by `shift` columns in the output grid. If its column is greater than the maximum gap column, draw it shifted right by `shift` columns in the output grid.
        *   If splitting vertically: For each pixel of the **Split Object**, if its row is less than the minimum gap row, draw it shifted up by `shift` rows in the output grid. If its row is greater than the maximum gap row, draw it shifted down by `shift` rows in the output grid.
    12. Determine the final top-left corner position for the **Moving Object**:
        *   If moving Up: `(0, original_min_col)`
        *   If moving Down: `(grid_height - moving_object_height, original_min_col)`
        *   If moving Left: `(original_min_row, 0)`
        *   If moving Right: `(original_min_row, grid_width - moving_object_width)`
    13. Draw the **Moving Object** at this calculated final position onto the output grid.