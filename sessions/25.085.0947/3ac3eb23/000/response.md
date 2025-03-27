*   **Perception:**
    *   The input grids contain one or more non-white pixels, located only in the top row (row 0) in the provided examples. The rest of the grid is white (0).
    *   The output grids retain the original non-white pixels from the input.
    *   Additional non-white pixels appear in the output grid in the rows below the original non-white pixels.
    *   The pattern of new pixels depends on the column of the original pixel and the row number.
    *   For a non-white pixel at `(0, c)` with color `C`, new pixels of color `C` are added in subsequent rows `r > 0`.
    *   If row `r` is odd, pixels are added at `(r, c-1)` and `(r, c+1)`.
    *   If row `r` is even, a pixel is added at `(r, c)`.
    *   This pattern continues down to the bottom of the grid.
    *   Each initial non-white pixel generates its own independent pattern.
    *   The generation respects grid boundaries; pixels are only placed if the coordinates are valid.

*   **YAML Facts:**
    
```yaml
    task: Generate vertical patterns extending downwards from non-white pixels in the input grid.
    
    elements:
      - type: grid
        attributes: [input, output]
        properties:
          size: variable height and width
          pixels: values 0-9 (colors)
    
      - type: object
        name: seed_pixel
        description: A non-white pixel in the input grid.
        properties:
          color: The color value (1-9).
          position: (row, column) coordinates. In examples, always row 0.
    
      - type: pattern
        name: descending_alternating_pattern
        description: The pattern generated below a seed_pixel.
        rules:
          - condition: Row index 'r' relative to grid top (0-indexed).
          - rule_odd_row: If 'r' is odd, place seed_pixel color at (r, seed_col - 1) and (r, seed_col + 1).
          - rule_even_row: If 'r' is even, place seed_pixel color at (r, seed_col).
          - boundary_check: Apply rules only if target coordinates are within grid bounds.
          - extent: Pattern applies from the row below the seed_pixel down to the bottom row.
    
    transformation:
      - action: initialize_output
        source: input_grid
        result: Output grid starts as a copy of the input grid.
      - action: identify_seeds
        source: input_grid
        criteria: Pixel color is not white (0).
        result: List of seed_pixels (color, row, column).
      - action: apply_pattern
        for_each: seed_pixel in identified_seeds
        using: descending_alternating_pattern
        target: output_grid
        details: For each seed at (seed_row, seed_col) with color C, iterate rows r from seed_row + 1 to grid_height - 1. Apply pattern rules based on 'r' being odd or even, placing color C at calculated coordinates if within bounds.
    
    relationships:
      - Each seed_pixel independently generates a pattern in the output.
      - The output grid combines the initial state (input grid) and all generated patterns.
    ```


*   **Natural Language Program:**
    1.  Create the output grid as a copy of the input grid.
    2.  Identify all non-white pixels in the input grid. Call these "seed pixels".
    3.  For each seed pixel located at `(seed_row, seed_col)` with color `C`:
        a.  Iterate through all row indices `r` from `seed_row + 1` down to the last row index of the grid.
        b.  If the row index `r` is odd:
            i.  If the column `seed_col - 1` is within the grid's width boundaries, set the pixel at `(r, seed_col - 1)` in the output grid to color `C`.
            ii. If the column `seed_col + 1` is within the grid's width boundaries, set the pixel at `(r, seed_col + 1)` in the output grid to color `C`.
        c.  If the row index `r` is even:
            i.  If the column `seed_col` is within the grid's width boundaries (it always will be if the seed pixel was), set the pixel at `(r, seed_col)` in the output grid to color `C`.
    4.  The final modified grid is the result.