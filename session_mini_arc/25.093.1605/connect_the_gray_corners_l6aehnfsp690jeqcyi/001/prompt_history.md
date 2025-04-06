
## train_1

**input:**
```
5 0 0 0 5
0 0 0 0 0
5 0 0 0 5
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
5 1 1 1 5
1 0 0 0 1
5 1 1 1 5
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 5 0 0 5
0 0 0 0 0
0 0 0 0 0
0 5 0 0 5
```


**output:**
```
0 0 0 0 0
0 5 1 1 5
0 1 0 0 1
0 1 0 0 1
0 5 1 1 5
```


## train_3

**input:**
```
0 5 0 0 5
0 5 0 0 5
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 5 1 1 5
0 5 1 1 5
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
5 0 5 0 0
0 0 0 0 0
0 0 5 0 5
0 0 0 0 0
5 0 5 0 5
```


**output:**
```
5 1 5 0 0
1 0 1 0 0
1 0 5 1 5
1 0 0 0 1
5 1 5 1 5
```

**Perception:**

The task involves transforming a 2D grid of numbers (representing colors). The input grids contain the numbers 0 and 5. The output grids contain the numbers 0, 1, and 5. The transformation appears to involve changing some of the 0s to 1s based on their proximity to the 5s. The positions and values of the 5s remain unchanged from input to output. The change from 0 to 1 seems to occur for cells that are directly adjacent (horizontally or vertically) to a cell containing a 5.

**Facts:**


```yaml
Objects:
  - name: Grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (e.g., 5x5 in examples)
      - cell_values: [0, 1, 5] (0 and 5 in input, 0, 1, 5 in output)
  - name: Cell
    properties:
      - value: integer (0, 1, or 5)
      - position: (row, column) coordinates
      - neighbors: adjacent cells (up, down, left, right)

Relationships:
  - Adjacency: Cells can be adjacent horizontally or vertically.
  - Transformation Trigger: A cell with value 5 triggers a change in adjacent cells with value 0.

Actions:
  - Identify cells with value 5 in the input grid.
  - For each cell with value 5, identify its adjacent cells (up, down, left, right).
  - If an adjacent cell has a value of 0 in the input grid, change its value to 1 in the output grid.
  - Cells that originally had value 5 remain 5 in the output grid.
  - Cells that originally had value 0 and are not adjacent to any 5 remain 0 in the output grid.
```


**Natural Language Program:**

1.  Create a new grid with the same dimensions as the input grid, initially copying all values from the input grid.
2.  Iterate through each cell `(r, c)` of the input grid.
3.  If the value of the input cell `input[r][c]` is 0:
    a.  Check its neighbors (up: `input[r-1][c]`, down: `input[r+1][c]`, left: `input[r][c-1]`, right: `input[r][c+1]`), making sure to stay within the grid boundaries.
    b.  If any of these valid neighbors has a value of 5 in the *input* grid, set the value of the corresponding cell in the *output* grid `output[r][c]` to 1.
4.  If the value of the input cell `input[r][c]` is 5, keep the value 5 in the output grid `output[r][c]`.
5.  Return the modified output grid.
