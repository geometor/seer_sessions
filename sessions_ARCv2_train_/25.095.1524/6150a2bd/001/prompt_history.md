
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

## Perception

The input and output are both 3x3 grids containing single-digit integers. Comparing the input and output grids in both examples, it appears that the output grid is a rotated version of the input grid. Specifically, the output grid corresponds to the input grid rotated by 180 degrees.

## Facts


```yaml
objects:
  - name: input_grid
    type: 2D list of integers
    rows: 3
    columns: 3
    description: The initial arrangement of numbers.
  - name: output_grid
    type: 2D list of integers
    rows: 3
    columns: 3
    description: The transformed arrangement of numbers.

actions:
  - name: rotate_180
    input: input_grid
    output: output_grid
    description: Rotates the input grid by 180 degrees. The element at input_grid[i][j] moves to output_grid[rows-1-i][columns-1-j].

relationships:
  - type: transformation
    from: input_grid
    to: output_grid
    via: rotate_180
    description: The output grid is the result of applying a 180-degree rotation to the input grid.
```


## Natural Language Program

1.  Read the input 3x3 grid.
2.  Create a new empty 3x3 grid for the output.
3.  For each element at position (row `i`, column `j`) in the input grid, place it at position (2 - `i`, 2 - `j`) in the output grid.
4.  Return the resulting output grid.
