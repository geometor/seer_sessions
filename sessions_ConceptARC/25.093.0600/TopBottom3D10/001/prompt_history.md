
## train_1

**input:**
```
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 3 3 3 3 3 3 3 0 0
1 2 2 2 2 1 0 0 0 0 0 0 3 0 0
1 1 1 1 1 1 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 0 0 0 0 0 0 0 0 0
1 2 3 3 3 3 3 3 3 3 3 3 3 0 0
1 2 3 2 2 1 0 0 0 0 0 0 3 0 0
1 1 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 4 4 4 8 0 0 0 0 0 0
0 6 6 6 6 6 8 4 4 4 8 6 6 6 6 6 0
0 6 0 6 0 6 8 8 8 8 8 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 4 4 4 8 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 6 0 6 0 6 8 6 8 6 8 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of integers.
2.  **Colors/Numbers:** The integers represent different colors or states. The integer 0 consistently appears as a background color, remaining unchanged in the periphery and sometimes within internal areas. Non-zero integers represent distinct colored regions or objects within the grid.
3.  **Objects/Regions:** The non-zero numbers form contiguous or separated regions (shapes). For instance, in `train_1`, there's a region of 1s and 2s, and a region of 3s. In `train_2`, there are regions of 8s, 4s, and 6s.
4.  **Transformation Type:** The transformation modifies the colors of *some* non-zero cells. The background (0) cells seem unaffected. The core shapes generally persist, but boundaries or internal colors change.
5.  **Key Change Pattern:** In both examples, a specific color seems to "expand" or "influence" its neighbors.
    *   In `train_1`, cells colored 1 or 2 that are adjacent (sharing an edge, not just a corner) to a cell colored 3 in the *input* grid become color 3 in the *output* grid.
    *   In `train_2`, cells colored 8 or 4 that are adjacent to a cell colored 6 in the *input* grid become color 6 in the *output* grid.
6.  **Identifying the Influencing Color:** The color causing the change (3 in `train_1`, 6 in `train_2`) appears to be the most frequent non-zero color in the respective input grid.
    *   `train_1`: Frequencies (approx): '3' occurs most often.
    *   `train_2`: Frequencies (approx): '6' occurs most often.

**YAML Facts:**


```yaml
Grid:
  Type: 2D array of integers
Cells:
  Properties:
    - color: integer value
    - position: [row, column]
    - is_background: true if color == 0 else false
Relationships:
  - Orthogonal Adjacency: Cells sharing an edge are neighbors.
Colors:
  - Background: 0
  - Foreground: non-zero integers
  - Dominant Color: The non-zero color with the highest frequency in the input grid.
Transformation:
  Name: Neighbor Influence / Color Spreading
  Input: Grid
  Output: Grid
  Rule: Non-zero cells in the input grid change their color to the Dominant Color if they are orthogonally adjacent to a cell that had the Dominant Color in the input grid.
  Invariants:
    - Background cells (color 0) remain unchanged.
    - Cells with the Dominant Color remain unchanged.
    - Non-zero cells not adjacent to the Dominant Color remain unchanged.
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Identify all unique non-zero colors present in the input grid.
3.  Calculate the frequency (count) of each unique non-zero color within the entire input grid.
4.  Determine the "dominant color" - the non-zero color with the highest frequency.
5.  Create the output grid, initially as an identical copy of the input grid.
6.  Iterate through every cell (`r`, `c`) in the input grid.
7.  For the current cell `Input[r, c]`:
    a.  If its color is 0 (background), skip to the next cell.
    b.  If its color is already the dominant color, skip to the next cell.
    c.  Check all orthogonal neighbors (cells at `[r-1, c]`, `[r+1, c]`, `[r, c-1]`, `[r, c+1]`, ensuring they are within the grid boundaries).
    d.  If *any* of these neighbors in the *input* grid has the dominant color, then change the color of the cell at `[r, c]` in the *output* grid to the dominant color.
8.  Return the modified output grid.
