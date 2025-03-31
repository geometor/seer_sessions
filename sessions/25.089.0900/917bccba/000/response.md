Okay, let's analyze the provided examples for this ARC task.

## Perception of Task Elements

1.  **Grid Structure:** All examples use a 12x12 grid. The background is consistently white (0).
2.  **Colors:** Each example uses exactly two non-background colors. Let's call them C1 and C2.
    *   Train 1: C1=Blue(1), C2=Azure(8)
    *   Train 2: C1=Red(2), C2=Green(3)
    *   Train 3: C1=Green(3), C2=Yellow(4)
3.  **Objects/Shapes:**
    *   There's a central H-like or I-like structure composed of both C1 and C2. C1 forms the main "posts" and parts of the crossbar, while C2 forms a central vertical line segment within the structure and part of the crossbar.
    *   There are vertical lines composed solely of C2 located outside the central structure, aligned vertically with the C2 segment inside the structure.
    *   In train 1 and 3, the crossbar of the H-shape also extends horizontally beyond the main structure using color C2. In train 2, it seems C2 also forms the ends of the crossbar.
4.  **Transformation Pattern:**
    *   **Internal C2 Removal:** The C2 pixels forming the vertical segment *inside* the H-structure are removed (changed to white 0).
    *   **External C2 Line Movement:** The vertical lines of C2 outside the structure are moved horizontally. They appear to move to the column corresponding to the rightmost edge of the H-structure. The original column of these lines is cleared (changed to white 0).
    *   **Crossbar Transformation:** The horizontal crossbar undergoes a significant change. The segment of the crossbar *between* (and including) the C1 vertical posts of the H-structure is changed entirely to color C1. The parts of the crossbar extending *outside* these C1 posts retain their original color (which is C2).

## YAML Fact Sheet


```yaml
task_context:
  grid_size: [12, 12]
  background_color: 0 # white
  num_distinct_colors_per_example: 3 # background + 2 foreground colors

objects:
  - id: H_structure
    description: A central H-like shape composed of two colors, C1 and C2.
    properties:
      color_1: C1 # Forms vertical posts and part of the crossbar
      color_2: C2 # Forms internal vertical line and part of the crossbar
      bounding_box: Defines the spatial extent.
      crossbar_row: The row index containing the horizontal bar.
      left_post_col: Column index of the leftmost C1 segment defining the H structure on the crossbar row.
      right_post_col: Column index of the rightmost C1 segment defining the H structure on the crossbar row.
      right_edge_col: Column index of the rightmost extent of the H structure's bounding box.

  - id: external_lines
    description: Vertical lines outside the H_structure, composed solely of C2.
    properties:
      color: C2
      column_index: The original column where these lines appear.
      vertical_extent: The rows these lines occupy.

relationships:
  - C2 is present both inside the H_structure (vertical line, crossbar) and as external_lines.
  - external_lines are vertically aligned with the internal C2 vertical line segment.

actions:
  - action: clear_internal_vertical_C2
    object: H_structure
    details: Change pixels of color C2 within the H_structure's bounding box to background_color (0), *except* for those on the crossbar_row.
  - action: modify_crossbar
    object: H_structure
    details: >
      Iterate through the crossbar_row. For columns between left_post_col and right_post_col (inclusive),
      change the pixel color to C1. Pixels outside this column range retain their original color.
  - action: move_external_lines
    object: external_lines
    details: >
      Change the original external_lines pixels to background_color (0).
      Draw new vertical lines of color C2 at the column index defined by H_structure.right_edge_col,
      maintaining the original vertical_extent.

```


## Natural Language Program

1.  Identify the background color (white, 0) and the two foreground colors, C1 and C2. C2 is distinguishable as the color appearing both within the central structure's vertical axis and as separate external vertical lines. C1 forms the main 'posts' of the central H-like structure.
2.  Locate the central H-like structure composed of C1 and C2. Determine its bounding box, the row index of its horizontal crossbar (`crossbar_row`), the column index of the leftmost C1 pixel on the crossbar (`left_post_col`), the column index of the rightmost C1 pixel on the crossbar (`right_post_col`), and the column index of the overall rightmost extent of the structure (`right_edge_col`).
3.  Locate the external vertical lines composed solely of C2. Note their original column index (`external_line_col`) and their row indices (`external_line_rows`).
4.  Initialize the output grid as a copy of the input grid.
5.  Iterate through the input grid pixels *within* the H-structure's bounding box: If a pixel's color is C2 and its row index is *not* `crossbar_row`, change the corresponding pixel in the output grid to the background color (0).
6.  Iterate through the `external_line_rows`: Change the pixel at (`row`, `external_line_col`) in the output grid to the background color (0). Then, change the pixel at (`row`, `right_edge_col`) in the output grid to C2.
7.  Iterate through the columns (`c`) of the `crossbar_row` in the output grid:
    *   If `c` is between `left_post_col` and `right_post_col` (inclusive), set the pixel color at (`crossbar_row`, `c`) to C1.
    *   Otherwise (if `c` is less than `left_post_col` or greater than `right_post_col`), the pixel at (`crossbar_row`, `c`) retains its original color from the input grid.
8.  Return the modified output grid.