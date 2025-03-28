*   **Perception:**
    *   Each input grid contains two distinct objects of the same non-white color (gray, blue, or red in the examples).
    *   These two objects appear to be identical or mirrored reflections of each other.
    *   The two objects are separated by a single row or column composed entirely of white pixels (0).
    *   In the output grid, this separating row or column is filled entirely with green pixels (3).
    *   All other pixels from the input grid remain unchanged in the output grid.
    *   Example 1 shows vertical separation by a column. Examples 2 and 3 show horizontal separation by a row.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    objects:
      - identifier: primary_shapes
        count: 2
        properties:
          - color: non-white (gray, blue, red in examples)
          - symmetry: identical or mirrored
          - spatial_relation: separated by a single line (row or column)
      - identifier: separating_line
        count: 1
        properties:
          - type: row or column
          - composition: entirely white pixels (0)
          - location: between the two primary_shapes
      - identifier: fill_color
        count: 1
        properties:
          - color: green (3)
    actions:
      - name: identify_objects
        inputs: input_grid
        outputs: primary_shapes, separating_line
      - name: verify_conditions
        inputs: primary_shapes, separating_line
        conditions:
          - primary_shapes count is 2
          - primary_shapes have same color
          - separating_line exists (single row/column, all white)
      - name: fill_line
        inputs: input_grid, separating_line, fill_color
        outputs: output_grid
        description: Replace the white pixels in the separating_line with the fill_color across the entire row or column.
    relationships:
      - The separating_line is located exactly between the bounding boxes of the two primary_shapes.
      - The orientation of the separating_line (row or column) depends on the relative positioning of the primary_shapes (vertical or horizontal separation).
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, connected non-white objects in the input grid.
    2.  Check if there are exactly two such objects and if they share the same color.
    3.  Determine the bounding boxes for these two objects.
    4.  Check if the objects are separated horizontally by exactly one row, where all pixels in that row between the objects (inclusive of the full grid width) are white (0). If yes, identify the index of this row.
    5.  Check if the objects are separated vertically by exactly one column, where all pixels in that column between the objects (inclusive of the full grid height) are white (0). If yes, identify the index of this column.
    6.  If a separating white row is found (step 4), create the output grid by copying the input grid and then changing all pixels in that specific row index to green (3).
    7.  If a separating white column is found (step 5), create the output grid by copying the input grid and then changing all pixels in that specific column index to green (3).
    8.  If neither condition (step 4 or 5) is met, the transformation rule might not apply (or the output could be identical to the input, though examples suggest a change always occurs). Based on the examples, assume one of the conditions will always be met.