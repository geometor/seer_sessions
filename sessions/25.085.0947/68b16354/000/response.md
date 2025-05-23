*   **Perception:**
    *   All examples show an input grid and an output grid of the same dimensions.
    *   Comparing the input and output grids, the content appears identical, but the arrangement is different.
    *   Specifically, the rows seem to be reordered.
    *   In `train_1`, the top row `[7, 3, 3, 1, 2]` of the input becomes the bottom row of the output. The bottom row `[8, 1, 7, 7, 1]` of the input becomes the top row of the output. The middle row `[2, 7, 8, 7, 2]` remains in the middle. This suggests a vertical flip or reflection across the horizontal midline.
    *   This pattern holds true for `train_2` and `train_3` as well. The order of the rows is completely reversed.

*   **Facts:**
    
```yaml
    task: grid_transformation
    examples:
      - id: train_1
        input_grid:
          dimensions: 5x5
        output_grid:
          dimensions: 5x5
        relationship: output rows are input rows in reverse vertical order
      - id: train_2
        input_grid:
          dimensions: 5x5
        output_grid:
          dimensions: 5x5
        relationship: output rows are input rows in reverse vertical order
      - id: train_3
        input_grid:
          dimensions: 7x7
        output_grid:
          dimensions: 7x7
        relationship: output rows are input rows in reverse vertical order
    transformation:
      type: geometric
      operation: vertical_flip
      axis: horizontal_midline
    objects:
      - type: grid
        properties:
          - height
          - width
          - rows
      - type: row
        properties:
          - sequence_of_pixels
          - vertical_index
    action:
      - name: reverse_row_order
        description: The order of the rows in the input grid is reversed to produce the output grid.
        input: input_grid
        output: output_grid
    ```


*   **Natural Language Program:**
    1.  Take the input grid.
    2.  Reverse the order of the rows. The first row becomes the last row, the second row becomes the second-to-last row, and so on, until the last row becomes the first row.
    3.  The resulting grid with the reversed row order is the output grid.