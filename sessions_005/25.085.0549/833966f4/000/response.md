**Perception**

The input and output are both single-column grids (5 rows, 1 column).
The set of pixel values (colors) present in the input is identical to the set of pixel values in the output, but their positions are changed.
Observing the transformation:
- In `train_1`, the value at row 0 (maroon/9) swaps with the value at row 1 (white/0). The value at row 2 (blue/1) remains unchanged. The value at row 3 (magenta/6) swaps with the value at row 4 (azure/8).
- In `train_2`, the value at row 0 (yellow/4) swaps with the value at row 1 (green/3). The value at row 2 (magenta/6) remains unchanged. The value at row 3 (red/2) swaps with the value at row 4 (azure/8).
The pattern appears to be swapping the contents of adjacent pairs of rows, starting from the top (rows 0 and 1, rows 2 and 3, and so on). If there is an odd number of rows, the last row remains in its original position.

**Facts**


```yaml
task_type: grid_transformation
input_shape:
  type: grid
  description: A single column grid (Nx1). In the examples, N=5.
output_shape:
  type: grid
  description: Same dimensions as the input grid (Nx1).
grid_elements:
  type: pixels
  description: Cells containing integer values 0-9 representing colors.
transformation:
  type: rearrangement
  scope: rows
  pattern: pairwise_swap
  details: |
    Iterate through the rows of the input grid using an index `i` starting from 0 and incrementing by 2.
    For each `i`, if row `i+1` exists, swap the entire content of row `i` with the entire content of row `i+1`.
    If the grid has an odd number of rows, the last row (at index N-1) is not involved in any swap and remains in its original position in the output.
invariants:
  - Grid dimensions remain the same.
  - The multiset of pixel values remains the same.
variants:
  - The vertical position (row index) of pixel values changes based on the pairwise swapping rule.
```


**Natural Language Program**

1.  Take the input grid.
2.  Create a copy of the input grid to serve as the output grid.
3.  Iterate through the rows of the grid using an index `i`, starting at 0 and stepping by 2 (i.e., process rows 0, 2, 4, ...).
4.  For each index `i`, check if a subsequent row `i+1` exists within the grid boundaries.
5.  If row `i+1` exists, swap the content of row `i` in the output grid with the content of row `i+1`.
6.  If row `i+1` does not exist (meaning row `i` is the last row and the total number of rows is odd), do nothing for this row `i`.
7.  Return the modified grid as the output.