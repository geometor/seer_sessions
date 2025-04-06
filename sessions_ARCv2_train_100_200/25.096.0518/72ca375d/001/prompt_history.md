
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4
4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6
0 6 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 5
5 5 5 5
```

Okay, I will analyze the provided examples to understand the transformation task.

**Perception of Elements:**

1.  **Input:** A 10x10 grid of single digits (0-9). The non-zero digits form distinct, potentially overlapping or adjacent, connected shapes or "objects". 0 represents the background.
2.  **Output:** A smaller rectangular grid containing digits.
3.  **Objects:** Within the input grid, contiguous blocks of the same non-zero digit can be considered as distinct objects.
4.  **Transformation:** The core task seems to involve identifying one specific object from the input grid based on some criteria and then extracting a representation of that object as the output.
5.  **Extraction Logic:** The output grid appears to correspond to the bounding box of the selected object. Within this bounding box, cells matching the selected object's digit retain their value, while all other cells (including background 0s and potentially parts of other objects falling within the bounding box) are set to 0 in the output.
6.  **Selection Criteria:** The critical step is determining *which* object is selected. Analyzing the examples:
    *   In `train_1`, the object made of '4' is selected. Its bounding box is 2x2, area 4, and it contains 4 cells (density 4/4 = 1.0). Other objects ('8', '2') have lower densities (5/6, 6/10 respectively).
    *   In `train_2`, the object made of '6' is selected. Its bounding box is 2x4, area 8, and it contains 6 cells (density 6/8 = 0.75). Other objects ('2', '7') have lower densities (5/8, 4/6 respectively).
    *   In `train_3`, the object made of '5' is selected. Its bounding box is 2x4, area 8, and it contains 6 cells (density 6/8 = 0.75). Other objects ('3', '8') have lower densities (4/6, 9/14 respectively).
    *   The pattern suggests selecting the object with the highest "density", calculated as the number of cells in the object divided by the area of its bounding box.

**Facts (YAML):**


```yaml
InputType: Grid
InputProperties:
  - Size: 10x10
  - Cells: Contain single digits (0-9)
  - Background: Represented by digit 0
  - Objects: Formed by connected non-zero cells of the same digit

OutputType: Grid
OutputProperties:
  - Size: Variable, smaller than input
  - Cells: Contain single digits (0 or the digit of the selected object)

Transformation: Object Selection and Extraction

SelectionCriteria:
  - Identify all distinct connected non-zero objects.
  - For each object:
      - Calculate its size (number of cells).
      - Determine its bounding box.
      - Calculate the area of its bounding box.
      - Calculate its density (size / area).
  - Select the object with the maximum density.
  - (Assumption: No ties in maximum density in provided examples; if ties occur, a secondary rule like smallest bounding box area or top-left position might be needed).

ExtractionSteps:
  - Get the bounding box (min_row, max_row, min_col, max_col) and digit (D) of the selected object.
  - Create an output grid with dimensions (max_row - min_row + 1) x (max_col - min_col + 1).
  - Iterate through the cells (r, c) within the bounding box range in the input grid.
  - If input[r][c] == D, set output[r - min_row][c - min_col] = D.
  - Otherwise, set output[r - min_row][c - min_col] = 0.

Relationships:
  - The output grid is derived from a sub-region (bounding box) of the input grid.
  - The content of the output grid depends on the single object selected based on the maximum density criterion.
```


**Natural Language Program:**

1.  Parse the input grid to identify all distinct connected groups of identical non-zero digits (these are the "objects").
2.  For each identified object:
    a.  Count the number of cells belonging to the object (its `size`).
    b.  Find the minimum and maximum row and column indices occupied by the object's cells to determine its `bounding_box`.
    c.  Calculate the `area` of the bounding box (height * width).
    d.  Calculate the `density` of the object (`size` / `area`).
3.  Find the object that has the highest `density` among all objects. Let this be the `selected_object` and its digit be `selected_digit`.
4.  Determine the `bounding_box` of the `selected_object` (min_row, max_row, min_col, max_col).
5.  Create a new output grid with dimensions `(max_row - min_row + 1)` rows and `(max_col - min_col + 1)` columns.
6.  Iterate through each row `r` from `min_row` to `max_row` and each column `c` from `min_col` to `max_col` of the input grid.
7.  For each input cell `input[r][c]`:
    a.  If `input[r][c]` is equal to the `selected_digit`, set the corresponding cell in the output grid `output[r - min_row][c - min_col]` to `selected_digit`.
    b.  Otherwise, set the output grid cell `output[r - min_row][c - min_col]` to 0.
8.  Return the generated output grid.
