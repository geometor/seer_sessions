Okay, I will analyze the provided examples to understand the transformation logic.

**Perception of Task Elements:**

1.  **Grid Structure:** Each input grid consists of a central area primarily filled with 'white' (0) pixels, bordered either on the top and bottom rows or on the left and right columns by a single, uniform color different from 'white'.
2.  **Border Colors:** The two borders in each example always have distinct colors.
    *   Example 1: Top border 'azure' (8), Bottom border 'green' (3).
    *   Example 2: Top border 'red' (2), Bottom border 'yellow' (4).
    *   Example 3: Left border 'green' (3), Right border 'yellow' (4).
3.  **Internal Elements:** Within the central 'white' area, there are scattered 'blue' (1) pixels.
4.  **Transformation:** The core transformation involves changing the color of certain 'white' (0) pixels that are directly adjacent (sharing an edge, not diagonally) to the 'blue' (1) pixels.
5.  **Color Change Logic:** The new color assigned to a 'white' pixel depends on its position relative to the adjacent 'blue' pixel and the colors of the borders.
    *   If the borders are top and bottom:
        *   A 'white' pixel directly *above* a 'blue' pixel changes to the color of the *top* border.
        *   A 'white' pixel directly *below* a 'blue' pixel changes to the color of the *bottom* border.
    *   If the borders are left and right:
        *   A 'white' pixel directly to the *left* of a 'blue' pixel changes to the color of the *left* border.
        *   A 'white' pixel directly to the *right* of a 'blue' pixel changes to the color of the *right* border.
6.  **Consistency:** The original 'blue' pixels and the border pixels remain unchanged in the output. Only specific adjacent 'white' pixels are modified.

**YAML Facts:**


```yaml
task_description: Change the color of white pixels adjacent to blue pixels based on the color of the corresponding border.

grid_properties:
  - bordered: true
  - border_type: exclusive (either horizontal top/bottom OR vertical left/right)
  - border_thickness: 1 pixel

objects:
  - object: border_1
    definition: The top row (if horizontal borders) or the left column (if vertical borders).
    properties:
      - color: uniform, non-white
      - role: color_source_1
  - object: border_2
    definition: The bottom row (if horizontal borders) or the right column (if vertical borders).
    properties:
      - color: uniform, non-white, different from border_1
      - role: color_source_2
  - object: trigger_pixel
    definition: Any pixel with the color 'blue' (value 1) located within the non-border area.
    properties:
      - color: blue (1)
      - role: trigger
  - object: target_pixel
    definition: Any pixel with the color 'white' (value 0) located within the non-border area.
    properties:
      - color: white (0)
      - role: potential_target

relationships:
  - relation: adjacency
    subject: target_pixel
    object: trigger_pixel
    details: Target pixel shares an edge (up, down, left, or right) with a trigger pixel.

actions:
  - action: identify_borders
    input: input_grid
    output: border_type (horizontal/vertical), border_color_1, border_color_2
  - action: find_triggers
    input: input_grid
    output: list_of_trigger_coordinates
  - action: apply_color_change
    condition: border_type is horizontal
    steps:
      - for each trigger_pixel at (row, col):
        - check pixel at (row-1, col):
          - if pixel exists and is white (0): change its color to border_color_1 (top border)
        - check pixel at (row+1, col):
          - if pixel exists and is white (0): change its color to border_color_2 (bottom border)
  - action: apply_color_change
    condition: border_type is vertical
    steps:
      - for each trigger_pixel at (row, col):
        - check pixel at (row, col-1):
          - if pixel exists and is white (0): change its color to border_color_1 (left border)
        - check pixel at (row, col+1):
          - if pixel exists and is white (0): change its color to border_color_2 (right border)
  - action: construct_output
    steps:
      - start with a copy of the input grid.
      - apply all determined color changes.
      - return the modified grid.

final_output:
  - type: grid
    content: The input grid modified according to the color change rules.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Determine if the input grid has horizontal borders (top and bottom rows are non-white and uniform) or vertical borders (left and right columns are non-white and uniform).
3.  If the borders are horizontal:
    a.  Identify the color of the top border (`color_top`) and the bottom border (`color_bottom`).
    b.  Iterate through each pixel `(r, c)` of the input grid, excluding the borders.
    c.  If the pixel `(r, c)` is 'blue' (1):
        i.  Check the pixel directly above at `(r-1, c)`. If it exists within the grid (not including the top border row) and is 'white' (0), change the corresponding pixel in the *output* grid at `(r-1, c)` to `color_top`.
        ii. Check the pixel directly below at `(r+1, c)`. If it exists within the grid (not including the bottom border row) and is 'white' (0), change the corresponding pixel in the *output* grid at `(r+1, c)` to `color_bottom`.
4.  If the borders are vertical:
    a.  Identify the color of the left border (`color_left`) and the right border (`color_right`).
    b.  Iterate through each pixel `(r, c)` of the input grid, excluding the borders.
    c.  If the pixel `(r, c)` is 'blue' (1):
        i.  Check the pixel directly to the left at `(r, c-1)`. If it exists within the grid (not including the left border column) and is 'white' (0), change the corresponding pixel in the *output* grid at `(r, c-1)` to `color_left`.
        ii. Check the pixel directly to the right at `(r, c+1)`. If it exists within the grid (not including the right border column) and is 'white' (0), change the corresponding pixel in the *output* grid at `(r, c+1)` to `color_right`.
5.  Return the modified output grid.