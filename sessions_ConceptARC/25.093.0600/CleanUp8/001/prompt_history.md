
## train_1

**input:**
```
2 2 0 0 0 0 0 0 0 0
6 2 0 0 3 0 0 1 0 0
0 0 1 6 0 0 0 0 0 0
0 0 1 1 0 0 6 0 0 6
0 0 0 0 3 3 0 0 0 0
0 3 0 0 3 3 0 1 0 0
0 0 0 0 0 3 4 4 0 0
0 1 0 0 7 0 4 6 0 0
7 0 0 0 0 0 0 0 5 5
0 0 0 0 3 0 0 0 7 5
```


**output:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 5 5
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 4 3
0 6 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 4 0 0 6 7 0 0
4 0 0 0 6 6 0 0 0 0
0 1 0 0 6 8 0 0 0 0
0 0 5 5 0 0 0 0 6 0
0 0 1 5 0 0 6 0 0 0
9 9 0 0 0 0 0 0 0 1
8 9 0 0 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (arrays) of integers. The size appears constant (10x10 in the examples).
2.  **Core Transformation:** The transformation modifies the input grid row by row, but the logic seems to depend on pairs of consecutive rows.
3.  **Row Pairing:** The grid is processed in pairs of adjacent rows: (row 0, row 1), (row 2, row 3), (row 4, row 5), and so on.
4.  **Pattern Selection:** Within each pair, one of the two rows is chosen as a 'pattern' row.
5.  **Selection Criterion:** The selection appears based on the number of non-zero elements in each row within the pair. The row with fewer non-zero elements is selected.
6.  **Tie-breaking:** If both rows in a pair have the same count of non-zero elements, the first row of the pair (the one with the even index) is selected as the pattern.
7.  **Output Generation:** Once the pattern row is selected for a pair, *both* corresponding rows in the output grid become identical copies of that selected pattern row.

**Facts:**


```yaml
Task: Grid Transformation by Row Pair Sparsity Comparison

Objects:
  - InputGrid: A 2D array of integers.
  - OutputGrid: A 2D array of integers, derived from InputGrid.
  - Row: A 1D array of integers representing a horizontal line in the grid.
  - RowPair: Two consecutive rows from the InputGrid (e.g., Row 2k and Row 2k+1).
  - Cell: An individual element within a Row/Grid containing an integer value.

Properties:
  - Row:
    - index: The vertical position (0-indexed).
    - values: The sequence of integers in the row.
    - non_zero_count: The number of cells in the row with a value not equal to 0.
  - RowPair:
    - first_row: The row with the even index (2k).
    - second_row: The row with the odd index (2k+1).
    - pattern_row: The selected row from the pair based on the comparison rule.

Actions:
  - Iterate: Process the InputGrid row pairs sequentially.
  - CountNonZeros: Calculate the non_zero_count for a given Row.
  - CompareCounts: Compare the non_zero_count of the first_row and second_row in a RowPair.
  - SelectPattern: Choose one row from the RowPair based on the comparison result (fewer non-zeros wins; first row wins ties).
  - CopyRow: Duplicate the values of the selected pattern_row.
  - AssignOutput: Set both corresponding rows in the OutputGrid to be copies of the pattern_row for that pair.

Relationships:
  - OutputGrid dimensions are the same as InputGrid dimensions.
  - OutputGrid rows at indices 2k and 2k+1 are both determined solely by the InputGrid rows at indices 2k and 2k+1.
  - The pattern_row is selected based on having the minimum non_zero_count within the RowPair (with tie-breaking favoring the first_row).
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Iterate through the rows of the input grid using a step of 2, considering pairs of rows (row `i` and row `i+1`) where `i` is an even number (0, 2, 4, ... up to the second-to-last row).
3.  For each pair of rows (let's call them `row_A` at index `i` and `row_B` at index `i+1`):
    a.  Count the number of non-zero elements in `row_A`.
    b.  Count the number of non-zero elements in `row_B`.
    c.  Compare the counts:
        i.  If `row_A` has strictly fewer non-zero elements than `row_B`, select `row_A` as the `pattern_row`.
        ii. If `row_B` has strictly fewer non-zero elements than `row_A`, select `row_B` as the `pattern_row`.
        iii. If both rows have the same number of non-zero elements, select `row_A` (the first row of the pair) as the `pattern_row`.
    d.  Copy the selected `pattern_row` into the output grid at both index `i` and index `i+1`.
4.  Return the completed output grid.
