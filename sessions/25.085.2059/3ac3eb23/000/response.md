*   **Perception:**
    *   The task involves taking an input grid and producing an output grid of the same dimensions.
    *   The input grids contain a few non-`white` pixels, typically in the top row, on a `white` background.
    *   The output grids retain the original non-`white` pixels and add more pixels of the same colors below them.
    *   Each non-`white` pixel in the input seems to generate a vertical pattern extending downwards.
    *   The pattern generated below a pixel at `(r, c)` with color `C` alternates between adding two pixels of color `C` at `(r+k, c-1)` and `(r+k, c+1)` when `k` is odd, and adding one pixel of color `C` at `(r+k, c)` when `k` is even and positive.
    *   This pattern generation continues until the bottom edge of the grid is reached.
    *   Pixels are only added within the grid boundaries. If a generated position `(r', c')` falls outside the columns (i.e., `c' < 0` or `c' >= width`), that pixel is not added.
    *   Multiple source pixels in the input generate their patterns independently, potentially overlapping but without changing each other's color.

*   **Facts:**
    
```yaml
    task_type: pattern_generation
    grid_properties:
      - dimensions: preserved between input and output
      - background_color: white (0)
    objects:
      - type: pixel
        properties:
          - color: non-white colors (1-9) act as seeds
          - position: (row, column)
    actions:
      - name: identify_seeds
        input: input_grid
        output: list of non-white pixel coordinates and colors
      - name: generate_pattern
        input: seed_pixel (color C, position (r, c)), grid_dimensions (height, width)
        output: set of new pixel coordinates and their color (C)
        details: |
          For each row i from r+1 to height-1:
          Let k = i - r.
          If k is odd:
            Generate potential pixels at (i, c-1) and (i, c+1).
          If k is even:
            Generate potential pixel at (i, c).
          Filter generated pixels to keep only those within column boundaries (0 <= col < width).
          All generated pixels have color C.
      - name: combine_patterns
        input: input_grid, set of all generated pixels
        output: output_grid
        details: Start with a copy of the input grid. Add (overwrite) the generated pixels onto this grid.
    relationships:
      - type: spatial
        description: The generated pattern originates below each seed pixel and extends downwards.
      - type: dependency
        description: The color of the generated pattern depends entirely on the color of the seed pixel.
      - type: structural
        description: The pattern alternates structure based on the row distance (odd/even) from the seed pixel.
    ```


*   **Natural Language Program:**
    1.  Create the output grid as an exact copy of the input grid.
    2.  Find all non-`white` pixels in the input grid. Call these "seed pixels".
    3.  For each seed pixel with color `C` located at row `r` and column `c`:
        a.  Iterate through all rows `i` below the seed pixel's row (`i` from `r + 1` to the last row index).
        b.  Calculate the vertical distance `k = i - r`.
        c.  If `k` is an odd number:
            i.  If the column `c - 1` is within the grid's width boundaries, change the pixel at `(i, c - 1)` in the output grid to color `C`.
            ii. If the column `c + 1` is within the grid's width boundaries, change the pixel at `(i, c + 1)` in the output grid to color `C`.
        d.  If `k` is an even number:
            i.  Change the pixel at `(i, c)` in the output grid to color `C`. (The column `c` is guaranteed to be within bounds if the seed was).
    4.  Return the modified output grid.