*   **Perception**:
    *   The inputs and outputs are 2D grids of integers.
    *   Each grid contains primarily zeros (representing a background) and one dominant non-zero integer representing a pattern or shape.
    *   Each input grid also contains a single instance of a different non-zero integer, located consistently in the bottom-left corner (index [6, 0]). Let's call this the "marker" color.
    *   The dominant non-zero integer in the input (e.g., 3 in `train_1`, 2 in `train_2`) represents the "target" color.
    *   In the output grid, all instances of the "target" color from the input are replaced by the "marker" color.
    *   The original cell containing the "marker" color in the input is replaced by 0 in the output.
    *   All cells with the value 0 in the input remain 0 in the output.
    *   The spatial arrangement or shape formed by the non-zero elements is preserved, but the color is changed.

*   **YAML Facts**:
    
```yaml
    task_type: grid_transformation
    components:
      - grid:
          type: 2D array of integers
          properties:
            - dimensions: variable (observed as 7x7 in examples)
            - cell_values: integers
      - colors:
          - background_color: 0
          - target_color:
              description: The dominant non-zero color forming a pattern in the input.
              examples: [3 in train_1, 2 in train_2]
              property: occurs multiple times
          - marker_color:
              description: A unique non-zero color present only once in the input.
              examples: [6 in train_1, 4 in train_2]
              property: occurs exactly once
              location: typically fixed (observed as bottom-left corner [6,0] in examples)
    actions:
      - identify:
          - marker_color: Find the value present exactly once in the input grid.
          - target_color: Find the most frequent non-zero color (excluding the marker_color).
      - replace:
          - target_color cells: Change their value to the marker_color in the output.
          - marker_color cell: Change its value to the background_color (0) in the output.
      - preserve:
          - background_color cells: Keep their value (0) in the output.
          - structure: Maintain the relative positions of the pattern.
    relationships:
      - input_output: The output grid is derived from the input grid based on color replacement rules.
      - marker_target: The marker_color dictates the new color for the target_color pattern.
    ```


*   **Natural Language Program**:
    1.  Identify the `marker_color` by finding the non-zero integer that appears exactly once in the input grid.
    2.  Identify the `target_color` by finding the non-zero integer that appears most frequently in the input grid (this will be the color forming the main pattern).
    3.  Create a new output grid with the same dimensions as the input grid, initially filled with zeros (or as a copy).
    4.  Iterate through each cell of the input grid:
        a.  If the value of the current input cell is equal to the `target_color`, set the value of the corresponding cell in the output grid to the `marker_color`.
        b.  If the value of the current input cell is equal to the `marker_color`, set the value of the corresponding cell in the output grid to 0.
        c.  If the value of the current input cell is 0, set the value of the corresponding cell in the output grid to 0.
    5.  Return the modified output grid.