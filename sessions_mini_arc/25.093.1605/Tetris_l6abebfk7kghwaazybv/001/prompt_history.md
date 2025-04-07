
## train_1

**input:**
```
0 0 4 0 0
0 4 4 4 8
2 2 4 8 8
2 2 0 7 8
7 7 7 7 8
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
5 5 5 5 5
0 0 0 0 0
5 5 5 5 5
```


## train_2

**input:**
```
0 4 0 0 0
1 4 4 7 0
1 4 7 7 7
1 3 3 7 0
1 3 3 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
5 5 5 5 5
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 1 0 0 0
0 1 0 0 2
1 1 3 3 2
8 1 3 3 2
8 8 8 2 2
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
5 5 5 5 5
5 5 5 5 5
5 5 5 5 5
```

Okay, I will analyze the provided input-output examples and generate the requested deliverables.

**Perception:**

The task involves transforming a 2D grid of numbers (input) into another 2D grid of the same dimensions (output). The output grid consists entirely of 0s and 5s. The transformation appears to operate row by row. The value assigned to an entire output row (either all 0s or all 5s) depends on a property of the corresponding input row. Specifically, it seems that if an input row contains the digit 0 at any position, the corresponding output row is filled with 0s. If an input row does *not* contain any 0s, the corresponding output row is filled with 5s.

**Facts:**


```yaml
task_elements:
  - object: input_grid
    type: 2D array of integers
    description: The source data grid.
  - object: output_grid
    type: 2D array of integers
    description: The target data grid, with the same dimensions as the input_grid. Contains only 0s and 5s.
  - object: grid_row
    description: A horizontal sequence of cells within a grid.
    relationship: Belongs to either input_grid or output_grid. Output rows correspond positionally to input rows.
  - property: contains_zero
    applies_to: input_grid_row
    description: A boolean property indicating whether the digit 0 exists anywhere within the input row.
  - action: fill_row
    operates_on: output_grid_row
    parameters: fill_value (either 0 or 5)
    description: Sets all cells in an output grid row to a specified value.
condition_action_link:
  - condition: An input_grid_row `contains_zero` is true.
    action: `fill_row` for the corresponding output_grid_row with `fill_value` = 0.
  - condition: An input_grid_row `contains_zero` is false.
    action: `fill_row` for the corresponding output_grid_row with `fill_value` = 5.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Iterate through each row of the input grid, keeping track of the row index.
3.  For the current input row, check if it contains the number 0 in any cell.
4.  If the input row contains at least one 0, fill the entire corresponding row in the output grid with 0s.
5.  If the input row does *not* contain any 0s, fill the entire corresponding row in the output grid with 5s.
6.  Return the completed output grid.
