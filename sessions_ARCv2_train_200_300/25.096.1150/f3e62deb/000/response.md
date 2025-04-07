*   **Perception:** The task involves manipulating 10x10 grids containing numerical values. Each input grid features a single, distinct object composed of non-zero identical digits, arranged in a 3x3 hollow square pattern, against a background of zeros. The output grid shows the same object relocated to a different position within the grid, while the background remains zero. The object's shape and color (the specific digit) are preserved during the transformation. The movement is always purely horizontal or purely vertical.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: grid
        properties:
          size: 10x10
          cell_values: integers (0-9)
          background_value: 0
      - type: object
        properties:
          shape: 3x3 hollow square
          composition: uniform non-zero digit (color)
          count_per_grid: 1
          location: variable within the grid
      - type: transformation
        action: move object
        properties:
          preserves_shape: true
          preserves_color: true
          movement_axis: horizontal or vertical (mutually exclusive per instance)
          movement_rule: dependent on object color
    rules:
      - condition: object_color == 8
        action: move object horizontally
        target_location: top-left column index becomes 7, row index remains unchanged
      - condition: object_color == 4
        action: move object vertically
        target_location: top-left row index becomes 7, column index remains unchanged
      - condition: object_color == 6
        action: move object vertically
        target_location: top-left row index becomes 0, column index remains unchanged
    relationships:
      - object location (output) depends on object color (input) and object location (input)
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a 10x10 grid filled with zeros.
    2.  Scan the input grid to locate the non-zero object. Identify its color (the digit used) and the row and column indices of its top-left corner cell.
    3.  Determine the destination coordinates for the object's top-left corner based on its color:
        *   If the object's color is 8, the destination row index is the same as the original row index, and the destination column index is 7.
        *   If the object's color is 4, the destination column index is the same as the original column index, and the destination row index is 7.
        *   If the object's color is 6, the destination column index is the same as the original column index, and the destination row index is 0.
    4.  Place the object (maintaining its original 3x3 hollow square shape and color) onto the output grid, starting at the calculated destination top-left corner coordinates.