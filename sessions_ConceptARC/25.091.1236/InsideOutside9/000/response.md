*   **Perception**:
    The input grids contain a background of white (0), two parallel lines of red (2) pixels (either horizontal or vertical), and several scattered yellow (4) pixels. The output grid retains the red lines and the white background. The transformation rule focuses on the yellow pixels: only those yellow pixels located strictly *between* the two parallel red lines are kept in the output; all other yellow pixels (those outside the region bounded by the red lines, or on the lines themselves if they happened to overlap) are changed to white (0).

*   **Facts**:
    
```yaml
    objects:
      - type: grid
        properties:
          - background_color: white (0)
      - type: line
        properties:
          - color: red (2)
          - count: 2
          - orientation: parallel (either horizontal or vertical)
          - function: define a bounding region
      - type: pixel
        properties:
          - color: yellow (4)
          - role: candidates for removal
    relationships:
      - type: spatial
        description: Yellow pixels can be located inside, outside, or potentially on the red lines. The critical relationship is being 'between' the two red lines.
    actions:
      - action: identify
        target: red lines
        details: Determine their orientation (horizontal/vertical) and bounding indices (min/max row or column).
      - action: filter
        target: yellow pixels
        condition: Keep only yellow pixels whose row index (for horizontal lines) or column index (for vertical lines) is strictly between the indices of the two red lines.
      - action: replace
        target: yellow pixels failing the filter condition
        replacement: white (0)
        output: The final grid state.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all red (2) pixels in the input grid.
    3.  Determine if the red pixels form two distinct parallel lines (either all red pixels share the same two column indices, or they share the same two row indices).
    4.  If vertical red lines are found at columns `c1` and `c2` (where `c1 < c2`), iterate through all yellow (4) pixels in the input grid. If a yellow pixel at `(r, c)` has a column `c` such that `c <= c1` or `c >= c2`, change the corresponding pixel in the output grid to white (0).
    5.  If horizontal red lines are found at rows `r1` and `r2` (where `r1 < r2`), iterate through all yellow (4) pixels in the input grid. If a yellow pixel at `(r, c)` has a row `r` such that `r <= r1` or `r >= r2`, change the corresponding pixel in the output grid to white (0).
    6.  Leave all other pixels (red lines, white background, and yellow pixels strictly between the red lines) unchanged from their input values.
    7.  Return the modified output grid.