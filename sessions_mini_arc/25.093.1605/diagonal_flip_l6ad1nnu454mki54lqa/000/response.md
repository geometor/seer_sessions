*   **Perception:** The task involves transforming a 2D grid containing numerical values. Each input grid features a pattern composed of a single non-zero integer against a background of zeros. The output grid shows the same pattern, but its orientation is changed. The transformation consistently appears to be a reflection across the main diagonal (from top-left to bottom-right) or, equivalently, a matrix transposition. The non-zero value itself remains unchanged, only its position is altered. The grid dimensions also remain constant.

*   **Facts:**
    
```yaml
    task_elements:
      - element: Grid
        properties:
          - type: 2D array of integers
          - dimensions: constant (e.g., 5x5 in examples)
          - contains: Cells
      - element: Cell
        properties:
          - position: (row, column) coordinates
          - value: integer
      - element: Non-zero Pattern
        properties:
          - composed_of: Cells with value > 0
          - value: a single unique integer (e.g., 3, 2, 8, 4)
          - forms: a specific shape or configuration within the grid
      - element: Background
        properties:
          - composed_of: Cells with value == 0
    relationships:
      - Non-zero Pattern exists within the Grid, surrounded by Background.
    action:
      - name: Transpose Pattern
      - input: Input Grid
      - output: Output Grid
      - steps:
          - For each Cell(row, col) in the Input Grid:
          - If Cell.value is non-zero:
          - Locate the corresponding Cell(col, row) in the Output Grid.
          - Set Output Grid Cell(col, row).value = Input Grid Cell(row, col).value
          - Otherwise (if Cell.value is zero):
          - Ensure the corresponding Output Grid Cell(col, row) is initially zero (unless overwritten by a transposed non-zero value).
    constraints:
      - Grid dimensions remain unchanged.
      - The non-zero integer value remains unchanged.
      - Only the positions of the non-zero values are modified according to the transpose rule.
    ```


*   **Natural Language Program:**
    1.  Create a new output grid with the same dimensions as the input grid, and initialize all its cells to zero.
    2.  Iterate through each cell of the input grid, identified by its row index `r` and column index `c`.
    3.  If the value of the input cell at `(r, c)` is not zero:
        a.  Take this non-zero value.
        b.  Place this value into the output grid at the transposed position `(c, r)`.
    4.  Return the completed output grid.