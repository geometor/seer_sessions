**General Assessment**

The initial code successfully solved the first training example (`train_1`) but failed on the second (`train_2`). The failure occurred because the logic for vertical filling was incorrect. In `train_2`, the orange seed pixels were located *below* the vertical span of the main yellow boundary structure. The original code filled both upwards and downwards from these seeds, incorrectly coloring a pixel below one of the seeds.

The key insight derived from analyzing `train_2` is that the fill directionality is relative to the main boundary structure.
*   If a seed's row is *within* the boundary's row span, the fill proceeds horizontally outwards (left and right) until the boundary is hit.
*   If a seed's row is *outside* the boundary's row span, the fill proceeds vertically *only towards* the boundary's row span until the boundary is hit. That is, if the seed is below the boundary rows, fill only upwards; if the seed is above, fill only downwards.

The stopping condition remains the same: the fill stops upon encountering a pixel that is part of the largest connected component of yellow pixels (the main boundary) or the grid edge. Other yellow pixels not part of this main component do not stop the fill.

**Metrics**

Metrics gathered for the examples:

*   **`train_1`**:
    *   Grid Shape: 10x10
    *   Main Yellow Boundary: Size=28, Row Span=[2, 8]
    *   Seed Coordinates: [(5, 0)]
    *   Seed (5, 0): Row 5 is within [2, 8] -> Horizontal Fill.

*   **`train_2`**:
    *   Grid Shape: 12x14
    *   Main Yellow Boundary: Size=27, Row Span=[1, 8] (Note: the internal yellow line at row 8, cols 4-8 is *not* part of the largest component).
    *   Seed Coordinates: [(10, 3), (11, 9)]
    *   Seed (10, 3): Row 10 > 8 -> Vertical Fill, Position=Below. Fill direction should be UP only.
    *   Seed (11, 9): Row 11 > 8 -> Vertical Fill, Position=Below. Fill direction should be UP only.

**Facts YAML**


```yaml
elements:
  - color: 0
    name: white
    role: background
    property: fillable_area
  - color: 4
    name: yellow
    role: boundary_structure
    property: static
    observation: Forms shapes. The largest connected component acts as the primary boundary for fills. Other yellow pixels are ignored by the fill process.
  - color: 7
    name: orange
    role: seed_and_fill
    property: dynamic
    observation: Initiates filling process. Final fill color.

grid_properties:
  - size: variable height and width

transformation:
  - name: directional_ray_cast_fill
    input_elements:
      - seed_pixels (orange)
      - boundary_structure_pixels (yellow)
      - background (white)
    output_elements:
      - filled_pixels (orange)
      - original_boundary_structure (yellow)
      - remaining_background (white)
    process:
      - step: Create a copy of the input grid for the output.
      - step: Identify all yellow (4) pixels. Determine the largest connected component (using 4-way adjacency) - this is the 'main boundary'. Store the coordinates of these main boundary pixels.
      - step: If a main boundary exists, calculate its minimum and maximum row indices (`min_row`, `max_row`). If no boundary exists, treat as if fill is unbounded (or handle as error/edge case if necessary, though examples suggest boundary exists).
      - step: Identify all orange (7) 'seed' pixels in the input grid.
      - step: For each seed pixel at (r, c):
          - determine_fill_behavior:
              - Check if a main boundary exists and if the seed row `r` is within its span: `min_row <= r <= max_row`.
              - If YES (Horizontal Fill Case):
                  - Ray cast left from `(r, c-1)`: Fill white (0) pixels in the *output grid* with orange (7) until a main boundary pixel or grid edge is hit at column `j`.
                  - Ray cast right from `(r, c+1)`: Fill white (0) pixels in the *output grid* with orange (7) until a main boundary pixel or grid edge is hit at column `j`.
              - If NO (Vertical Fill Case):
                  - If `r < min_row` (seed is above boundary): Ray cast *downwards* from `(r+1, c)`. Fill white (0) pixels in the *output grid* with orange (7) until a main boundary pixel or grid edge is hit at row `i`.
                  - If `r > max_row` (seed is below boundary): Ray cast *upwards* from `(r-1, c)`. Fill white (0) pixels in the *output grid* with orange (7) until a main boundary pixel or grid edge is hit at row `i`.
                  - (Implicit: If no boundary exists, this case might default to vertical fill in both directions, or requires specific handling).
          - Ensure the seed pixel location `(r, c)` itself is orange (7) in the output grid.
    notes: The fill process checks against the original input grid's state for white pixels but writes to the output grid. The stopping condition depends only on the coordinates identified as belonging to the *largest* yellow component. Fill proceeds along a straight line (row or column).
```


**Natural Language Program**

1.  Create an identical copy of the input grid to serve as the working output grid.
2.  Find all yellow (4) pixels in the input grid. Identify the coordinates of the pixels belonging to the largest connected component of these yellow pixels (using 4-way adjacency). These coordinates define the 'main boundary'.
3.  If a main boundary was found, determine its minimum and maximum row index (`min_boundary_row`, `max_boundary_row`). If no main boundary exists, handle appropriately (e.g., proceed without boundary checks, though unlikely based on examples).
4.  Find the coordinates `(r, c)` of all orange (7) 'seed' pixels in the input grid.
5.  For each seed pixel at `(r, c)`:
    a.  Set the pixel `(r, c)` in the *output grid* to orange (7).
    b.  Check if a main boundary exists and if the seed's row `r` is within the boundary's span: `min_boundary_row <= r <= max_boundary_row`.
    c.  **If the seed row `r` is within the boundary span (Horizontal Fill):**
        i.  **Fill Left:** Iterate column index `j` from `c-1` down to 0. If the pixel `(r, j)` is part of the main boundary coordinates, stop filling left. If the pixel `(r, j)` in the *input grid* is white (0), change the pixel `(r, j)` in the *output grid* to orange (7). Otherwise (non-white, non-boundary), continue checking the next pixel to the left.
        ii. **Fill Right:** Iterate column index `j` from `c+1` up to `width-1`. If the pixel `(r, j)` is part of the main boundary coordinates, stop filling right. If the pixel `(r, j)` in the *input grid* is white (0), change the pixel `(r, j)` in the *output grid* to orange (7). Otherwise, continue checking the next pixel to the right.
    d.  **If the seed row `r` is outside the boundary span (Vertical Fill):**
        i.  **If `r < min_boundary_row` (Seed Above Boundary):** Fill *only downwards*. Iterate row index `i` from `r+1` up to `height-1`. If the pixel `(i, c)` is part of the main boundary coordinates, stop filling down. If the pixel `(i, c)` in the *input grid* is white (0), change the pixel `(i, c)` in the *output grid* to orange (7). Otherwise, continue checking the next pixel down.
        ii. **If `r > max_boundary_row` (Seed Below Boundary):** Fill *only upwards*. Iterate row index `i` from `r-1` down to 0. If the pixel `(i, c)` is part of the main boundary coordinates, stop filling up. If the pixel `(i, c)` in the *input grid* is white (0), change the pixel `(i, c)` in the *output grid* to orange (7). Otherwise, continue checking the next pixel up.
6.  Return the final output grid.