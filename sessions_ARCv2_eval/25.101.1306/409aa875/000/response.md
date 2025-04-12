**Perception of Task Elements:**

1.  **Grid Structure:** The task operates on 16x16 grids where each cell holds a color value (0-9). The background color is consistently orange (7).
2.  **Objects:** The inputs contain distinct shapes or patterns formed by non-orange pixels (maroon=9 in Ex1, white=0 in Ex2, red=2 in Ex3). These shapes are the primary actors.
3.  **Transformations:** The core transformation involves identifying these non-orange shapes and then modifying specific pixels in the output grid based on the shape's type, color, and location. The modifications often involve placing new pixels (maroon=9 or blue=1) at locations relative to the identified shapes, sometimes involving vertical projection or filling gaps. Some transformations seem global, triggered by the presence of certain shapes.
4.  **Color Mapping:** There appears to be a mapping from the input shape's color to the output modification color:
    *   Maroon (9) shape -> Blue (1) modification (Ex1)
    *   White (0) shape -> Maroon (9) modification (Ex2)
    *   Red (2) shape -> Maroon (9) modification (Ex3)
5.  **Shape-Specific Logic:** Different shapes trigger different rules:
    *   'V' shapes (3 pixels: top, bottom-left, bottom-right) trigger a vertical projection upwards. The distance of projection depends on the shape's row, and the specific V-shape might matter (e.g., centrality).
    *   'L' shapes (3 pixels: 2 horizontal, 1 vertical below the left one) trigger gap-filling between adjacent shapes (only for the topmost row of shapes) and a global pattern placement in specific rows/columns.

**YAML Fact Document:**


```yaml
task_context:
  grid_size: [16, 16]
  background_color: 7 # orange
  num_examples: 3

objects:
  - type: V-shape
    definition: 3 pixels (r, c), (r+1, c-1), (r+1, c+1) of the same non-orange color C.
    center: (r, c)
    observed_colors: [9, 0] # maroon, white
    examples: [train_1, train_2]
  - type: L-shape
    definition: 3 pixels (r, c), (r, c+1), (r+1, c) of the same non-orange color C.
    corner: (r, c)
    observed_colors: [2] # red
    examples: [train_3]

transformations:
  - rule: V-shape Projection
    input_trigger: V-shape of color C at center (r, c)
    conditions:
      - Applies if C is white(0).
      - Applies if C is maroon(9) AND the V-shape is closest to the grid's vertical center.
    actions:
      - Calculate offset k: k = 6 if r < 13 else k = 5.
      - Determine target coordinate: (r-k, c).
      - Determine output color C': C'=maroon(9) if C=white(0); C'=blue(1) if C=maroon(9).
      - Modify output grid at target coordinate with color C'.
    examples: [train_1, train_2]
  - rule: L-shape Global Pattern
    input_trigger: Presence of any red(2) L-shapes.
    actions:
      - Modify output grid at [(1,0), (1,3), (1,6), (1,9)] to maroon(9).
      - Modify output grid at [(9,0), (9,3), (9,6), (9,9)] to maroon(9).
    examples: [train_3]
  - rule: L-shape Gap Filling
    input_trigger: Pair of red(2) L-shapes L1, L2 in the same rows r, r+1 with corners (r, c1) and (r, c2) where c2 = c1 + 4.
    conditions:
      - The row r must be the minimum row containing any red(2) L-shape.
    actions:
      - Modify output grid at (r, c1+3) to maroon(9).
      - Modify output grid at (r+1, c1+3) to maroon(9).
    examples: [train_3]

relationships:
  - type: Relative Position
    description: Transformations depend on the row (r) of the input shape (determines projection offset k) or being the topmost shape (triggers gap filling). Centrality matters for maroon V-shapes. Adjacency matters for L-shape gap filling (c2 = c1 + 4).
  - type: Color Mapping
    input_color: 9 # maroon
    output_color: 1 # blue
    condition: V-shape, central
  - type: Color Mapping
    input_color: 0 # white
    output_color: 9 # maroon
    condition: V-shape
  - type: Color Mapping
    input_color: 2 # red
    output_color: 9 # maroon
    condition: L-shape triggers (both gap fill and global pattern)

```


**Natural Language Program:**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Find all V-shapes, defined as three pixels of the same non-orange color C arranged as `(r, c), (r+1, c-1), (r+1, c+1)`. Record their center `(r, c)` and color C.
3.  Find all red L-shapes, defined as three red (2) pixels arranged as `(r, c), (r, c+1), (r+1, c)`. Record their corner `(r, c)`.
4.  **Process V-shapes:**
    *   For each white (0) V-shape with center `(r, c)`: Calculate offset `k = 6` if `r < 13`, else `k = 5`. Change the pixel at `(r-k, c)` in the output grid to maroon (9).
    *   For each maroon (9) V-shape with center `(r, c)`: Check if its column `c` is closest to the grid's vertical centerline (columns 7 or 8). If it is the closest, calculate offset `k = 6` if `r < 13`, else `k = 5`. Change the pixel at `(r-k, c)` in the output grid to blue (1).
5.  **Process Red L-shapes:**
    *   If any red (2) L-shapes were found:
        *   Change the output grid pixels at `(1, 0), (1, 3), (1, 6), (1, 9)` to maroon (9).
        *   Change the output grid pixels at `(9, 0), (9, 3), (9, 6), (9, 9)` to maroon (9).
        *   Find the minimum row `min_r` among all found red L-shape corners.
        *   Identify pairs of red L-shapes whose corners are at `(min_r, c1)` and `(min_r, c2)` where `c2 = c1 + 4`.
        *   For each such pair, change the output grid pixels at `(min_r, c1+3)` and `(min_r+1, c1+3)` to maroon (9).