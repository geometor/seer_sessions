
## train_1

**input:**
```
2 0 0 0 0 2
0 0 0 0 0 0
0 0 0 0 0 0
2 0 0 0 0 2
```


**output:**
```
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
```


## train_2

**input:**
```
2 0 0 0 0 2
0 2 0 0 2 0
0 0 2 2 0 0
0 2 0 0 2 0
```


**output:**
```
2 0 0 0 0 2
0 2 0 0 2 0
0 0 2 2 0 0
0 2 0 0 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0
0 2 0 0 2 0
2 0 0 0 0 2
0 2 0 0 2 0
```


**output:**
```
0 0 0 0 0 0
0 2 2 2 2 0
2 0 0 0 0 2
0 2 2 2 2 0
```


## train_4

**input:**
```
0 0 2 2 0 0
0 2 0 0 2 0
2 0 0 0 0 2
0 2 0 0 2 0
```


**output:**
```
0 0 2 2 0 0
0 2 0 0 2 0
2 0 0 0 0 2
0 2 0 0 2 0
```


## train_5

**input:**
```
2 0 0 0 0 2
0 2 0 0 2 0
0 2 0 0 2 0
2 0 0 0 0 2
```


**output:**
```
2 0 0 0 0 2
0 2 2 2 2 0
0 2 2 2 2 0
2 0 0 0 0 2
```

Okay, let's analyze the transformation logic.

## Perception

1.  **Grid Structure:** The input and output are 2D grids containing integers 0 and 2. The grid dimensions vary slightly in examples but maintain a structure (4 rows, 6 columns in all provided examples).
2.  **Core Operation:** The fundamental change observed is the conversion of some '0' cells to '2' cells. '2' cells never change to '0'.
3.  **Row-Based Patterns:** The changes appear to be conditional based on specific patterns within individual rows. Two key patterns emerge involving rows containing exactly two '2's:
    *   Pattern 1 (P1): '2's at the absolute start and end of the row, with '0's in between (e.g., `[2, 0, 0, 0, 0, 2]`).
    *   Pattern 2 (P2): '2's at the second and second-to-last positions, with '0's elsewhere (e.g., `[0, 2, 0, 0, 2, 0]`).
4.  **Global Conditionality:** Whether a row fitting P1 or P2 is actually modified depends on the composition of the *entire grid*. The presence of rows with '2's that *don't* fit P1 or P2 (Other Patterns, OP) seems to inhibit *any* modification (Examples: train\_2, train\_4).
5.  **Rule Hierarchy:** When modifications *are* allowed (i.e., no OP rows exist):
    *   If *only* P1 rows (and potentially all-'0' rows) are present, the P1 rows are filled (train\_1).
    *   If *both* P1 and P2 rows are present, *only* the P2 rows are filled (train\_3, train\_5).
    *   (Implicitly) If *only* P2 rows (and potentially all-'0' rows) are present, the P2 rows would be filled.
6.  **Filling Mechanism:** When a row pattern (P1 or P2) is selected for modification, all the '0' cells strictly *between* the two '2's defining the pattern are changed to '2'.

## YAML Facts


