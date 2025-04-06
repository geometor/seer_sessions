
## train_1

**input:**
```
0 0 8 0 0 0 0 9 0 0
0 0 6 0 0 0 0 7 0 0
0 7 0 0 0 0 0 0 0 4
0 0 0 2 0 4 0 0 0 0
0 0 0 0 1 0 0 0 0 8
0 0 3 0 0 0 9 0 0 0
6 0 0 0 0 0 0 4 0 0
0 0 4 0 0 7 0 0 0 0
0 0 0 0 0 0 8 0 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 0 0 0 0 9 0 0
0 0 6 0 0 0 0 7 0 0
0 7 4 0 0 0 0 0 0 0
0 0 0 2 0 4 0 0 0 0
0 0 0 0 1 8 0 0 0 0
0 0 3 0 0 0 9 0 0 0
6 0 0 0 0 0 0 4 0 0
0 0 4 7 0 0 0 0 0 0
0 0 0 0 0 0 8 1 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
4 0 7 0 0
0 9 0 0 2
0 0 1 0 4
```


**output:**
```
4 7 0 0 0
0 9 0 0 2
0 0 1 0 4
```


## train_3

**input:**
```
0 8 0 4 0 0 0
4 0 0 0 0 0 7
0 0 1 0 0 8 0
0 9 0 0 4 0 0
```


**output:**
```
0 8 0 4 0 0 0
4 7 0 0 0 0 0
0 0 1 8 0 0 0
0 9 0 0 4 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 1 0 8 0 0 0 0
0 0 6 0 0 0 0 7
0 0 0 4 0 7 0 0
3 0 0 0 4 0 0 0
0 2 0 0 0 9 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 1 8 0 0 0 0 0
0 0 6 0 0 0 0 7
0 0 0 4 7 0 0 0
3 0 0 0 4 0 0 0
0 2 0 0 0 9 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are grids (2D arrays) of single digits, represented with spaces between columns and newlines between rows. The digits range from 0 to 9.
2.  **Core Element:** The fundamental units are the individual cells containing digits within the grid. The digit '0' appears to represent empty space or a background.
3.  **Transformation Scope:** The changes occur within individual rows. The transformation applied to one row does not seem to directly affect other rows.
4.  **Nature of Change:** Some non-zero digits change their position within a row, moving horizontally. Specifically, they move to the left. Zeros are introduced into the vacated positions. Not all non-zero digits move.

**Detailed Analysis & Pattern Recognition:**

*   **Focus on Rows:** Let's examine rows where changes occur compared to those that don't.
*   **Condition for Change:** Changes only seem to happen in rows containing *exactly two* non-zero digits. Rows with zero, one, or more than two non-zero digits remain unchanged.
*   **Specific Pairs:** Examining the rows with exactly two non-zero digits that *do* change reveals a specific pattern in the digit pairs involved:
    *   In `train_1`: (7, 4), (1, 8), (4, 7), (8, 1) pairs lead to movement.
    *   In `train_2`: (4, 7) pair leads to movement.
    *   In `train_3`: (4, 7), (1, 8) pairs lead to movement.
    *   In `train_4`: (1, 8), (4, 7) pairs lead to movement.
    *   Conversely, pairs like (8, 9), (6, 7), (2, 4), (3, 9), (6, 4), (9, 2), (1, 4), (8, 4), (9, 4) do *not* lead to movement in the examples.
*   **Rule Identification:** The movement occurs if and only if a row contains exactly two non-zero digits, and those digits form the pair {1, 8} (i.e., a 1 and an 8) or the pair {4, 7} (i.e., a 4 and a 7).
*   **Movement Mechanics:** When the condition is met, the rightmost of the two non-zero digits moves to the position immediately to the right of the leftmost digit. The original position of the moved digit becomes 0.

**YAML Facts:**


```yaml
task_elements:
  - type: grid
    description: A 2D array of single digits (0-9).
    properties:
      - rows: Independent units for transformation.
      - cells: Contain digits 0-9. '0' acts as empty space.
transformation_rule:
  scope: row-wise
  conditions:
    - description: Applies only if a row contains exactly two non-zero digits.
      property: count(non_zero_digits) == 2
    - description: The pair of non-zero digits must be {1, 8} or {4, 7}.
      property: set(non_zero_digits) == {1, 8} or set(non_zero_digits) == {4, 7}
  action:
    - description: Move the rightmost non-zero digit.
      target: rightmost_non_zero_digit
      destination: The cell immediately to the right of the leftmost_non_zero_digit.
      effect: The original cell of the moved digit becomes 0.
    - description: Rows not meeting the conditions remain unchanged.
      target: rows_not_meeting_conditions
      effect: No change.
relationships:
  - type: positional
    description: The relative left/right positions of the two non-zero digits determine which one moves and where it lands.
  - type: value-based_trigger
    description: The specific numeric values of the non-zero pair ({1,8} or {4,7}) trigger the movement action.
```


**Natural Language Program:**

1.  Iterate through each row of the input grid independently.
2.  For the current row, identify all non-zero digits and their column indices.
3.  Count the number of non-zero digits found in the row.
4.  Check if the count of non-zero digits is exactly two.
5.  If the count is not two, keep the row unchanged and proceed to the next row.
6.  If the count is exactly two, identify the values of these two digits.
7.  Check if the set of these two digit values is equal to {1, 8} or {4, 7}.
8.  If the set of digits is not {1, 8} and not {4, 7}, keep the row unchanged and proceed to the next row.
9.  If the count is two AND the set of digits is {1, 8} or {4, 7}:
    a.  Identify the column index of the leftmost non-zero digit (`c_left`) and the column index of the rightmost non-zero digit (`c_right`).
    b.  Get the value of the rightmost non-zero digit (`v_right`).
    c.  Modify the row: Set the value at column `c_right` to 0.
    d.  Modify the row: Set the value at column `c_left + 1` to `v_right`.
10. After processing all rows, assemble the modified rows into the output grid.
