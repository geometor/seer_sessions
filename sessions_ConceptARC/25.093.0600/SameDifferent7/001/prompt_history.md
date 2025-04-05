
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 0 4 3 4 0 6 8 6 6 6 6
0 0 3 3 3 0 8 8 8 6 6 6
0 0 4 3 4 0 6 8 6 6 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 3 3 3 3 0 0 7 7 7 7 7
0 3 2 2 3 0 0 7 4 4 7 7
0 3 2 2 3 0 0 7 4 7 7 7
0 3 3 3 3 0 0 7 4 4 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 3 3 3 0 8 8 8 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 9 9 9 9 9
0 0 0 0 0 0 0 9 4 4 4 9
0 1 1 1 1 0 0 9 4 4 9 9
0 1 6 6 1 0 0 9 4 9 9 9
0 1 6 1 1 1 0 9 4 4 4 9
0 1 6 6 1 1 0 9 9 9 9 9
0 1 1 1 1 0 0 0 3 3 3 3
0 0 0 0 7 7 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 7 7 3 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 0 7 7 7 0 3 1 1 3
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0
0 0 5 5 5 5 6 6 6 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 6 6 6 0 0
5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:** The task involves transforming a 2D grid of digits (0-9) into another grid of the same dimensions. The input grids contain distinct regions or "blobs" formed by connected non-zero digits. The output grids are much sparser, retaining only specific digits from certain input blobs. The digit '0' acts as a background color.
*   **Analysis:** The transformation focuses on blobs composed of exactly two distinct non-zero digits. Within such blobs, one digit seems to form an outer layer or border ('outer color'), while the other forms an inner core ('inner color'). The transformation rule isolates and retains only those cells of the 'inner color' that are completely surrounded by other cells belonging to the *same* blob (i.e., cells with either the inner or outer color). Blobs with only one non-zero color or more than two non-zero colors are completely removed (replaced by 0s) in the output. The 'outer color' is typically the one that has cells adjacent to the '0' background, while the 'inner color' does not (or does so to a lesser extent).

*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: Grid
        properties: [2D, Integer Digits (0-9)]
      - type: Background
        properties: [Digit 0]
      - type: Object
        name: Blob
        properties: [Connected Component of Non-Zero Digits, Moore Connectivity (8 directions)]
      - type: Blob Property
        name: Colors
        properties: [Set of unique non-zero digits within the blob]
      - type: Blob Property
        name: Color Count
        properties: [Number of unique non-zero digits]
      - type: Special Blob
        name: Two-Color Blob
        criteria: [Color Count == 2]
        properties:
          - Outer Color: [The color within the blob that has adjacency to the Background (0)]
          - Inner Color: [The color within the blob that is not the Outer Color]
      - type: Cell
        properties: [Row, Column, Digit Value]
      - type: Cell Property
        name: Neighborhood
        properties: [8 adjacent cells (Moore Neighborhood)]
      - type: Cell Condition
        name: Fully Surrounded within Blob
        criteria: [Applies to Inner Color cells in a Two-Color Blob, All 8 neighbors must have either Inner Color or Outer Color]
    actions:
      - Identify Blobs in Input Grid
      - Analyze Colors within each Blob
      - Filter for Two-Color Blobs
      - Identify Inner and Outer Colors for Two-Color Blobs
      - Filter Inner Color cells based on the "Fully Surrounded within Blob" condition
      - Construct Output Grid: Initialize with 0s, place surviving Inner Color cells
    relationships:
      - Blobs are composed of Cells.
      - Cells have Neighbors.
      - Output Grid is derived from Input Grid based on Blob properties and Cell conditions.
      - Only Inner Color cells from Two-Color Blobs that are fully surrounded within their blob appear in the Output Grid.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled with zeros.
    2.  Identify all distinct connected components (blobs) of non-zero cells in the input grid, using 8-directional (Moore) connectivity.
    3.  For each identified blob:
        a.  Determine the set of unique non-zero digits (colors) present within the blob.
        b.  Count the number of unique colors.
        c.  If the count is exactly two, proceed to the next step. Otherwise, ignore this blob (it contributes only zeros to the output).
        d.  Designate the two colors as `color1` and `color2`. Identify which color has at least one cell adjacent (horizontally, vertically, or diagonally) to a background cell (0). Label this color as `C_outer` (outer color) and the other color as `C_inner` (inner color).
        e.  Iterate through all cells `(r, c)` within this blob that contain the `C_inner` color.
        f.  For each such cell `(r, c)`, examine its 8 neighboring cells.
        g.  Check if all 8 neighbors are within the grid boundaries AND contain either the `C_inner` or `C_outer` color.
        h.  If this condition is met (the `C_inner` cell is fully surrounded by cells of the same blob), set the corresponding cell `(r, c)` in the output grid to `C_inner`.
    4.  Return the completed output grid.
