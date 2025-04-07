*   **Perception of task elements:**
    *   The input is a 2D grid containing mostly zeros and a few non-zero digits (1, 2, 3, 6). These non-zero digits act as markers or starting points.
    *   The output is a modified 2D grid where lines or patterns emanate from the original marker positions.
    *   The value of the marker determines the type, direction, and length of the line drawn.
        *   `1`: Draws a horizontal line segment `[1, 5, 5]` extending 2 cells to the right from the marker.
        *   `2`: Draws a horizontal line segment `[2, 5, 5, 5, 2]` extending 4 cells to the left from the marker, bounded by `2`s.
        *   `3`: Draws a vertical line segment `[3, 5, 5, 3]` extending 3 cells down from the marker, bounded by `3`s.
        *   `6`: Draws a vertical line segment `[6, 5, 5, 5, 5, 5, 6]` extending 6 cells up from the marker, bounded by `6`s.
    *   The digit `5` is used to fill the path of the lines between the endpoints.
    *   If two paths (segments filled with `5`) intersect at a cell, that cell's value becomes `4`.
    *   From each intersection point (marked with `4`), a diagonal line of `4`s is drawn starting one cell down and one cell left, continuing in the down-left direction until the grid boundary.

*   **YAML Facts:**
    
```yaml
    grid:
      type: 2D array of integers
      properties:
        size: variable (e.g., 10x10, 11x11, 9x9)
        background_color: 0
    
    objects:
      - object: marker
        properties:
          value: non-zero integer (1, 2, 3, 6) in input
          location: (row, col) coordinates in the input grid
      - object: line_segment
        properties:
          type: horizontal or vertical
          direction: right, left, down, up (determined by marker value)
          length: specific integer (determined by marker value)
          endpoints_color: same as marker value
          path_color: 5
      - object: intersection
        properties:
          location: (row, col) where two path_color segments (5) overlap
          color: 4
      - object: diagonal_line
        properties:
          origin: starts one cell down and left from an intersection point
          direction: down-left
          color: 4
          termination: grid boundary
    
    relationships:
      - marker determines the properties (type, direction, length, colors) of the line_segment originating from it.
      - intersection occurs at the overlap location of path_color (5) from different line_segments.
      - diagonal_line originates relative to an intersection location.
    
    actions:
      - find_markers: Identify location and value of all non-zero cells in the input grid.
      - draw_lines: For each marker, generate the coordinates and values (endpoints and path color 5) for its corresponding line_segment based on its value. Store these potential modifications.
      - detect_intersections: Identify coordinates where path color 5 is assigned by more than one line_segment.
      - resolve_grid: Create the output grid by:
          - Placing all line_segment endpoints (1, 2, 3, 6).
          - Placing path color 5 for non-intersecting parts of line_segments.
          - Placing intersection color 4 at detected intersection coordinates.
      - draw_diagonals: For each intersection coordinate (now marked with 4), generate the coordinates for the down-left diagonal line of 4s until the boundary, and update the output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid (or as a grid of zeros with the same dimensions).
    2.  Create a temporary data structure (e.g., a grid or list) to record the cells painted by the 'path' color `5` and which marker generated them.
    3.  Iterate through each cell `(r, c)` of the input grid.
    4.  If a cell contains a marker `N` (non-zero value):
        *   Based on the value `N`, determine the sequence of cells and their corresponding values (endpoint `N` or path `5`) for the line segment:
            *   If `N = 1`: Cells `(r, c)=1`, `(r, c+1)=5`, `(r, c+2)=5`.
            *   If `N = 2`: Cells `(r, c-4)=2`, `(r, c-3)=5`, `(r, c-2)=5`, `(r, c-1)=5`, `(r, c)=2`.
            *   If `N = 3`: Cells `(r, c)=3`, `(r+1, c)=5`, `(r+2, c)=5`, `(r+3, c)=3`.
            *   If `N = 6`: Cells `(r-6, c)=6`, `(r-5, c)=5`, `(r-4, c)=5`, `(r-3, c)=5`, `(r-2, c)=5`, `(r-1, c)=5`, `(r, c)=6`.
        *   For each cell `(r', c')` in the generated sequence that is within the grid boundaries:
            *   If the value assigned is the endpoint color `N`, update the output grid at `(r', c')` with `N`.
            *   If the value assigned is the path color `5`, record this assignment (e.g., add marker ID to a list associated with cell `(r', c')` in the temporary structure).
    5.  Identify intersection points: Iterate through the temporary structure. Any cell `(ri, ci)` associated with more than one marker ID is an intersection. Store these intersection coordinates.
    6.  Finalize line drawing: Iterate through the temporary structure again. For each cell `(r', c')` associated with path color `5`:
        *   If `(r', c')` is an intersection point, set the output grid cell `(r', c')` to `4`.
        *   If `(r', c')` is not an intersection point and the output grid cell `(r', c')` is currently `0`, set it to `5`. (Avoid overwriting endpoints).
    7.  Draw diagonal lines: For each identified intersection coordinate `(ri, ci)`:
        *   Initialize `(rd, cd) = (ri + 1, ci - 1)`.
        *   While `(rd, cd)` is within the grid boundaries:
            *   Set the output grid cell `(rd, cd)` to `4`.
            *   Update `(rd, cd)` to `(rd + 1, cd - 1)`.
    8.  Return the final output grid.