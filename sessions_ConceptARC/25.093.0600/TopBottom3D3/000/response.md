*   **Perception:** The task involves transforming a 2D grid of colored cells. The input grids contain distinct regions of non-zero colors, typically with one color region partially or fully surrounding another. The transformation replaces the "inner" color with the "outer" color, effectively filling the inner region with the color of the surrounding region. The background color (0) remains unchanged. The key is identifying which non-zero color is "inner" (doesn't touch the background) and which is "outer" (touches the background).

*   **YAML Facts:**
    
```yaml
    objects:
      - grid:
          description: A 2D array of integer values representing colors.
          properties:
            - dimensions: rows and columns.
            - cells: individual elements with color values.
      - cell:
          description: An element within the grid at a specific row and column.
          properties:
            - coordinates: (row, column).
            - color: integer value.
      - color_region:
          description: A connected area of cells sharing the same non-zero color.
          properties:
            - color_value: The integer color of the region.
            - touches_background: Boolean flag indicating if any cell in the region is adjacent (up, down, left, right) to a cell with color 0.
    relationships:
      - adjacency: Cells can be adjacent horizontally or vertically.
      - containment: One color region might border or surround another.
    actions:
      - identify_colors: Find all unique non-zero colors in the input grid.
      - check_background_adjacency: For each non-zero color, determine if any cell of that color is adjacent to a background cell (color 0).
      - classify_colors:
          - inner_color: The non-zero color that does NOT touch the background (0).
          - outer_color: The non-zero color that DOES touch the background (0).
      - transform_grid: Create the output grid by replacing all cells with the inner_color with the outer_color, keeping all other cells (outer_color and background) the same.
    ```


*   **Natural Language Program:**
    1.  Identify all unique non-zero integer values (colors) present in the input grid.
    2.  For each unique non-zero color, determine if any cell containing this color is directly adjacent (horizontally or vertically) to a cell with the value 0 (background).
    3.  Designate the unique non-zero color whose cells are *never* adjacent to the background (0) as the `inner_color`.
    4.  Designate the unique non-zero color whose cells *are* adjacent to the background (0) as the `outer_color`.
    5.  Construct the output grid by iterating through each cell of the input grid:
        *   If the input cell's color is the `inner_color`, set the corresponding output cell's color to the `outer_color`.
        *   Otherwise (if the input cell's color is the `outer_color` or 0), keep the original color for the corresponding output cell.