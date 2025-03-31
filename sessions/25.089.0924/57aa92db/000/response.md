*   **Perception:**
    *   The task involves modifying an input grid based on local interactions between pixels of different colors.
    *   The input grids contain multiple distinct "objects" composed of contiguous non-white pixels. Some objects are single-colored, while others are composed of two different non-white colors.
    *   The transformation only affects objects composed of exactly two different non-white colors. Single-color objects remain unchanged.
    *   Within a two-colored object, one color acts as an "expander" and the other as a "target" or "center".
    *   The transformation rule appears to be based on the relative numerical value (color index) of the two adjacent colors within an object. The color with the higher index value expands.
    *   The expansion fills the 3x3 area centered on each pixel of the target (lower index) color. Specifically, any white (0) pixel within this 3x3 area is changed to the expander (higher index) color.
    *   The original pixels of both the expander and target colors remain unchanged.
    *   The expansion happens simultaneously for all target pixels associated with a given expander color within an object.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    element_type: pixels
    background_color: 0 (white)
    objects:
      - type: contiguous_pixels
        properties:
          - color (non-zero)
          - shape
          - adjacency
      - composition:
          - single_color: These objects are ignored by the transformation.
          - two_color: These objects are subject to transformation.
    relationships:
      - adjacency: Cardinal (N, S, E, W) adjacency between pixels of different non-white colors within the same object triggers the transformation. Diagonal adjacency is not considered for triggering.
      - comparison: Numerical comparison between the color indices of adjacent, different non-white colors.
    actions:
      - identify_objects: Find connected components of non-white pixels.
      - identify_two_color_objects: Filter for objects containing exactly two distinct non-white colors.
      - identify_expander_target_pairs: For each two-color object, find adjacent pairs of the two colors. The color with the higher index is the 'expander' (Color A), the one with the lower index is the 'target' (Color B).
      - perform_expansion:
          - for each pixel of Color B that is adjacent to Color A:
              - define a 3x3 neighborhood centered on the Color B pixel.
              - for each pixel within this 3x3 neighborhood:
                  - if the pixel is currently white (0):
                      - change its color to Color A.
    constraints:
      - Original non-white pixels are preserved.
      - Expansion only fills white pixels.
      - Expansion uses the 3x3 neighborhood (Moore neighborhood) including diagonals relative to the target center.
      - The trigger requires direct cardinal adjacency between the two colors.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Iterate through each cell `(r, c)` of the input grid.
    3.  Let `Color B` be the color of the cell `input_grid[r, c]`.
    4.  If `Color B` is white (0), skip to the next cell.
    5.  Check the four cardinal neighbors (up, down, left, right) of the cell `(r, c)`.
    6.  For each neighbor `(nr, nc)`:
        a.  Let `Color A` be the color of the cell `input_grid[nr, nc]`.
        b.  If `Color A` is not white (0) and `Color A` is different from `Color B` and the numerical value of `Color A` is greater than the numerical value of `Color B`:
            i.  This means `Color B` at `(r, c)` is a "target" pixel, and `Color A` is its corresponding "expander" color.
            ii. Consider the 3x3 neighborhood centered at `(r, c)`.
            iii. For each cell `(tr, tc)` within this 3x3 neighborhood (from `r-1, c-1` to `r+1, c+1`):
                1.  Check if the cell `(tr, tc)` is within the grid boundaries.
                2.  If the cell `input_grid[tr, tc]` is white (0):
                    *   Update the cell `output_grid[tr, tc]` to `Color A`. (Note: It's important to apply updates based on the original input state but modify the output grid. If multiple expansions target the same white cell, they should all result in the same color based on the examples, so simple overwriting is sufficient).
    7.  Return the modified output grid.