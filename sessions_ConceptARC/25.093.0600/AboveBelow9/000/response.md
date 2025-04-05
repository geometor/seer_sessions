## Perception

The input and output are grids of numbers. The number `0` appears to represent the background. Each input grid contains various shapes or patterns formed by non-zero digits (e.g., `3` in the first example, `7` in the second). A distinct feature in both input grids is a single row composed entirely of the digit `4`. This row acts as a horizontal divider.

Observing the transformation, the row of `4`s remains unchanged in the output. All rows *above* the row of `4`s also remain unchanged. However, all rows *below* the row of `4`s are replaced entirely with `0`s in the output. The specific non-zero digits (like `3` or `7`) above the `4`s row seem irrelevant to the transformation rule itself, other than being preserved. The core operation is contingent on the location of the solid row of `4`s.

## Facts


```yaml
Objects:
  - name: input_grid
    type: grid
    properties:
      - contains digits, including 0, 4, and others (e.g., 3, 7)
  - name: output_grid
    type: grid
    properties:
      - derived from input_grid
  - name: boundary_row
    type: row
    properties:
      - located within input_grid
      - consists entirely of the digit 4
Relationships:
  - The output_grid retains all rows from the input_grid up to and including the boundary_row.
  - Rows in the output_grid below the index of the boundary_row are replaced with 0s.
Actions:
  - Identify the index of the first row in the input_grid that consists entirely of the digit 4.
  - Copy all rows from the input_grid from the beginning up to and including this identified boundary_row to the output_grid.
  - Fill all subsequent rows in the output_grid (below the boundary_row) with the digit 0.
```


## Natural Language Program

1.  Iterate through the rows of the input grid from top to bottom.
2.  Identify the first row that consists entirely of the digit `4`. Let the index of this row be `boundary_index`.
3.  Create a new output grid with the same dimensions as the input grid.
4.  Copy all rows from the input grid from index `0` up to and including `boundary_index` to the corresponding rows in the output grid.
5.  For all rows in the output grid with an index greater than `boundary_index`, fill them entirely with the digit `0`.
6.  Return the resulting output grid.