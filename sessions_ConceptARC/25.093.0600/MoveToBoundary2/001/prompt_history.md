
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
```

**Perception of the elements of the task:**

The input and output are both 10x10 grids containing integers 0 and 7. The transformation seems to rearrange the positions of the '7's within the grid while keeping the '0's. Observing the examples, it appears that the '7's within each column "fall" downwards, stacking up at the bottom of the column. The relative horizontal positions (columns) of the '7's are preserved, but their vertical positions change based on how many '7's are in that specific column. The operation is column-independent; the movement of '7's in one column does not affect other columns. It's like applying gravity to the '7's within each column separately.

**YAML block documenting facts:**


```yaml
task_elements:
  - object: grid
    properties:
      - type: 2D array
      - dimensions: 10x10
      - cell_values: [0, 7]
      - value_meaning:
          - 0: empty space
          - 7: particle/block
  - object: column
    properties:
      - acts as independent unit during transformation
relationships:
  - within each column, the number of '7's remains constant between input and output.
action:
  - name: apply_gravity_per_column
    description: >
      For each column in the input grid, count the total number of '7's.
      In the corresponding output column, place this number of '7's starting
      from the bottom row and filling upwards. Fill the remaining cells
      at the top of the column with '0's.
```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid and fill it entirely with '0's.
2.  Determine the number of rows and columns in the input grid.
3.  For each column index `c` from 0 to (number of columns - 1):
    a.  Count the number of cells containing '7' in the input grid's column `c`. Let this count be `num_sevens`.
    b.  Starting from the bottom row (row index `r = number of rows - 1`) and moving upwards:
        i.  If `num_sevens` is greater than 0, place a '7' in the output grid at position (`r`, `c`) and decrement `num_sevens`.
        ii. Continue this process for `num_sevens` steps upwards in the current column `c`.
4.  The resulting grid is the final output.
