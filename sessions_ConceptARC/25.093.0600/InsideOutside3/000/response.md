*   **Perception:** The task operates on 10x10 grids containing primarily digits 0, 2, and 4. The input grids usually feature multiple instances of the digit 2 and a single instance of the digit 4. The output grid is derived from the input grid based on a conditional rule involving the spatial relationship between the digit 4 and any adjacent digits 2. Specifically, the transformation depends on whether the cell containing the digit 4 has any neighbouring cells (horizontally, vertically, or diagonally) that contain the digit 2. If such a neighbour exists, the digit 4 is preserved in the output, and all instances of the digit 2 in the grid are changed to 0. Conversely, if the digit 4 has no adjacent neighbours with the digit 2, then all instances of the digit 2 are preserved in the output, and the digit 4 is changed to 0.

*   **YAML Facts:**
    
```yaml
    objects:
      - grid:
          description: A 10x10 matrix of integers.
          properties:
            - dimensions: [10, 10]
            - cells: Contains integer values, primarily 0, 2, and 4.
      - cell:
          description: A single element within the grid.
          properties:
            - position: (row, column) coordinates.
            - value: An integer (0, 2, or 4).
      - target_digit_4:
          description: The cell containing the value 4. Assumed unique per input grid.
          properties:
            - value: 4
            - position: Specific (row, column) coordinates.
      - neighbor_digit_2:
          description: Cells containing the value 2.
          properties:
            - value: 2
            - position: Specific (row, column) coordinates.
    relationships:
      - adjacency:
          description: The spatial relationship between the cell containing 4 and its 8 immediate neighbours (horizontal, vertical, diagonal).
          condition: Check if any neighbour of the cell with value 4 contains the value 2.
    actions:
      - find_digit_4: Locate the coordinates of the cell containing 4.
      - check_neighbors: Examine the 8 neighbours of the cell containing 4 for the presence of the value 2.
      - conditional_replacement:
          if: A neighbour contains 2.
          then: Keep the value 4 at its position, replace all values 2 in the entire grid with 0.
          else: Replace the value 4 with 0, keep all values 2 at their positions.
      - copy_zeros: All cells with value 0 remain 0.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Find the coordinates (row `r4`, column `c4`) of the cell containing the value 4 in the input grid.
    3.  Check the 8 neighbouring cells surrounding (`r4`, `c4`). Determine if any of these neighbours contain the value 2.
    4.  **Condition 1:** If at least one neighbour contains the value 2:
        *   Iterate through all cells in the output grid.
        *   If a cell contains the value 2, change its value to 0.
        *   The cell at (`r4`, `c4`) retains its value 4.
    5.  **Condition 2:** If none of the neighbours contain the value 2:
        *   Change the value of the cell at (`r4`, `c4`) in the output grid to 0.
        *   All cells originally containing 2 retain their value 2.
    6.  All cells originally containing 0 retain their value 0 in both conditions.
    7.  Return the modified output grid.