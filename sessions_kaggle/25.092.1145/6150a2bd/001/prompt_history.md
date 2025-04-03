
## train_1

**input:**
```
5 5 2
1 0 0
0 0 0
```


**output:**
```
0 0 0
0 0 1
2 5 5
```


## train_2

**input:**
```
3 3 8
3 7 0
5 0 0
```


**output:**
```
0 0 5
0 7 3
8 3 3
```

Okay, let's break down the task based on the provided examples.

**Perception of Elements:**

1.  **Input/Output Format:** Both the input and output are structured as grids (2D arrays) of integers. In the examples provided, they are 3x3 grids.
2.  **Content:** The grids contain non-negative integers. The non-zero numbers present in the input grid seem to reappear in the output grid, possibly rearranged. The number of zeros might change or stay the same depending on the rearrangement.
3.  **Transformation Pattern:** Observing the positions of the numbers, the transformation appears to be a spatial rearrangement. Specifically, comparing the input and output grids in both examples suggests a 180-degree rotation.
    *   In `train_1`, the top-left `5` moves to the bottom-right, the top-right `2` moves to the bottom-left, and the middle-left `1` moves to the middle-right.
    *   In `train_2`, the top-left `3` moves to bottom-right, the top-right `8` moves to bottom-left, the middle-left `3` moves to middle-right, the middle-center `7` stays in the middle-center, and the bottom-left `5` moves to top-right.
    *   This consistent pattern across both examples strongly indicates a 180-degree rotation of the entire grid.

**Facts:**


```yaml
objects:
  - input_grid:
      description: A 2D array representing the initial state.
      properties:
        - dimensions: [rows, columns] (e.g., 3x3 in the examples)
        - elements: Non-negative integers
  - output_grid:
      description: A 2D array representing the final state after transformation.
      properties:
        - dimensions: Identical to input_grid dimensions
        - elements: Non-negative integers derived from input_grid
relationships:
  - transformation: The output_grid is derived from the input_grid.
  - type: Spatial rearrangement.
  - specific_transformation: 180-degree rotation.
  - element_mapping: A cell at position (row `r`, column `c`) in the input_grid corresponds to the cell at position (total_rows - 1 - `r`, total_columns - 1 - `c`) in the output_grid. The value is transferred between these corresponding cells.
```


**Natural Language Program:**

1.  Accept the input grid.
2.  Determine the number of rows (`R`) and columns (`C`) in the input grid.
3.  Create a new grid (the output grid) with the same dimensions (`R` x `C`).
4.  Iterate through each cell of the input grid using its row index `r` (from 0 to `R-1`) and column index `c` (from 0 to `C-1`).
5.  For each input cell at `(r, c)`, retrieve its value.
6.  Calculate the target position in the output grid: the target row index is `R - 1 - r`, and the target column index is `C - 1 - c`.
7.  Place the retrieved value into the calculated target position `(R - 1 - r, C - 1 - c)` in the output grid.
8.  After processing all cells from the input grid, return the completed output grid.
