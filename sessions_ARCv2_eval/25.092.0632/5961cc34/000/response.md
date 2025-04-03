*   **Perception:** The task involves transforming input grids containing various colored objects into output grids. The input grids feature a consistent background color (azure, 8). There are distinct objects primarily composed of blue (1) and green (3) pixels, which seem to define key shapes or patterns ("pattern objects"). Additionally, near the bottom of the input grids, there are marker pixels: a single yellow (4) pixel and one or more red (2) pixels directly below it in the same column. The output grids consist solely of the azure background and red (2) pixels forming specific shapes. The transformation logic appears to depend on the number of distinct "pattern objects" found in the input.

*   **YAML Facts:**
    
```yaml
    task_context:
      background_color: 8 (azure)
      output_color: 2 (red)
      pattern_colors: [1 (blue), 3 (green)]
      marker_colors: [4 (yellow), 2 (red)]
      grid_dimensions: variable

    observations:
      - element: pattern_objects
        description: Connected components composed of pattern_colors (blue or green). Considered connected if pixels share an edge (not diagonal). Blue and Green pixels connect to each other.
        properties:
          - count: The number of distinct pattern_objects in the input grid.
          - bounding_box: The smallest rectangle enclosing all pixels of a single pattern_object.
        relationship: The transformation rule depends on the 'count' property.

      - element: marker_objects
        description: A vertical structure near the bottom, consisting of a single yellow (4) pixel with one or more red (2) pixels directly below it in the same column.
        properties:
          - column_index: The column where the marker_objects reside.
          - target_color: The color of the red pixels in the marker (always red, 2).
        relationship: Used only when the count of pattern_objects is exactly 1 to determine the output column. Implicitly confirms the output color is red (2).

      - element: output_grid
        description: The result of the transformation.
        properties:
          - dimensions: Same as the input grid.
          - background: Same as input background (azure, 8).
          - foreground: Pixels colored with the target_color (red, 2).
        relationship:
          - If pattern_object count is 1: Foreground is a single vertical line of red (2) spanning the full height of the grid in the column specified by marker_objects.column_index.
          - If pattern_object count is > 1: Foreground is the union of the bounding_boxes of all pattern_objects, filled with red (2).

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, then change all non-background (non-azure) pixels to the background color (azure, 8).
    2.  Identify all distinct connected components where connectivity includes pixels colored blue (1) or green (3). Treat blue and green pixels equivalently for finding components. Count these components ("pattern objects").
    3.  **If** the number of pattern objects is exactly 1:
        a.  Find the column index containing the yellow (4) marker pixel.
        b.  Fill the entire identified column in the output grid with red (2).
    4.  **Else if** the number of pattern objects is greater than 1:
        a.  For each identified pattern object, determine its minimum bounding box (minimum row, minimum column, maximum row, maximum column).
        b.  Iterate through all cells within the union of these bounding boxes. For each cell (row, col) that falls within *any* of the calculated bounding boxes, set the corresponding cell in the output grid to red (2).
    5.  Return the final output grid.