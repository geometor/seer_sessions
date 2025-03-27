*   **Perception**:
    *   The input and output grids are the same size (11x11 in the examples).
    *   Both grids feature an outer border, primarily magenta (6), enclosing an inner area, primarily orange (7).
    *   Within the orange area in the input grid, there are distinct objects made of other colors (azure, maroon, red, gray).
    *   The output grid retains the internal objects and the orange background mostly unchanged.
    *   The key transformation occurs on the border pixels. Specific border pixels change color based on the internal objects.
    *   For each internal object, its color is "projected" onto one cell of the border. The border chosen (top, bottom, left, or right) is the one closest to the object's center.
    *   The specific cell on the chosen border that receives the object's color corresponds to the row or column where the object has the most pixels.
    *   Simultaneously, the border cell directly opposite the projected color is changed to white (0).

*   **Facts YAML**:
    
```yaml
    task_context:
      grid_size: Fixed, input and output grids have the same dimensions.
      colors:
        border: magenta (6) - forms the outermost frame.
        background: orange (7) - dominant color inside the border.
        objects: [azure (8), maroon (9), red (2), gray (5)] - form distinct shapes within the background.
        projection_target: The border pixels (magenta 6).
        projection_opposite: white (0).
    
    elements:
      - element: border
        description: The outermost single layer of pixels, initially magenta (6).
        properties: [color: magenta(6), location: edge]
      - element: background
        description: The area inside the border, predominantly orange (7).
        properties: [color: orange(7), location: interior]
      - element: internal_objects
        description: Connected components of pixels within the background area, with colors distinct from the border and background.
        properties: [color: various (azure, maroon, red, gray), location: interior, shape: variable]
    
    transformations:
      - action: identify_objects
        input: input grid
        output: list of internal objects (color, pixels, bounding box, center)
        criteria: Color is not border color and not background color. Connected components.
      - action: determine_projection
        input: internal object (color C, center, pixels), grid dimensions (H, W)
        output: projection border, projection coordinate (row or col), opposite coordinate (row or col)
        logic:
          1. Calculate distance from object center to each of the four borders.
          2. Identify the closest border (projection border). Tie-break: Top > Left > Bottom > Right.
          3. If projecting vertically (Top/Bottom): Find the column `proj_c` with the max count of object pixels. Tie-break: min column index. The opposite coordinate is also `proj_c`.
          4. If projecting horizontally (Left/Right): Find the row `proj_r` with the max count of object pixels. Tie-break: min row index. The opposite coordinate is also `proj_r`.
      - action: apply_projection
        input: output grid (initially copy of input), object color C, projection border, projection coordinate, opposite coordinate
        output: modified output grid
        logic:
          1. Determine target cell `(r_target, c_target)` on the projection border based on the projection coordinate.
          2. Determine opposite cell `(r_opp, c_opp)` on the opposite border based on the opposite coordinate.
          3. Set `output_grid[r_target, c_target] = C`.
          4. Set `output_grid[r_opp, c_opp] = 0` (white).
    
    relationships:
      - relation: object_to_border_projection
        description: Each internal object projects its color onto the nearest border edge and causes the opposite border edge cell (in the same row/column) to turn white.
        details:
          - Proximity: Determined by the object's center relative to the borders.
          - Coordinate: Determined by the row/column index where the object has the maximum pixel count along the relevant axis.
    ```


*   **Natural Language Program**:
    1.  Create a copy of the input grid to serve as the initial output grid.
    2.  Identify the primary border color (e.g., magenta 6) and the primary internal background color (e.g., orange 7).
    3.  Find all distinct connected objects within the grid whose color is neither the border color nor the background color.
    4.  For each identified object:
        a.  Note its color (`object_color`).
        b.  Determine its center coordinates (`center_row`, `center_col`).
        c.  Calculate the distance from the center to the top, bottom, left, and right borders of the grid.
        d.  Identify the border closest to the object's center. Use a tie-breaking rule if distances are equal (e.g., prioritize Top, then Left, then Bottom, then Right).
        e.  If the closest border is Top or Bottom (vertical projection):
            i.  Find the column index (`proj_col`) where the object has the maximum number of pixels. If multiple columns have the same maximum count, choose the smallest column index.
            ii. If the closest border is Top: Set the pixel at `(0, proj_col)` in the output grid to `object_color`, and set the pixel at `(grid_height - 1, proj_col)` to white (0).
            iii. If the closest border is Bottom: Set the pixel at `(grid_height - 1, proj_col)` in the output grid to `object_color`, and set the pixel at `(0, proj_col)` to white (0).
        f.  If the closest border is Left or Right (horizontal projection):
            i.  Find the row index (`proj_row`) where the object has the maximum number of pixels. If multiple rows have the same maximum count, choose the smallest row index.
            ii. If the closest border is Left: Set the pixel at `(proj_row, 0)` in the output grid to `object_color`, and set the pixel at `(proj_row, grid_width - 1)` to white (0).
            iii. If the closest border is Right: Set the pixel at `(proj_row, grid_width - 1)` in the output grid to `object_color`, and set the pixel at `(proj_row, 0)` to white (0).
    5.  Return the modified output grid.