Okay, let's analyze the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** All examples use a 10x10 grid.
2.  **Colors:** The primary colors involved are white (0 - background), gray (5), and various other colors (blue=1, red=2, green=3, yellow=4, magenta=6, orange=7, maroon=9).
3.  **Key Objects:**
    *   **Gray Lines/Segments (Color 5):** These appear as solid horizontal or vertical lines or segments. They seem to act as boundaries or triggers for the transformation. They remain unchanged in the output.
    *   **Colored Patterns:** These are non-white, non-gray pixels that appear adjacent (immediately below or immediately to the right) to the gray segments. These patterns are the "source" for the transformation.
    *   **White Space (Color 0):** This is the background color that gets filled during the transformation.
4.  **Transformation Actions:** The core action is the propagation or "tiling" of the colored patterns into adjacent white space. The direction and manner of propagation depend on the orientation of the adjacent gray line segment.
    *   **Horizontal Propagation:** If a colored pattern (a column of pixels) is immediately below a horizontal gray segment, each pixel's color in that column is extended horizontally to the right, filling the white space in its respective row, up to the end of the gray segment above it. (Seen in train_1, train_3 right side).
    *   **Vertical Propagation:** If a colored pattern (one or more rows of pixels) is immediately to the right of a vertical gray segment, this block of rows is tiled vertically upwards, filling the white space, repeating the pattern block until it reaches the top boundary defined by the vertical gray segment. (Seen in train_2, train_3 left side, train_4).
5.  **Boundaries:** The propagation seems strictly bounded by the extent of the adjacent gray line segment. Propagation only overwrites white pixels.

**YAML Facts:**


```yaml
task_description: Propagate colored patterns adjacent to gray lines into white space. The direction and method of propagation depend on the orientation of the gray line relative to the pattern.

elements:
  - element: grid
    description: A 2D array of pixels with values 0-9 representing colors. Size is typically 10x10 in examples.
  - element: pixel
    description: A single cell in the grid with a color value.
    properties:
      - color: white (0), blue (1), red (2), green (3), yellow (4), gray (5), magenta (6), orange (7), azure (8), maroon (9)
      - position: (row, column) coordinates
  - element: gray_segment
    description: A contiguous line of gray (5) pixels, either horizontal or vertical.
    properties:
      - orientation: horizontal or vertical
      - start_pos: (row, col) of one end
      - end_pos: (row, col) of the other end
    role: Acts as a boundary and a trigger for propagation. Remains unchanged.
  - element: colored_pattern
    description: A contiguous block (pixel, column, row, or rectangle) of non-white, non-gray pixels located immediately adjacent (below or right) to a gray segment.
    properties:
      - colors: The specific colors within the pattern.
      - shape: The arrangement of pixels (e.g., vertical column, horizontal row(s)).
      - location: Position relative to an adjacent gray segment.
    role: Acts as the source material for propagation.
  - element: white_space
    description: Pixels with the background color white (0).
    role: The target area to be filled by propagation.

actions:
  - action: identify_gray_segments
    description: Locate all horizontal and vertical contiguous segments of gray pixels.
  - action: identify_source_patterns
    description: For each gray segment, find any non-white, non-gray pixels immediately below (for horizontal segments) or immediately to the right (for vertical segments). Group these adjacent pixels into pattern blocks (columns for horizontal, rows for vertical).
  - action: propagate_horizontally
    description: For each source pixel (r, c) found below a horizontal gray segment ending at column c_end, fill the white pixels (r, k) with the source pixel's color for c < k <= c_end.
    triggered_by: Horizontal gray segment and colored pixel(s) immediately below it.
    target: White pixels in the same row, to the right, bounded by the gray segment's extent.
  - action: propagate_vertically
    description: For a source pattern block (rows r_s_top to r_s_bot) found to the right of a vertical gray segment (rows r_top to r_bot), tile/repeat this block upwards into the white space in the same columns, filling rows r_top to r_s_top - 1. The tiling repeats the source block pattern cyclically from bottom to top.
    triggered_by: Vertical gray segment and colored row(s) immediately to its right.
    target: White pixels in the same columns, above the source pattern, bounded by the gray segment's extent.

relationships:
  - relationship: adjacency
    description: Key relationship is between gray segments and colored patterns (non-diagonal adjacency - below or right). Also relevant for defining contiguous segments.
  - relationship: bounding
    description: Gray segments define the boundaries (spatial extent) for the propagation originating from adjacent colored patterns.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all maximal contiguous horizontal segments of gray (5) pixels.
3.  For each horizontal gray segment spanning columns `c_start` to `c_end` at row `r_gray`:
    a.  Look for non-white, non-gray pixels in the row immediately below (`r_gray + 1`) within the same columns (`c_start` to `c_end`).
    b.  For each such source pixel found at `(r_gray + 1, c_source)` with color `C`:
        i.  Iterate through columns `k` from `c_source + 1` to `c_end`.
        ii. If the pixel `(r_gray + 1, k)` in the output grid is white (0), change its color to `C`.
4.  Identify all maximal contiguous vertical segments of gray (5) pixels.
5.  For each vertical gray segment spanning rows `r_top` to `r_bottom` at column `c_gray`:
    a.  Look for non-white, non-gray pixels in the column immediately to the right (`c_gray + 1`) within the same rows (`r_top` to `r_bottom`).
    b.  If such pixels exist, identify the block of contiguous source rows (`r_source_top` to `r_source_bottom`) and columns (`c_source_left` to `c_source_right`) forming the pattern adjacent to the gray segment.
    c.  Determine the height of this source pattern block: `pattern_height = r_source_bottom - r_source_top + 1`.
    d.  Iterate upwards through the target rows `r_target` from `r_source_top - 1` down to `r_top`.
    e.  For each target row `r_target`, determine the corresponding source row `r_source` within the pattern block using modular arithmetic based on the distance from the bottom of the source block: `r_source = r_source_bottom - ((r_source_bottom - r_target) % pattern_height)`.
    f.  Iterate through the columns `c` from `c_source_left` to `c_source_right`.
    g.  If the pixel `(r_target, c)` in the output grid is white (0), change its color to the color of the pixel `(r_source, c)` in the original input grid's pattern block.
6.  Return the modified output grid.