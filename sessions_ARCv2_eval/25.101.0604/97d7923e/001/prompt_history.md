
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 2 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 7 0 0 0 0 0 0 0 5 0 0 0 0
0 0 7 0 0 1 0 0 0 0 5 0 0 3 0
0 0 7 0 0 7 0 1 0 0 5 0 0 5 0
0 0 7 0 0 7 0 7 0 0 5 0 0 5 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```


**output:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 1 0 0 0 0 0 0 0 5 0 0 0 0
0 0 1 0 0 1 0 0 0 0 5 0 0 3 0
0 0 1 0 0 7 0 1 0 0 5 0 0 3 0
0 0 1 0 0 7 0 7 0 0 5 0 0 3 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids (matrices) containing non-negative integers. The size of the grid varies between examples.
2.  **Cell Values:** The grids contain numbers, primarily 0 and other single-digit positive integers (e.g., 1, 2, 3, 5, 7). The value 0 appears to represent an empty or background cell.
3.  **Transformation Type:** The transformation modifies some cell values within the grid while leaving others unchanged. The overall grid dimensions remain the same.
4.  **Key Change Pattern:** The changes seem localized within columns. Specifically, a particular number (e.g., 5 in train_1, 3 in train_2, 7 in train_3) is changed to another specific number (e.g., 2 in train_1, 2 in train_2, 1 in train_3) only in cells *below* the first occurrence of the replacement number within that column.

**YAML Facts:**

```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D array
      - content: non-negative integers
      - zero_meaning: likely background/empty
      - dimensions: variable
  - element: Transformation
    properties:
      - type: cell value modification
      - scope: column-wise
      - preserves_dimensions: true
      - preserves_zeros: true
  - element: Key Numbers
    properties:
      - role: Target Number (T)
        identification: The largest non-zero integer value present in the input grid.
        action_on: Gets replaced under specific conditions.
        examples: [5 (train_1), 3 (train_2), 7 (train_3)]
      - role: Replacement Number (R)
        identification: The smallest non-zero integer value present in the input grid.
        action_on: Triggers replacement and is the value used for replacement.
        examples: [2 (train_1), 2 (train_2), 1 (train_3)]
  - element: Condition for Change
    properties:
      - location: column-based
      - trigger: Presence of the Replacement Number (R) in a column.
      - rule: Any occurrence of the Target Number (T) in a cell *below* the topmost occurrence of the Replacement Number (R) within the same column is changed to the Replacement Number (R).
      - constraint: Cells above or at the same row as the topmost R, or cells in columns without R, are not changed based on this rule.
```

**Natural Language Program:**

1.  **Identify Key Values:** Scan the entire input grid to find the smallest non-zero integer (`replacement_num`) and the largest non-zero integer (`target_num`).
2.  **Initialize Output:** Create a copy of the input grid to serve as the output grid.
3.  **Process Columns:** Iterate through each column of the grid from left to right.
4.  **Find First Replacement:** For the current column, scan downwards from the top row to find the row index of the *first* cell containing the `replacement_num`. If no `replacement_num` is found in this column, proceed to the next column.
5.  **Apply Replacements:** If a `replacement_num` was found at row index `first_occurrence_row`:
    *   Scan downwards in the *same column* starting from the row *below* `first_occurrence_row` (i.e., row index `first_occurrence_row + 1`) to the bottom row.
    *   For each cell examined in this downward scan, if its value in the *input* grid is equal to the `target_num`, change the value of the corresponding cell in the *output* grid to `replacement_num`.
6.  **Finalize:** After processing all columns, the modified output grid is the result.
