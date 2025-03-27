*   **Perception:**
    *   The task involves transforming a 3x3 input grid into a 9x9 output grid.
    *   The output grid is primarily white (0), with a pattern derived from the input grid placed within it.
    *   The input grid is replicated three times either horizontally or vertically.
    *   The placement and orientation (horizontal/vertical tiling) of the replicated input pattern within the 9x9 output grid depend on a specific feature of the input grid.
    *   Observing the examples reveals that the determining feature is the presence of a homogeneous line (a row or column where all pixels have the same color) within the 3x3 input grid.
    *   If the input has a homogeneous row, the replication is horizontal.
    *   If the input has a homogeneous column, the replication is vertical.
    *   The position of this homogeneous line dictates where the replicated pattern is placed in the output grid. A homogeneous line at index `i` (0, 1, or 2) causes the pattern to be placed starting at index `i * 3` in the corresponding dimension (row index for horizontal tiling, column index for vertical tiling).

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    input_grid_size: 3x3
    output_grid_size: 9x9
    background_color: white (0)
    primary_object: The 3x3 input grid pattern.
    actions:
      - identify_homogeneous_line:
          target: input_grid
          result: line_type (row or column), line_index (0, 1, or 2)
      - replicate_pattern:
          target: input_grid
          count: 3
          orientation: determined by line_type (horizontal for row, vertical for column)
          result: intermediate_pattern (3x9 for horizontal, 9x3 for vertical)
      - place_pattern:
          target: output_grid (initially all white)
          pattern: intermediate_pattern
          position: determined by line_index (start_row = line_index * 3 for horizontal, start_col = line_index * 3 for vertical)
    relationships:
      - The orientation of replication (horizontal/vertical) depends on whether the homogeneous line is a row or column.
      - The placement of the replicated pattern depends on the index of the homogeneous line.
    assumptions:
      - Each input grid contains exactly one homogeneous line (either a row or a column).
    ```


*   **Natural Language Program:**
    1.  Initialize a 9x9 output grid filled entirely with white pixels (value 0).
    2.  Inspect the 3x3 input grid to find if any row consists of three identical pixel colors.
    3.  If a homogeneous row is found at row index `R` (where `R` can be 0, 1, or 2):
        a.  Create a 3x9 pattern by horizontally tiling the 3x3 input grid three times side-by-side.
        b.  Place this 3x9 pattern onto the 9x9 output grid, starting at row `R * 3` and column 0.
    4.  Else (if no homogeneous row is found), inspect the input grid to find if any column consists of three identical pixel colors. Assume one will be found based on the provided examples.
    5.  If a homogeneous column is found at column index `C` (where `C` can be 0, 1, or 2):
        a.  Create a 9x3 pattern by vertically tiling the 3x3 input grid three times one below the other.
        b.  Place this 9x3 pattern onto the 9x9 output grid, starting at row 0 and column `C * 3`.
    6.  Return the modified 9x9 output grid.