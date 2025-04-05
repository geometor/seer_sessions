*   **Perception of Task Elements:**
    *   The task operates on 2D grids of integers (colors).
    *   Each input grid contains multiple distinct non-zero integer values, representing different colored regions, plus a background color '0'.
    *   The '0' color typically forms an outer border around the non-zero colored regions.
    *   The transformation involves changing the color of some regions while leaving others (and the background) unchanged.
    *   Specifically, one non-zero color seems to "take over" or replace another non-zero color.
    *   The determining factor for which color replaces which appears related to proximity to the outer '0' border. The color that touches the '0' border persists and replaces the color(s) that do not touch the '0' border.

*   **YAML Documentation of Facts:**
    
```yaml
    task_elements:
      - object: Grid
        properties:
          - type: 2D array of integers
          - contains: Cells
          - has: background_color (usually 0)
          - has: non_zero_colors (set of integers > 0)
      - object: Cell
        properties:
          - position: (row, column)
          - value: integer (color)
      - object: ColorRegion
        properties:
          - color_value: integer > 0
          - cells: list of Cell objects with the same color_value
          - touches_background: boolean (indicates if any cell in the region is adjacent to a background_color cell)

    relationships:
      - type: adjacency
        between: Cell
        definition: Cells sharing an edge (up, down, left, right).
      - type: containment
        description: Grid contains Cells.
      - type: grouping
        description: Cells with the same non-zero value form a ColorRegion.

    actions:
      - action: identify_colors
        input: Input Grid
        output: Set of unique non-zero colors present.
      - action: identify_border_touching_color
        input: Input Grid, Set of non-zero colors
        process: For each non-zero color, check if any cell with that color is adjacent to a cell with the background color (0).
        output: The non-zero color that touches the background border. (Assumption: only one such color exists). Let's call this the 'replacement_color'.
      - action: identify_inner_colors
        input: Set of non-zero colors, replacement_color
        output: Set of non-zero colors that are not the replacement_color. Let's call these 'target_colors'.
      - action: replace_colors
        input: Input Grid, target_colors, replacement_color
        process: Create a copy of the Input Grid. Iterate through each cell. If a cell's color is in target_colors, change its value to replacement_color. Otherwise, keep the original value.
        output: Output Grid

    transformation_rule:
      goal: Modify the input grid based on color adjacency to the background border.
      steps:
        - Find all unique non-zero colors in the input grid.
        - Determine which non-zero color has at least one cell adjacent (up, down, left, right) to a cell with the background color (0). This is the 'replacement_color'.
        - Identify all other non-zero colors as 'target_colors'.
        - Create the output grid by replacing every cell containing a 'target_color' with the 'replacement_color'. Cells with the 'replacement_color' or the background color (0) remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the set of all unique non-zero integer values (colors) present in the input grid.
    3.  Find the specific non-zero color (`replacement_color`) for which at least one cell with this color is directly adjacent (sharing an edge) to a cell with the value 0 (background).
    4.  Identify the set of all other non-zero colors (`target_colors`) present in the input grid (i.e., all non-zero colors excluding the `replacement_color`).
    5.  Iterate through each cell of the input grid.
    6.  If the current cell's color is one of the `target_colors`, change the color of the corresponding cell in the output grid to the `replacement_color`.
    7.  If the current cell's color is the `replacement_color` or the background color (0), keep its color unchanged in the output grid.
    8.  Return the modified output grid.