*   **Perception:**
    The task involves identifying and removing "noise" pixels from a grid that has a dominant background pattern organized either by rows or by columns. The noise pixels are replaced by the most common color found within their respective row or column, depending on the overall pattern orientation.

    *   In `train_1`, the input grid shows horizontal stripes (yellow and green rows) with some magenta pixels interspersed, primarily within the green rows but also one in a yellow row. The output grid replaces these magenta pixels with the dominant color of the row they belong to (green for green rows, yellow for the yellow row). The dominant pattern is row-based.
    *   In `train_2`, the input grid shows vertical stripes (orange and red columns) with some gray pixels interspersed. The output grid replaces these gray pixels with the dominant color of the column they belong to (orange for orange columns, red for red columns). The dominant pattern is column-based.

    The core logic seems to be:
    1.  Determine whether the grid's primary structure is row-based or column-based by comparing the color homogeneity within rows versus columns.
    2.  Identify the "noise" pixels, which are those whose color does not match the majority color of their respective row (if row-based) or column (if column-based).
    3.  Replace each noise pixel with the majority color of its row or column, according to the determined orientation.

*   **Facts:**
    
```yaml
    task_type: cleanup_noise
    input_features:
      - grid: 2D array of integers (colors)
      - patterns:
          - dominant_orientation: Either 'row' or 'column' based on color homogeneity.
          - background_colors: The colors forming the primary row or column patterns.
          - noise_pixels: Pixels whose color differs from the majority color of their respective row/column (depending on orientation).
    output_features:
      - grid: Same dimensions as input.
      - changes: Noise pixels are replaced.
      - replacement_rule: Noise pixel at (r, c) is replaced by the majority color of row 'r' if orientation is 'row', or by the majority color of column 'c' if orientation is 'column'.
    relationships:
      - homogeneity_determines_orientation: The orientation with higher color concentration (sum of majority counts) dictates the processing axis (rows or columns).
      - noise_replacement: The replacement color for a noise pixel is determined by the majority color along the processing axis it belongs to.
    examples:
      - train_1:
          orientation: row (row homogeneity > column homogeneity)
          noise_color: magenta (6)
          action: Replace magenta pixels with the majority color of their respective row (yellow or green).
      - train_2:
          orientation: column (column homogeneity > row homogeneity)
          noise_color: gray (5)
          action: Replace gray pixels with the majority color of their respective column (orange or red).
    ```


*   **Natural Language Program:**
    1.  Determine the primary orientation of the grid pattern:
        a.  Calculate a 'row homogeneity score' by summing, for each row, the count of the most frequent color in that row.
        b.  Calculate a 'column homogeneity score' by summing, for each column, the count of the most frequent color in that column.
        c.  Compare the scores. If the row score is greater than or equal to the column score, the orientation is 'row'. Otherwise, the orientation is 'column'.
    2.  Create a copy of the input grid to serve as the output grid.
    3.  If the orientation is 'row':
        a.  For each row in the grid:
            i.  Identify the majority color for that row.
            ii. For each cell in that row:
                *   If the cell's color in the input grid is *not* the row's majority color, update the cell's color in the output grid to be the row's majority color.
    4.  If the orientation is 'column':
        a.  For each column in the grid:
            i.  Identify the majority color for that column.
            ii. For each cell in that column:
                *   If the cell's color in the input grid is *not* the column's majority color, update the cell's color in the output grid to be the column's majority color.
    5.  Return the modified output grid.