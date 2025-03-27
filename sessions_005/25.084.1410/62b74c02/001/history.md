
## train_1

**input:**
```
3 2 3 0 0 0 0 0 0 0 0 0
1 2 1 0 0 0 0 0 0 0 0 0
3 2 3 0 0 0 0 0 0 0 0 0
1 3 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 2 3 3 3 3 3 3 3 3 2 3
1 2 1 1 1 1 1 1 1 1 2 1
3 2 3 3 3 3 3 3 3 3 2 3
1 3 1 1 1 1 1 1 1 1 3 1
```


## train_2

**input:**
```
8 2 8 0 0 0 0 0 0 0
1 8 1 0 0 0 0 0 0 0
1 8 1 0 0 0 0 0 0 0
```


**output:**
```
8 2 8 8 8 8 8 8 2 8
1 8 1 1 1 1 1 1 8 1
1 8 1 1 1 1 1 1 8 1
```


## train_3

**input:**
```
2 3 8 2 0 0 0 0 0 0 0 0 0 0
2 8 8 2 0 0 0 0 0 0 0 0 0 0
2 8 3 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 3 8 2 2 2 2 2 2 2 2 3 8 2
2 8 8 2 2 2 2 2 2 2 2 8 8 2
2 8 3 2 2 2 2 2 2 2 2 8 3 2
```

**Perception**

The input grid contains a rectangular block of various colors starting from the top-left corner (column 0). This block is immediately followed by a region filled entirely with the white color (0), extending to the right edge of the grid. The output grid has the same dimensions as the input grid. The transformation involves filling the white region based on the columns of the initial colored block. The initial block itself is preserved in the output. The filling pattern works from right to left: the rightmost columns of the output replicate the columns of the initial block in reverse order (last column of block maps to last column of output, second-last maps to second-last, etc.). Once all columns of the initial block have been used in this reverse mapping, any remaining columns in the central part of the filled region are populated by replicating the *first* column of the initial block.

**Facts**


```yaml
elements:
  - object: input_grid
    attributes:
      - type: grid
      - contains: [initial_block, white_region]
  - object: initial_block
    attributes:
      - type: rectangle
      - location: top-left corner (column 0) of input_grid
      - colors: various non-white colors
      - width: W (variable across examples)
      - height: H (same as input_grid height)
  - object: white_region
    attributes:
      - type: rectangle
      - location: immediately right of initial_block in input_grid
      - color: white (0)
      - width: GridW - W (where GridW is input_grid width)
      - height: H
  - object: output_grid
    attributes:
      - type: grid
      - dimensions: same as input_grid
      - content: derived from input_grid

relationships:
  - type: transformation
    applies_to: input_grid
    results_in: output_grid
    rule:
      - step: Preserve the initial_block in the output_grid at the same location.
      - step: Fill the columns corresponding to the white_region in the output_grid.
      - detail: The filling uses columns from the initial_block.
      - rule_part_1:
          action: map_columns_reverse
          source: initial_block columns (from right-to-left: W-1, W-2, ..., 0)
          target: output_grid columns (from right-to-left: GridW-1, GridW-2, ..., GridW-W)
          condition: applies for the last W columns of the output grid.
      - rule_part_2:
          action: fill_columns
          source: initial_block column 0
          target: output_grid columns (from W to GridW-W-1)
          condition: applies to any columns between the preserved initial_block and the columns filled by rule_part_1.
```


**Natural Language Program**

1.  Identify the initial rectangular block of non-white pixels starting from the top-left corner (column 0) of the input grid. Let its width be `W`.
2.  Note the total width of the input grid, `GridW`.
3.  Create an output grid of the same dimensions as the input grid.
4.  Copy the initial block (columns 0 to `W-1`) from the input grid to the corresponding columns in the output grid.
5.  Fill the columns in the output grid from index `GridW-1` down to `GridW-W` by copying columns from the initial block in reverse order. Specifically, for `i` from 0 to `W-1`:
    *   Copy the column `W-1-i` from the initial block to column `GridW-1-i` in the output grid.
6.  Fill any remaining columns in the output grid, specifically those from index `W` up to `GridW-W-1`, by repeatedly copying the *first* column (column 0) of the initial block into each of these columns.
