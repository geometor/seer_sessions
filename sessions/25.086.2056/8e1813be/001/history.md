
## train_1

**input:**
```
0 0 0 0 0 2 0 0 4 0
0 5 5 5 0 2 0 0 4 0
0 5 5 5 0 2 0 0 4 0
0 5 5 5 0 2 0 0 4 0
0 0 0 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
```


**output:**
```
1 2 4
1 2 4
1 2 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 4 4 4 4 4 4 4
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 8 8 8 8 8 8 8
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```


**output:**
```
2 2 2 2 2 2
1 1 1 1 1 1
3 3 3 3 3 3
4 4 4 4 4 4
8 8 8 8 8 8
6 6 6 6 6 6
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 5 5 5 5 0 2
0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 5 5 5 5 0 0
8 8 8 8 8 0 5 5 5 5 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2
8 8 8 8
4 4 4 4
1 1 1 1
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input:** The inputs are grids containing various colored pixels. Common elements include:
    *   A white background (color 0).
    *   One or more distinct colored shapes (lines, rectangles).
    *   Sometimes gray shapes (color 5) are present.
2.  **Output:** The outputs are smaller, square grids.
    *   Each output grid contains only the non-white, non-gray colors found in the input shapes.
    *   The size of the output grid (NxN) corresponds to the number (N) of unique non-white, non-gray colors in the input.
    *   The arrangement of colors in the output depends on the orientation of the shapes in the input.
3.  **Transformation:** The core transformation involves:
    *   Identifying the relevant colors (excluding white and gray).
    *   Determining the order of these colors based on their position (top-to-bottom, then left-to-right) in the input grid.
    *   Detecting the dominant orientation of the colored shapes (primarily vertical or primarily horizontal/mixed).
    *   Constructing a square output grid whose size matches the number of relevant colors.
    *   Filling the output grid row-wise or column-wise based on the detected orientation and the determined color order.

**YAML Fact Document:**


```yaml
task_context:
  - The task involves extracting specific colors from an input grid and arranging them into a smaller, square output grid.
  - Background color (white, 0) and gray color (5) are consistently ignored during color extraction.

input_elements:
  - type: grid
  - properties:
      - contains pixels of various colors (0-9)
      - features identifiable objects (contiguous blocks of non-background color)
      - objects can be lines (horizontal/vertical) or rectangles.
      - gray objects may be present but are irrelevant to the output colors.

output_elements:
  - type: grid
  - properties:
      - always square (NxN)
      - N equals the count of unique, non-white, non-gray colors in the input.
      - contains only the unique, non-white, non-gray colors from the input.
      - colors are arranged either in rows or columns.

transformation_rules:
  - action: identify_colors
    - description: Find all unique pixel colors in the input grid, excluding white (0) and gray (5).
    - result: a set of relevant colors.
  - action: determine_order
    - description: Order the relevant colors based on their first appearance in the input grid (minimum row index first, then minimum column index as a tie-breaker).
    - result: an ordered list of colors.
  - action: detect_orientation
    - description: Analyze the shapes formed by the relevant colors. If all shapes are predominantly vertical (height >= width), the orientation is 'vertical'. Otherwise, it's 'horizontal'.
    - input: shapes/objects corresponding to relevant colors.
    - result: 'vertical' or 'horizontal'.
  - action: construct_output
    - description: Create a square grid of size NxN, where N is the number of relevant colors.
    - input: N (count of relevant colors).
    - result: an empty NxN grid.
  - action: populate_output
    - description: Fill the output grid based on the determined orientation and color order.
    - input: empty NxN grid, ordered list of colors, orientation.
    - rule_if_vertical: Fill the j-th column entirely with the j-th color from the ordered list.
    - rule_if_horizontal: Fill the i-th row entirely with the i-th color from the ordered list.
    - result: the final output grid.

relationships:
  - The size of the output grid is directly determined by the count of unique relevant colors in the input.
  - The order of colors in the output depends on the spatial order (top-to-bottom, left-to-right) of their first appearance in the input.
  - The arrangement pattern (rows vs. columns) in the output depends on the geometric orientation (vertical vs. horizontal/mixed) of the colored shapes in the input.
```


**Natural Language Program:**

1.  Scan the input grid to find all unique colors present, ignoring white (0) and gray (5). Let N be the count of these unique relevant colors.
2.  For each relevant color, find the coordinate (row, column) of its first appearance in the input grid (scanning top-to-bottom, then left-to-right).
3.  Sort the relevant colors based on these first appearance coordinates (primarily by row index, secondarily by column index).
4.  Identify all contiguous objects formed by the relevant colors in the input grid.
5.  Determine the overall orientation: Check if *every* identified object has a height greater than or equal to its width. If this condition is true for all objects, the orientation is 'Vertical'. Otherwise, the orientation is 'Horizontal'.
6.  Create a new square grid of size N x N.
7.  If the orientation is 'Vertical', then for each color `C` at index `j` (0-based) in the sorted list, fill the entire `j`-th column of the output grid with color `C`.
8.  If the orientation is 'Horizontal', then for each color `C` at index `i` (0-based) in the sorted list, fill the entire `i`-th row of the output grid with color `C`.
9.  Return the generated N x N grid.
