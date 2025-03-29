*   **Perception:** The input grids contain vertical lines of azure pixels starting from the top row and extending downwards for a few rows. There are also one or more red objects located somewhere below these initial azure lines. The background is white. The output grids show that the azure lines have been extended downwards from their initial position. This extension continues until the bottom of the grid, *unless* the extension encounters a red pixel in the same column. If a red pixel is encountered, the azure extension stops *at that row*, effectively overwriting any white pixels above the red pixel in that column but not overwriting the red pixel itself or extending below it. Columns without red pixels below the initial azure lines are extended all the way to the bottom row.

*   **YAML Facts:**
    
```yaml
    background_color: 0 # white
    line_color: 8 # azure
    obstacle_color: 2 # red

    elements:
      - object: azure_lines
        color: 8
        shape: vertical lines
        location: starting from top row, extending downwards
        properties:
          - column_index
          - initial_bottom_row_index
      - object: red_obstacles
        color: 2
        shape: variable, single or multiple contiguous blocks
        location: below initial azure lines
        properties:
          - row_index
          - column_index
      - object: background
        color: 0
        location: fills remaining space

    action:
      type: extend_lines
      source_object: azure_lines
      target_color: 8
      direction: downwards
      termination_condition:
        - type: grid_boundary
          boundary: bottom_row
        - type: obstacle_collision
          obstacle_object: red_obstacles
          behavior: stop extension at the row of the obstacle in the same column

    relationship:
      - The downward extension of an azure line in a specific column is blocked by the presence of a red obstacle in the same column at a lower row.
      - If no red obstacle exists below an azure line in its column, the line extends to the bottom edge of the grid.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Identify all columns that contain azure (8) pixels in the input grid.
    3.  For each identified column `c`:
        a.  Find the row index `r_start` of the lowest azure (8) pixel in column `c` in the input grid.
        b.  Iterate through the rows `r` starting from `r_start + 1` down to the last row of the grid.
        c.  Examine the pixel at position `(r, c)` in the *input* grid.
        d.  If the pixel at `(r, c)` in the input grid is red (2), stop the extension process for this column `c` (do not modify this row `r` or any subsequent rows in this column).
        e.  If the pixel at `(r, c)` in the input grid is *not* red (2), change the pixel at position `(r, c)` in the *output* grid to azure (8).
    4.  Return the modified output grid.