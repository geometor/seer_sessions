Okay, let's analyze the task based on the provided examples.

## Perception of Elements

1.  **Input Structure:** Each input consists of a grid of numbers. A defining feature is a horizontal separator line composed entirely of zeros, dividing the input into two distinct sub-grids: an upper grid (`grid1`) and a lower grid (`grid2`).
2.  **Grid Contents:** Both `grid1` and `grid2` contain numerical values. Within each sub-grid, there appears to be a primary "background" color (the most frequent non-zero digit) and a secondary "foreground" color forming a specific shape or pattern.
3.  **Foreground Shapes:** The core task seems to revolve around identifying and comparing the shapes formed by the foreground colors in `grid1` and `grid2`.
4.  **Output Structure:** The output is either a smaller grid or a single digit `0`.
5.  **Transformation Logic:** The transformation seems conditional based on the comparison of the foreground shapes in `grid1` and `grid2`.
    *   If the shapes (relative patterns, ignoring position and background color) are identical, the output is derived from the shape in `grid1`.
    *   If the shapes are different, the output depends on a property of the shape in `grid1`: whether its bounding box also contains cells of `grid1`'s background color. If it does, the output is derived from `grid1`'s shape; otherwise, the output is `0`.
6.  **Output Generation:** When the output is derived from `grid1`'s shape, it consists of the shape's bounding box. The cells corresponding to `grid1`'s foreground shape retain their color, while all other cells within the bounding box (including any original background cells) become `0`.

## YAML Fact Document


```yaml
task_elements:
  - name: Input Grid
    type: Grid
    properties:
      - Contains numerical digits.
      - Always includes at least one row composed entirely of zeros acting as a separator.
  - name: Grid Separator
    type: Row Property
    properties:
      - Consists solely of the digit 0.
      - Divides the input grid into two sub-grids (Grid1 and Grid2).
  - name: Grid1 (Upper Sub-grid)
    type: Sub-Grid
    properties:
      - Located above the zero separator.
      - Contains a background color (most frequent non-zero digit).
      - Contains a foreground color (another non-zero digit) forming Shape1.
  - name: Grid2 (Lower Sub-grid)
    type: Sub-Grid
    properties:
      - Located below the zero separator.
      - Contains a background color (most frequent non-zero digit, can differ from Grid1's).
      - Contains a foreground color (another non-zero digit, can be same or different from Grid1's) forming Shape2.
  - name: Shape1
    type: Pattern
    properties:
      - Located within Grid1.
      - Defined by the cells containing the foreground color of Grid1.
      - Has a minimal bounding box.
      - Has a relative pattern of foreground cells within its bounding box.
      - May or may not contain cells of Grid1's background color within its bounding box.
  - name: Shape2
    type: Pattern
    properties:
      - Located within Grid2.
      - Defined by the cells containing the foreground color of Grid2.
      - Has a minimal bounding box.
      - Has a relative pattern of foreground cells within its bounding box.
  - name: Output
    type: Grid or Scalar
    properties:
      - Can be a grid derived from Shape1.
      - Can be the single digit 0.

relationships:
  - type: Comparison
    between: [Shape1, Shape2]
    based_on: Relative pattern of foreground cells (ignoring position, background color, and foreground color value).
  - type: Condition
    if: Shape1 pattern equals Shape2 pattern
    then: Output is derived from Shape1.
  - type: Condition
    if: Shape1 pattern differs from Shape2 pattern
    then: Output depends on whether Shape1's bounding box contains Grid1's background color.
      - if_contains_background: Output is derived from Shape1.
      - if_not_contains_background: Output is 0.
  - type: Transformation (Output Generation from Shape1)
    input: Shape1 (bounding box, foreground color, locations of foreground cells)
    output_grid:
      - Dimensions match Shape1's bounding box.
      - Cells corresponding to Shape1's foreground locations retain Shape1's foreground color.
      - All other cells within the bounding box become 0.

actions:
  - Identify the zero separator row(s).
  - Split the input into Grid1 and Grid2.
  - For Grid1: Determine background color, foreground color, and locate Shape1.
  - For Grid2: Determine background color, foreground color, and locate Shape2.
  - Extract the relative pattern of Shape1.
  - Extract the relative pattern of Shape2.
  - Compare the relative patterns.
  - Based on comparison result and properties of Shape1, decide the output type (Shape1-derived grid or 0).
  - If generating Shape1-derived grid: Determine bounding box, map foreground color, fill remaining with 0.
```


## Natural Language Program

1.  **Parse Input:** Identify the row(s) consisting entirely of zeros which separate the input grid into an upper sub-grid (`grid1`) and a lower sub-grid (`grid2`).
2.  **Analyze Grid1:**
    a.  Identify the background color (`bg1`), which is the most frequent non-zero digit in `grid1`.
    b.  Identify the foreground color (`fg1`), which is the non-zero digit in `grid1` that is not `bg1`.
    c.  Determine the locations of all cells containing `fg1`.
    d.  Calculate the minimal bounding box (`bbox1`) that encloses all `fg1` cells.
    e.  Extract the relative pattern (`shape1`) of `fg1` cells within `bbox1` (e.g., as a set of coordinates relative to the top-left of `bbox1`).
3.  **Analyze Grid2:**
    a.  Identify the background color (`bg2`), which is the most frequent non-zero digit in `grid2`.
    b.  Identify the foreground color (`fg2`), which is the non-zero digit in `grid2` that is not `bg2`.
    c.  Determine the locations of all cells containing `fg2`.
    d.  Calculate the minimal bounding box (`bbox2`) that encloses all `fg2` cells.
    e.  Extract the relative pattern (`shape2`) of `fg2` cells within `bbox2`.
4.  **Compare Shapes:** Check if `shape1` is identical to `shape2`.
5.  **Determine Output:**
    a.  **If** `shape1` is identical to `shape2`:
        i.  Create a new grid with the dimensions of `bbox1`.
        ii. Fill the cells corresponding to the `fg1` locations (relative to `bbox1`) with the color `fg1`.
        iii. Fill all other cells in the new grid with `0`.
        iv. This new grid is the output.
    b.  **Else** (`shape1` is different from `shape2`):
        i.  Check if any cell within `bbox1` in the original `grid1` contains the background color `bg1`.
        ii. **If** any such `bg1` cell exists within `bbox1`:
            1. Create a new grid with the dimensions of `bbox1`.
            2. Fill the cells corresponding to the `fg1` locations (relative to `bbox1`) with the color `fg1`.
            3. Fill all other cells in the new grid with `0`.
            4. This new grid is the output.
        iii. **Else** (no `bg1` cells exist within `bbox1`):
            1. The output is the single digit `0`.