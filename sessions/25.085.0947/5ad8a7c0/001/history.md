
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

Okay, let's analyze the task examples.

**Perception**

1.  **Grid Structure:** All examples use a 4x6 grid.
2.  **Colors:** Only two colors are present: red (2) and white (0).
3.  **Transformation:** The core transformation involves changing some white pixels (0) to red (2). No red pixels change to white, and the grid size remains constant.
4.  **Row-based Operation:** The changes seem to happen within individual rows. Specifically, it looks like horizontal segments between pairs of red pixels are being filled.
5.  **Pair Identification:** The crucial element appears to be rows containing exactly two red pixels. Let's call these "pair rows".
6.  **Types of Pairs:** There are two types of pairs observed:
    *   **Edge Pairs:** The two red pixels are at the very ends of the row (column 0 and column 5).
    *   **Internal Pairs:** The two red pixels are *not* at the ends of the row.
7.  **Conditional Filling:** The filling doesn't always happen for every pair row. The decision to fill seems dependent on the overall configuration of edge pairs and internal pairs across the entire grid, and in one case, the content of the first row.
    *   If the edge pairs are specifically in rows 0 and 3: filling occurs either on the edge pair rows themselves (if no internal pairs exist) or on the internal pair rows (if they do exist).
    *   If the only edge pair is in row 2: filling occurs on the internal pair rows *only if* row 0 is entirely white.
    *   If the only edge pair is in row 0: no filling occurs.

**Facts**


```yaml
Grid:
  - dimensions: constant 4x6 for all examples
  - colors: [white (0), red (2)]

Objects:
  - type: Pixel
    properties:
      - color: white (0) or red (2)
      - location: (row, column)
  - type: Row
    properties:
      - index: 0 to 3
      - pixels: sequence of 6 pixels
      - classification:
          - HasPair: contains exactly two red pixels
          - IsEdgePair: HasPair is true AND red pixels are at col 0 and col 5
          - IsInternalPair: HasPair is true AND red pixels are NOT at col 0 and col 5

Relationships:
  - Set_EdgePairRows: The set of row indices where IsEdgePair is true.
  - Set_InternalPairRows: The set of row indices where IsInternalPair is true.
  - Input_Row0_Content: The specific pixel values in row 0 of the input grid.

Transformation:
  - name: Conditional Horizontal Fill
  - input: Input Grid
  - output: Output Grid (initially a copy of input)
  - condition: Determined by Set_EdgePairRows and Set_InternalPairRows, and potentially Input_Row0_Content.
      - IF Set_EdgePairRows == {0, 3}:
          - IF Set_InternalPairRows is empty: TargetRows = Set_EdgePairRows
          - ELSE: TargetRows = Set_InternalPairRows
      - ELIF Set_EdgePairRows == {2}:
          - IF Input_Row0_Content is all white (0): TargetRows = Set_InternalPairRows
          - ELSE: TargetRows = {}
      - ELIF Set_EdgePairRows == {0}: TargetRows = {}
      - ELSE (all other configurations): TargetRows = {}
  - action:
      - For each row_index in TargetRows:
          - Find column indices c1, c2 of the two red pixels in the input row at row_index (c1 < c2).
          - In the output grid's row at row_index, set all pixels from column c1 to c2 (inclusive) to red (2).
```


**Natural Language Program**

1.  Create the output grid as an identical copy of the input grid.
2.  Examine each row of the input grid to find rows containing exactly two red pixels.
3.  Identify the set of row indices corresponding to "Edge Pair Rows" (where the two red pixels are in column 0 and column 5).
4.  Identify the set of row indices corresponding to "Internal Pair Rows" (where the two red pixels are present but not in columns 0 and 5).
5.  Determine the set of "Target Rows" to be filled based on the following logic:
    a.  If the Edge Pair Rows are exactly row 0 and row 3:
        i.  If there are no Internal Pair Rows, the Target Rows are row 0 and row 3.
        ii. If there are Internal Pair Rows, the Target Rows are the Internal Pair Rows.
    b.  If the only Edge Pair Row is row 2:
        i.  Check if row 0 of the *input* grid consists entirely of white pixels.
        ii. If row 0 is all white, the Target Rows are the Internal Pair Rows.
        iii. If row 0 contains any red pixels, there are no Target Rows.
    c.  If the only Edge Pair Row is row 0: There are no Target Rows.
    d.  In all other configurations of Edge Pair Rows and Internal Pair Rows, there are no Target Rows.
6.  For each row index in the determined set of Target Rows:
    a.  Locate the column indices, `c1` and `c2`, of the two red pixels within that row in the input grid (ensure `c1` is less than `c2`).
    b.  Modify the corresponding row in the output grid by changing the color of all pixels from column `c1` to `c2` (inclusive) to red.
7.  The final modified grid is the result.
