*   **Perception of Task Elements:**
    *   The input consists of grids (matrices) containing integer values, primarily 0 representing the background.
    *   Within the grid, there are distinct rectangular regions defined by a border of a non-zero color (e.g., 2, 3, 1, 4).
    *   The interior of these rectangles is mostly filled with the same color as the border, but contains exactly one cell with a different non-zero color (the 'special' cell).
    *   The transformation modifies the interior of these rectangular regions while preserving the border and the background.
    *   The modification involves replacing the original interior color with a pattern based on the color and position of the 'special' cell. The pattern consists of the special cell's color arranged in a diagonal cross ('X') centered at the special cell's original location, with the remaining interior cells becoming 0.

*   **YAML Fact Documentation:**
    
```yaml
    task_elements:
      - object: grid
        description: A 2D array of integers representing pixels or cells.
      - object: background
        property: color
        value: 0
        relationship: unchanged in output
      - object: region
        description: A rectangular area within the grid.
        property: border_color
        value: non-zero integer (B)
        property: interior_color
        value: same as border_color (B)
      - object: special_cell
        description: A single cell within a region's interior.
        property: color
        value: non-zero integer (S), different from the region's border/interior color.
        relationship: determines the pattern color in the output.
        relationship: defines the center of the output pattern.
      - object: pattern
        description: The structure replacing the interior of a region in the output.
        property: shape
        value: diagonal cross ('X')
        property: color
        value: color of the special_cell (S)
        property: background
        value: 0
        relationship: centered at the original location of the special_cell.
    actions:
      - name: identify_regions
        input: input grid
        output: list of identified rectangular regions matching criteria (border B, interior B, one special cell S)
      - name: preserve_elements
        input: input grid, identified regions
        output: output grid with background and region borders copied from input
      - name: transform_interior
        input: identified region, special_cell location (r_s, c_s), special_cell color (S)
        output: modified interior for the output grid
        details: For each interior cell (r, c), if abs(r - r_s) == abs(c - c_s), set output cell to S, otherwise set to 0.
      - name: compose_output
        input: preserved elements grid, transformed interiors
        output: final output grid
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through the input grid to identify rectangular regions that meet the following criteria:
        *   The region is bounded by a single, non-zero color `B`.
        *   The interior of the region (cells not on the border) consists entirely of color `B`, except for exactly one cell with a different non-zero color `S` located at coordinates `(r_s, c_s)`.
    3.  For each identified region:
        *   Iterate through all cells `(r, c)` located strictly *inside* the border of this region.
        *   Calculate the absolute row distance `dr = abs(r - r_s)` and the absolute column distance `dc = abs(c - c_s)` from the special cell's location `(r_s, c_s)`.
        *   If `dr` is equal to `dc`, set the value of the cell `(r, c)` in the *output* grid to the special cell color `S`.
        *   Otherwise (if `dr` is not equal to `dc`), set the value of the cell `(r, c)` in the *output* grid to 0.
    4.  Leave all cells in the output grid that are not part of the interior of an identified region unchanged from their initial copied value (i.e., preserve the background and the borders of identified regions).
    5.  Return the final output grid.