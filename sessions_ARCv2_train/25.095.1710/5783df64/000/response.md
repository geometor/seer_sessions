*   **Perception of the elements of the task**
    *   The input is a 2D grid of integers. The dimensions of the input grid vary across examples (9x9 or 6x6).
    *   The input grid contains mostly zeros (0) and exactly nine non-zero single digits (1-9).
    *   The output is always a 3x3 grid of integers.
    *   The output grid contains only the non-zero digits present in the input grid.
    *   The key transformation involves locating the non-zero numbers within specific sub-regions of the input grid and arranging them into the fixed-size output grid.

*   **Facts**
    
```yaml
    objects:
      - name: input_grid
        type: 2D array of integers
        properties:
          - dimensions: variable (height H, width W)
          - content: contains 9 non-zero integers (1-9) and many zeros (0)
      - name: output_grid
        type: 2D array of integers
        properties:
          - dimensions: fixed (3x3)
          - content: contains the 9 non-zero integers from the input_grid
      - name: region
        type: conceptual sub-grid within input_grid
        properties:
          - dimensions: (H/3, W/3)
          - quantity: 9 regions arranged in a 3x3 structure within input_grid
          - content: each region contains exactly one non-zero integer
      - name: non_zero_number
        type: integer
        properties:
          - value: 1-9
          - location: specific (row, column) within input_grid and within a specific region
      - name: zero
        type: integer
        properties:
          - value: 0

    relationships:
      - input_grid is partitioned into 9 equal regions.
      - each region corresponds to a unique cell in the output_grid based on its position (e.g., top-left region maps to output[0][0]).
      - the value of each cell in the output_grid is the single non_zero_number found within its corresponding region in the input_grid.

    actions:
      - name: partition_input
        description: Divide the input_grid into 9 equal rectangular regions arranged in a 3x3 grid.
      - name: find_non_zero
        description: For each region, locate the single non_zero_number within it.
      - name: construct_output
        description: Create a 3x3 output_grid where the cell at position (i, j) contains the non_zero_number found in the region at position (i, j) of the partitioned input_grid.

    ```


*   **Natural Language Program**
    1.  Receive the input grid with dimensions H (height) and W (width).
    2.  Determine the dimensions of the 9 equal sub-regions: region height `rH = H/3` and region width `rW = W/3`.
    3.  Initialize an empty 3x3 output grid.
    4.  Iterate through the 3 rows of regions (let the region row index be `i` from 0 to 2).
    5.  Inside this loop, iterate through the 3 columns of regions (let the region column index be `j` from 0 to 2).
    6.  For the current region `(i, j)`, define its boundaries in the input grid:
        *   Start row: `i * rH`
        *   End row: `(i + 1) * rH - 1`
        *   Start column: `j * rW`
        *   End column: `(j + 1) * rW - 1`
    7.  Search within these boundaries in the input grid to find the single non-zero number.
    8.  Place the found non-zero number into the output grid at position `(i, j)`.
    9.  After iterating through all 9 regions, return the completed 3x3 output grid.