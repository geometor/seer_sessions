
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
7 0 0 0 0 0 7
0 7 0 0 0 7 0
0 0 7 0 7 0 0
0 0 0 7 0 0 0
0 0 7 0 7 0 0
0 7 0 0 0 7 0
7 0 0 0 0 0 7
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 7 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
7 0 0 0 7 0
0 7 0 7 0 0
0 0 7 0 0 0
0 7 0 7 0 0
7 0 0 0 7 0
0 0 0 0 0 7
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 7 0 7 0 0
0 0 0 7 0 0 0 7 0
0 0 7 0 0 0 0 0 7
0 7 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 7 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
7 0 0 0 7
0 7 0 7 0
0 0 7 0 0
0 7 0 7 0
7 0 0 0 7
```

Okay, let's break down this task.

**Perception of the Elements:**

1.  **Input Grid:** Each input grid contains a single non-white pixel, which is always orange (value 7), placed somewhere within the grid. The rest of the grid is white (value 0). The size of the input grid varies across examples.
2.  **Output Grid:** The output grid has the same dimensions as its corresponding input grid. It contains the original orange pixel from the input, plus several additional orange pixels. The remaining pixels are white.
3.  **Transformation Pattern:** The added orange pixels in the output grid form a distinct pattern relative to the original orange pixel. They lie along the two main diagonal lines that intersect at the position of the original orange pixel. These diagonals extend outwards from the center point (the original pixel) to the edges of the grid.

**YAML Facts:**


```yaml
task_description: "Draw two diagonal lines (an 'X' shape) passing through a single given pixel."
grid_properties:
  size_relation: "Output grid has the same dimensions as the input grid."
objects:
  - object_name: "marker_pixel"
    description: "The single non-white pixel in the input grid."
    properties:
      color: "orange (7)"
      count: 1
      location: "Variable, defines the center of the output pattern."
  - object_name: "background"
    description: "The uniform background color."
    properties:
      color: "white (0)"
  - object_name: "diagonal_pattern"
    description: "The pattern drawn in the output grid."
    properties:
      shape: "Two intersecting diagonal lines ('X' shape)."
      color: "orange (7)"
      center: "Located at the position of the input marker_pixel."
      extent: "Lines extend from the center to the grid boundaries."
relationships:
  - relation: "identity"
    objects: ["marker_pixel"]
    description: "The marker_pixel from the input is preserved at the same location in the output grid."
  - relation: "generation"
    objects: ["marker_pixel", "diagonal_pattern"]
    description: "The location of the marker_pixel determines the center and placement of the diagonal_pattern in the output grid."
    rule: "A pixel at (row, col) is part of the diagonal_pattern if its coordinates relative to the marker_pixel's coordinates (center_row, center_col) satisfy either (row - center_row) == (col - center_col) OR (row - center_row) == -(col - center_col)."
```


**Natural Language Program:**

1.  Identify the location (row `R`, column `C`) of the single orange pixel in the input grid.
2.  Create a new output grid with the same height and width as the input grid, filled entirely with white pixels.
3.  Iterate through every possible cell coordinate (`r`, `c`) within the bounds of the grid dimensions.
4.  For each cell (`r`, `c`), check if it satisfies either of the following conditions based on the identified location (`R`, `C`):
    *   Condition 1 (main diagonal): The difference in rows (`r - R`) is equal to the difference in columns (`c - C`).
    *   Condition 2 (anti-diagonal): The difference in rows (`r - R`) is equal to the negative of the difference in columns (`-(c - C)`), which is equivalent to `r + c == R + C`.
5.  If either Condition 1 or Condition 2 is true for the cell (`r`, `c`), set the color of that cell in the output grid to orange.
6.  After checking all cells, the resulting output grid is complete.
