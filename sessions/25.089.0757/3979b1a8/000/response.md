*   **Perception:**
    *   The input is a square grid (5x5 in the examples).
    *   The input grid contains a distinct pattern composed of three colors: one color for the corners, one for the edges adjacent to the corners, and one forming a central cross shape.
    *   The output grid is also square, with dimensions double that of the input grid (10x10 in the examples).
    *   The output grid can be viewed as a 2x2 arrangement of tiles, where each tile has the same dimensions as the input grid.
    *   The top-left tile of the output grid is an exact copy of the input grid.
    *   The remaining three tiles (top-right, bottom-left, bottom-right) reproduce the *structure* of the input grid but with permuted colors.
    *   There are two distinct color permutation rules applied.
    *   The top-right and bottom-left tiles use the same color permutation rule.
    *   The bottom-right tile uses a different color permutation rule.
    *   To determine the permutation rules, we need to identify the three significant colors in the input grid based on their position: `CornerColor`, `EdgeColor`, and `CenterColor`.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      input_size: N x M (e.g., 5x5)
      output_size: 2N x 2M (e.g., 10x10)
      colors_used: 3 distinct colors in the input pattern.
    objects:
      - object: input_grid_pattern
        description: A pattern composed of three distinct colors occupying specific regions - corners, edges surrounding the center, and a central cross.
        properties:
          - color_corner: The color at the four corners (e.g., input[0,0]).
          - color_edge: The color adjacent to the corners (e.g., input[0,1]).
          - color_center: The color forming the central cross (e.g., input[1,2]).
      - object: output_grid
        description: A 2x2 arrangement of tiles, each the size of the input grid.
        properties:
          - quadrant_top_left: Copy of input grid.
          - quadrant_top_right: Input grid structure with permuted colors.
          - quadrant_bottom_left: Input grid structure with permuted colors (identical permutation to top_right).
          - quadrant_bottom_right: Input grid structure with different permuted colors.
    transformations:
      - action: tile_and_copy
        input: input_grid
        output: top-left quadrant of output_grid
        rule: Direct copy.
      - action: tile_and_permute_1
        input: input_grid
        output: top-right and bottom-left quadrants of output_grid
        rule: >
          Apply color mapping:
          color_corner -> color_corner,
          color_edge -> color_center,
          color_center -> color_edge.
      - action: tile_and_permute_2
        input: input_grid
        output: bottom-right quadrant of output_grid
        rule: >
          Apply color mapping:
          color_corner -> color_center,
          color_edge -> color_corner,
          color_center -> color_edge.
    relationships:
      - relationship: size
        description: Output grid dimensions are double the input grid dimensions.
      - relationship: composition
        description: Output grid is composed of four quadrants derived from the input grid.
      - relationship: color_mapping
        description: Specific color permutations based on original position (corner, edge, center) define the content of three output quadrants.
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions of the input grid (N rows, M columns).
    2.  Create a new output grid with dimensions 2N rows and 2M columns.
    3.  Identify the three distinct colors in the input grid based on their positions:
        *   `CornerColor`: The color at position (0, 0).
        *   `EdgeColor`: The color at position (0, 1).
        *   `CenterColor`: The color at position (1, 2) (or any part of the central cross).
    4.  **Fill the Top-Left Quadrant (rows 0 to N-1, columns 0 to M-1):** Copy the input grid directly into this quadrant of the output grid.
    5.  **Fill the Top-Right Quadrant (rows 0 to N-1, columns M to 2M-1):** Iterate through each pixel (r, c) of the input grid. Determine the color `InputColor` at input[r, c]. Apply the following mapping to get the `OutputColor`:
        *   If `InputColor` is `CornerColor`, `OutputColor` is `CornerColor`.
        *   If `InputColor` is `EdgeColor`, `OutputColor` is `CenterColor`.
        *   If `InputColor` is `CenterColor`, `OutputColor` is `EdgeColor`.
        Place the `OutputColor` at output[r, c + M].
    6.  **Fill the Bottom-Left Quadrant (rows N to 2N-1, columns 0 to M-1):** Iterate through each pixel (r, c) of the input grid. Determine the color `InputColor` at input[r, c]. Apply the *same* mapping as in step 5 to get the `OutputColor`. Place the `OutputColor` at output[r + N, c].
    7.  **Fill the Bottom-Right Quadrant (rows N to 2N-1, columns M to 2M-1):** Iterate through each pixel (r, c) of the input grid. Determine the color `InputColor` at input[r, c]. Apply the following mapping to get the `OutputColor`:
        *   If `InputColor` is `CornerColor`, `OutputColor` is `CenterColor`.
        *   If `InputColor` is `EdgeColor`, `OutputColor` is `CornerColor`.
        *   If `InputColor` is `CenterColor`, `OutputColor` is `EdgeColor`.
        Place the `OutputColor` at output[r + N, c + M].
    8.  Return the completed output grid.