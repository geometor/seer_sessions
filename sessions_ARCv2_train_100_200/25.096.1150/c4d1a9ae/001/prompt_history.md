
## train_1

**input:**
```
4 2 4 4 6 4 5 5
2 4 4 4 6 4 4 5
4 2 4 4 6 4 5 5
2 4 4 6 4 4 4 5
4 2 4 6 4 4 5 5
2 4 4 6 4 4 4 5
4 2 4 6 4 4 5 5
2 4 4 4 6 4 4 5
4 2 4 4 6 4 5 5
2 4 4 4 6 4 4 5
```


**output:**
```
6 2 4 5 6 4 5 5
2 6 4 5 6 4 2 5
6 2 4 5 6 4 5 5
2 6 4 6 5 4 2 5
6 2 4 6 5 4 5 5
2 6 4 6 5 4 2 5
6 2 4 6 5 4 5 5
2 6 4 5 6 4 2 5
6 2 4 5 6 4 5 5
2 6 4 5 6 4 2 5
```


## train_2

**input:**
```
0 0 0 0 0 0 0 9
4 0 0 0 3 0 9 0
0 4 0 0 0 0 0 9
0 0 4 0 3 0 0 9
0 4 0 0 0 0 9 0
4 0 0 0 3 0 0 9
0 4 0 0 0 0 0 9
0 0 4 0 3 0 9 0
0 4 0 0 0 0 0 9
4 0 0 0 3 0 0 9
```


**output:**
```
3 3 3 0 9 0 4 9
4 3 3 0 3 0 9 4
3 4 3 0 9 0 4 9
3 3 4 0 3 0 4 9
3 4 3 0 9 0 9 4
4 3 3 0 3 0 4 9
3 4 3 0 9 0 4 9
3 3 4 0 3 0 9 4
3 4 3 0 9 0 4 9
4 3 3 0 3 0 4 9
```

Okay, let's break down the transformation logic based on the provided examples.

**Perception of Elements:**

1.  **Input/Output Structure:** Both inputs and outputs are 2D grids (arrays) of single-digit integers.
2.  **Dimensions:** The grid dimensions remain constant between input and output (10 rows x 8 columns in the examples).
3.  **Core Transformation:** The transformation involves selectively changing specific integer values within the grid. The changes are not uniform; they depend on the *position* (specifically, the column) of the value being changed.
4.  **Target Value:** In each example pair, there seems to be one specific integer value that is subject to modification (e.g., `4` in `train_1`, `0` in `train_2`).
5.  **Conditional Replacement:** If a cell contains the target value, its value in the output grid is determined by its column index. Cells *not* containing the target value retain their original value.
6.  **Column-Based Rules:** A specific set of rules maps column indices to replacement values for the target integer. These rules appear unique to each task instance.

**Facts (YAML):**


```yaml
task_type: grid_transformation
input_data:
  type: 2D_grid
  element_type: integer
  properties:
    - dimensions_preserved: true
output_data:
  type: 2D_grid
  element_type: integer
transformation:
  type: conditional_replacement
  target_value: 
    description: A specific integer identified within the input grid (varies per task instance, e.g., 4 or 0).
    scope: grid-wide
  condition:
    type: position_based
    attribute: column_index
  action:
    type: replace_value
    rules:
      description: A mapping defining the output value based on the column index when the cell value matches the target_value.
      example_1: # target_value = 4
        - column_indices: [0, 1]
          replacement_value: 6
        - column_indices: [3, 4]
          replacement_value: 5
        - column_indices: [6]
          replacement_value: 2
        - default: keep_original # For target value 4 in other columns
      example_2: # target_value = 0
        - column_indices: [0, 1, 2]
          replacement_value: 3
        - column_indices: [4]
          replacement_value: 9
        - column_indices: [6, 7]
          replacement_value: 4
        - default: keep_original # For target value 0 in columns 3, 5
  unmodified_elements:
    description: All cells whose value does not match the target_value remain unchanged.
```


**Natural Language Program:**

1.  **Initialize:** Create a new grid (`output_grid`) as a copy of the `input_grid`.
2.  **Identify Target:** Determine the specific integer `target_value` that undergoes transformation in this task instance (e.g., 4 or 0).
3.  **Define Column Rules:** Establish the set of rules mapping column indices to replacement values for the `target_value`. This includes:
    *   Which columns trigger a replacement.
    *   What the replacement value is for each specified column (or group of columns).
    *   Implicitly, that the `target_value` remains unchanged if its column is not mentioned in the rules.
4.  **Iterate and Transform:** Go through each cell of the `input_grid`, accessing its row index `r`, column index `c`, and value `v`.
5.  **Apply Rules:**
    *   Check if the current cell's value `v` is equal to the `target_value`.
    *   If `v` matches the `target_value`:
        *   Check if the current column index `c` corresponds to any defined replacement rule.
        *   If a rule exists for column `c`, update the cell at `output_grid[r][c]` with the specified replacement value.
        *   If no rule exists for column `c`, the cell `output_grid[r][c]` retains the `target_value` (as it was copied initially).
    *   If `v` does not match the `target_value`, the cell `output_grid[r][c]` remains unchanged from the initial copy.
6.  **Finalize:** Return the completed `output_grid`.
