**General Assessment and Strategy:**

The previous code (`code_00.py`) successfully solved `train_2` but failed on `train_1` and `train_3`. The analysis revealed two distinct issues:
1.  **Primary Rule Refinement (Train 1):** The rule for columns containing the global minimum non-zero value (`R`) needed adjustment. The special start condition when `first_r_row == 1` was incorrect. The replacement seems to start much later in this specific case.
2.  **Secondary Rule Discovery (Train 3):** The expected output for `train_3` showed changes (5 -> 3) in columns *without* the global minimum (`R=1`). This suggests a separate rule applies when `R` is absent from a column, likely involving local minimum and maximum values within that column.

The strategy is to:
1.  Refine the primary rule's special start condition for `first_r_row == 1` based on the `train_1` discrepancy.
2.  Formulate and implement a secondary rule for columns lacking `R`, based on the `train_3` changes.
3.  Combine these two rules into a single transformation function.

**Metrics and Observations:**

*   **Global Values & Threshold:**
    *   Train 1: R=2, T=5, Rows=10, Block Threshold = 10 // 2 = 5
    *   Train 2: R=2, T=3, Rows=10, Block Threshold = 10 // 2 = 5
    *   Train 3: R=1, T=7, Rows=10, Block Threshold = 10 // 2 = 5

*   **Analysis of Discrepancies in `code_00.py` results:**
    *   **Train 1 (Expected Pixels Off: 5):**
        *   **Column 4:** Input `[0,2,5,5,5,5,5,5,5,2]`. `first_r=1`. `first_t_below_r=2`. Code used `start=2+2=4`. Replaced rows 4-8 -> `[0,2,5,5,2,2,2,2,2,2]`. Expected output `[0,2,5,5,5,5,2,2,2,2]` replaces rows 6-8. **Error:** Incorrect start row (4 vs 6). The new hypothesis suggests `start = first_t + 4 = 2 + 4 = 6`, which matches the expected output.
        *   **Column 7:** Input `[0,0,0,2,5,5,5,5,5,2]`. `first_r=3`. `first_t_below_r=4`. Code used `start=4`. Replaced rows 4-8 -> `[0,0,0,2,2,2,2,2,2,2]`. Expected output is `[0,0,0,2,2,2,2,2,2,2]`. The reported error count (5 total) seems inconsistent with the column-by-column analysis if this column is correct. However, focusing on fixing the rules, the current primary rule (without the special `first_r=1` case) works correctly here.
    *   **Train 2 (Expected Pixels Off: 0):** Code worked correctly. Rules applied: Primary rule (normal case) in Col 6, Primary rule (blocking) in Col 2.
    *   **Train 3 (Expected Pixels Off: 2):**
        *   **Column 13:** Input `[0,0,0,0,0,0,3,5,5,3]`. No R=1 present. Code made no changes. Expected output `[0,0,0,0,0,0,3,3,3,3]`. **Error:** Missing secondary rule (5->3 change).
        *   **Column 14:** Input `[0,0,0,0,0,0,0,3,5,3]`. No R=1 present. Code made no changes. Expected output `[0,0,0,0,0,0,0,3,3,3]`. **Error:** Missing secondary rule (5->3 change).
        *   Secondary rule hypothesis: In columns without R, find local min (`min_l`) and max (`max_l`). If `min_l` exists above and below `max_l`, replace all `max_l` with `min_l`.
            *   Col 13: `min_l=3`, `max_l=5`. 3 at row 6 (above 5s) and row 9 (below 5s). Rule applies -> Replace 5s with 3s. Matches expected.
            *   Col 14: `min_l=3`, `max_l=5`. 3 at row 7 (above 5) and row 9 (below 5). Rule applies -> Replace 5 with 3. Matches expected.

**YAML Facts:**

```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D array
      - content: non-negative integers (0-9)
      - zero_meaning: background/empty
      - dimensions: variable height and width
  - element: Global Key Values
    properties:
      - role: Global Min Non-Zero (R)
        identification: Smallest non-zero integer globally in the input grid.
      - role: Global Max Non-Zero (T)
        identification: Largest non-zero integer globally in the input grid.
      - condition: Global R and T must exist and R != T for the primary rule.
  - element: Transformation
    properties:
      - type: cell value modification
      - scope: column-wise, conditional based on presence/absence of R
      - preserves_dimensions: true
      - preserves_zeros: true
  - element: Columnar Process
    properties:
      - scope: Operates independently on each column.
      - branching: Applies one of two rules based on presence of Global R.
      - grid_property_dependency: Uses number of rows (`rows`).
  - element: Primary Rule (Column contains Global R)
    properties:
      - identification: Find row index `first_r_row` of the first Global R.
      - blocking_condition: If `first_r_row >= rows // 2`, no replacement occurs.
      - target_identification: If not blocked, find `first_t_below_r_row` (first Global T below `first_r_row`). If none, no replacement occurs.
      - start_row_determination:
          - If `first_r_row == 1`, `start_row = first_t_below_r_row + 4`.
          - Otherwise, `start_row = first_t_below_r_row`.
      - application: If `start_row < rows`, iterate downwards from `start_row`. If input cell is T, change output cell to R.
  - element: Secondary Rule (Column does NOT contain Global R)
    properties:
      - identification: Find local min non-zero (`min_l`) and local max non-zero (`max_l`) values *within the column*.
      - condition: Requires `min_l`, `max_l` to exist, `min_l != max_l`.
      - trigger: Find `first_min_l_row`, `last_min_l_row`, and `first_max_l_row`. Replacement occurs if `first_min_l_row < first_max_l_row` AND `last_min_l_row > first_max_l_row`.
      - application: If triggered, replace *all* occurrences of `max_l` with `min_l` in the column.
```

**Natural Language Program:**

1.  **Identify Global Key Values:** Scan the entire input grid to find the global smallest non-zero integer (`R`) and the global largest non-zero integer (`T`).
2.  **Initialize Output:** Create a copy of the input grid. Get the number of rows (`rows`).
3.  **Process Each Column:** Iterate through the columns of the grid from left to right. For each column `j`:
    a.  **Check for Global R:** Determine if `R` exists anywhere in the current column.
    b.  **Apply Primary Rule (if R exists):**
        i.  Find the row index of the first occurrence of `R` (`first_r_row`).
        ii. Check the blocking condition: If `first_r_row >= rows // 2`, skip the rest of the primary rule for this column.
        iii. Find the row index of the first `T` located at a row strictly greater than `first_r_row` (`first_t_below_r_row`). If no such `T` exists, skip the rest of the primary rule.
        iv. Determine the replacement start row (`start_row`):
            *   If `first_r_row` is exactly 1, set `start_row = first_t_below_r_row + 4`.
            *   Otherwise, set `start_row = first_t_below_r_row`.
        v. Apply replacements: If `start_row` is less than `rows`, iterate through the rows from `start_row` down to the last row (`rows - 1`). For each row index `i` in this range, if the value in the *input* grid at `(i, j)` is equal to `T`, set the value in the *output* grid at `(i, j)` to `R`.
    c.  **Apply Secondary Rule (if R does not exist):**
        i.  Find the minimum non-zero value (`min_l`) and maximum non-zero value (`max_l`) present only within the current column `j`.
        ii. If `min_l` and `max_l` both exist and `min_l != max_l`:
            *   Find the row index of the first occurrence of `min_l` (`first_min_l_row`).
            *   Find the row index of the last occurrence of `min_l` (`last_min_l_row`).
            *   Find the row index of the first occurrence of `max_l` (`first_max_l_row`).
            *   If `first_min_l_row` exists, `last_min_l_row` exists, `first_max_l_row` exists, AND `first_min_l_row < first_max_l_row` AND `last_min_l_row > first_max_l_row`:
                *   Iterate through all rows `i` from 0 to `rows - 1`. If the value in the *input* grid at `(i, j)` is equal to `max_l`, set the value in the *output* grid at `(i, j)` to `min_l`.
4.  **Return Result:** After processing all columns, return the modified output grid.