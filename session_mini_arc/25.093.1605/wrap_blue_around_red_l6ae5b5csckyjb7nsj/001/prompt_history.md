
## train_1

**input:**
```
0 0 0 2 0
0 5 0 0 0
0 0 0 0 0
0 2 0 0 7
0 0 0 0 0
```


**output:**
```
0 0 1 2 1
0 5 1 1 1
1 1 1 0 0
1 2 1 0 7
1 1 1 0 0
```


## train_2

**input:**
```
0 0 0 0 2
0 7 0 0 0
0 0 8 0 0
0 0 0 0 0
0 9 0 0 0
```


**output:**
```
0 0 0 1 2
0 7 0 1 1
0 0 8 0 0
0 0 0 0 0
0 9 0 0 0
```


## train_3

**input:**
```
0 2 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 7 0
0 0 0 0 0
```


**output:**
```
1 2 1 0 0
1 1 1 0 0
0 0 0 0 0
0 0 0 7 0
0 0 0 0 0
```

Okay, analyzing the provided examples.

## Perception of Task Elements

1.  **Input/Output:** Both are 2D grids (matrices) of integers.
2.  **Grid Dimensions:** The dimensions of the input and output grids are identical within each example pair.
3.  **Values:** The grids contain non-negative integers. The value '0' appears to be a background or empty state. Non-zero values seem to represent distinct objects or states.
4.  **Transformation:** The core transformation involves changing some '0' values to '1' in the output. Non-zero values from the input seem to persist in the output at their original locations.
5.  **Rule:** The change from '0' to '1' appears dependent on the proximity of the '0' cell to non-zero cells in the input grid. Specifically, a '0' becomes a '1' if it is adjacent (horizontally, vertically, or diagonally) to at least one non-zero cell.

## YAML Facts


```yaml
task_type: grid_transformation
input_object:
  type: grid
  element_type: integer
  properties:
    - non_negative_values
    - contains_zeros: true
    - contains_non_zeros: true
output_object:
  type: grid
  element_type: integer
  properties:
    - non_negative_values
    - dimensions_match_input: true
transformation_rule:
  action: modify_cells
  condition:
    - target_cell_value: 0
    - check: neighbors (orthogonal and diagonal)
    - criterion: at_least_one_neighbor_is_non_zero
  effect: change_cell_value_to_1
  preservation:
    - condition: input_cell_value_is_non_zero
    - effect: copy_value_to_output
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each cell (`row`, `col`) of the input grid.
3.  If the value of the input cell at (`row`, `col`) is '0':
    a.  Check all eight neighboring cells (including diagonals) of the cell (`row`, `col`) in the *input* grid.
    b.  If any of these neighbors contain a value other than '0':
        i.  Set the value of the corresponding cell (`row`, `col`) in the *output* grid to '1'.
4.  Leave all cells that were initially non-zero in the input grid unchanged in the output grid (this is implicitly handled by initializing the output as a copy and only modifying the '0's that meet the condition).
5.  Return the modified output grid.
