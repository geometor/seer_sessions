*   **Perception of Task Elements:**
    *   The input and output are 2D grids (matrices) of integers.
    *   Each input grid contains exactly one non-zero integer (always 4 in the examples) and the rest are zeros.
    *   The output grid is derived from the input grid based on the position of the non-zero integer.
    *   The transformation involves propagating the non-zero value either horizontally (filling a row) or vertically (filling a column).
    *   The direction of propagation (row or column) depends on the column index of the non-zero element in the input grid. Specifically, if the non-zero element is in the first column (index 0), its entire row is filled. Otherwise, its entire column is filled.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: Input Grid
        properties:
          - type: 2D integer matrix
          - dimensions: 6x6 (based on examples)
          - content: Contains mostly zeros and a single non-zero integer (value V)
      - object: Output Grid
        properties:
          - type: 2D integer matrix
          - dimensions: Same as Input Grid
          - content: Derived from Input Grid
      - object: Non-Zero Cell
        properties:
          - location: (row R, column C) in Input Grid
          - value: V
      - action: Locate Non-Zero Cell
        inputs: Input Grid
        outputs: R, C, V
      - action: Conditional Fill
        conditions:
          - if: C == 0
            then: Fill Row R in Output Grid with value V
          - if: C != 0
            then: Fill Column C in Output Grid with value V
        inputs: Output Grid (initialized with zeros), R, C, V
        outputs: Modified Output Grid
      - relationship: Output Grid Generation
        process:
          - Initialize Output Grid with zeros, matching Input Grid dimensions.
          - Locate the Non-Zero Cell (R, C, V) in the Input Grid.
          - Apply Conditional Fill based on the column index C.
    ```


*   **Natural Language Program:**
    1.  Identify the row index `R`, column index `C`, and value `V` of the single non-zero cell in the input grid.
    2.  Create a new output grid with the same dimensions as the input grid, initially filled with zeros.
    3.  If the column index `C` of the non-zero cell is 0, fill the entire row `R` of the output grid with the value `V`.
    4.  Otherwise (if the column index `C` is not 0), fill the entire column `C` of the output grid with the value `V`.
    5.  Return the modified output grid.