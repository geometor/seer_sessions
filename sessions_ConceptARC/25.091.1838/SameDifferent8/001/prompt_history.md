
## train_1

**input:**
```
1 1 1 1 1 1 0 2 2 2 2 2 2 2 2
1 4 4 4 4 1 0 2 4 4 4 4 2 2 2
1 4 1 1 4 1 0 2 4 2 2 4 2 2 2
1 4 1 1 4 1 0 2 4 2 2 4 2 2 2
1 4 1 1 4 1 0 2 4 2 2 4 2 2 2
1 4 4 4 4 1 0 2 4 4 4 4 2 2 2
1 1 1 1 1 1 0 2 2 2 2 2 2 2 2
1 1 1 1 1 1 0 2 2 2 2 2 2 2 2
```


**output:**
```
4 4 4 4
4 0 0 4
4 0 0 4
4 0 0 4
4 4 4 4
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 7 8 8 7 7 7 7
7 7 8 8 7 7 7 7
7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3
3 3 3 8 8 8 8 3
3 3 3 8 8 8 8 3
3 3 3 8 8 8 8 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
```


**output:**
```
0
```


## train_3

**input:**
```
2 2 2 2 2 2 1 2 2 2 2 2 2 2
2 2 2 2 2 1 2 1 2 2 2 2 2 2
2 2 2 2 1 2 2 2 1 2 2 2 2 2
2 2 2 2 2 1 2 1 2 2 2 2 2 2
2 2 2 2 2 2 1 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 1 8 8
8 8 8 8 8 8 8 8 8 8 1 8 1 8
8 8 8 8 8 8 8 8 8 1 8 8 8 1
8 8 8 8 8 8 8 8 8 8 1 8 1 8
8 8 8 8 8 8 8 8 8 8 8 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
0 0 1 0 0
0 1 0 1 0
1 0 0 0 1
0 1 0 1 0
0 0 1 0 0
```


## train_4

**input:**
```
9 9 9 9 9 9
9 2 2 2 9 9
9 2 2 2 9 9
9 9 9 9 9 9
9 9 9 9 9 9
0 0 0 0 0 0
5 5 5 5 5 5
5 2 2 5 5 5
5 2 2 5 5 5
5 5 5 5 5 5
```


**output:**
```
0
```

**Perception:**

1.  **Input Structure:** Each input grid is divided into two distinct sections by a single line (row or column) composed entirely of white pixels (0).
2.  **Section Contents:** Each section typically consists of a dominant background color and an internal pattern made of a single, different color (the "inner color"). White pixels (0) act only as separators.
3.  **Comparison:** The core logic involves comparing the two sections, specifically focusing on the inner color and the shape it forms.
4.  **Inner Colors:** In all examples, the *same* inner color appears in both sections (Yellow in 1, Azure in 2, Blue in 3, Red in 4).
5.  **Shape Comparison:** The shapes formed by the inner color in the two sections are compared. "Shape" refers to the relative arrangement of pixels of the inner color.
6.  **Output Determination:**
    *   If the two shapes (formed by the common inner color) are identical, the output is derived from the first section (top or left).
    *   If the two shapes are different, the output depends on the nature of the shape in the *second* section (bottom or right).
7.  **Output Generation:**
    *   When an output pattern is generated (from either the first or second section), it consists of the bounding box of the inner shape. The pixels of the inner color are preserved, while the pixels corresponding to the section's original background color are replaced with white (0).
    *   A special output is a single white pixel (0). This occurs when the shapes are different *and* the shape in the second section is a simple, solid rectangle.

**Facts:**


```yaml
task_structure:
  - description: Input grid is split into two subgrids by a separator line.
    separator:
      type: line (row or column)
      color: white (0)
      thickness: 1 pixel
    subgrids:
      count: 2
      location: Determined by separator orientation (top/bottom or left/right)
      naming: [Subgrid_A (top/left), Subgrid_B (bottom/right)]

subgrid_properties:
  - description: Each subgrid contains objects/colors.
    elements:
      - background_color: The most frequent non-white color in the subgrid.
      - inner_pattern:
          description: A shape formed by a single color different from the background and white.
          color_property: In examples, the inner pattern color is the same in both Subgrid_A and Subgrid_B. Let this be 'inner_color'.
          shape_property: The geometric arrangement of 'inner_color' pixels relative to each other.

comparison_logic:
  - step: 1
    action: Identify the 'inner_color' common to both subgrids.
  - step: 2
    action: Extract the shape formed by 'inner_color' in Subgrid_A (Shape_A) and Subgrid_B (Shape_B).
  - step: 3
    action: Compare Shape_A and Shape_B for identity (identical relative pixel arrangement).

output_rules:
  - condition: Shape_A is identical to Shape_B.
    result: Generate output pattern based on Shape_A.
      - source: Subgrid_A
      - bounding_box: Smallest rectangle containing Shape_A.
      - content:
          - Keep 'inner_color' pixels from Shape_A.
          - Replace Subgrid_A's background_color pixels within the bounding box with white (0).
  - condition: Shape_A is different from Shape_B.
    sub_condition: Check if Shape_B is a solid, filled rectangle.
    results:
      - if_true: Output is a 1x1 grid containing white (0).
      - if_false: Generate output pattern based on Shape_B.
          - source: Subgrid_B
          - bounding_box: Smallest rectangle containing Shape_B.
          - content:
              - Keep 'inner_color' pixels from Shape_B.
              - Replace Subgrid_B's background_color pixels within the bounding box with white (0).

```


**Natural Language Program:**

1.  **Find Separator:** Scan the input grid rows and columns to find a line composed entirely of white (0) pixels. This line separates the grid into two subgrids. Define the subgrid encountered first (top or left) as Subgrid A and the other (bottom or right) as Subgrid B.
2.  **Identify Inner Colors and Shapes:**
    *   In Subgrid A, determine the background color (most frequent non-white) and the inner color (the other non-white color). Extract the shape (relative pixel coordinates) formed by the inner color (Shape A).
    *   In Subgrid B, determine the background color and the inner color. Extract the shape formed by the inner color (Shape B).
    *   Verify that the inner color is the same in both subgrids. If not, the rule is undefined (but assume it is the same based on examples). Let the common inner color be `C`.
3.  **Compare Shapes:** Check if Shape A and Shape B are identical (same pattern of `C` pixels relative to their top-left corners).
4.  **Determine Output Based on Comparison:**
    *   **If Shape A and Shape B are identical:**
        a.  Find the minimum bounding box containing Shape A within Subgrid A.
        b.  Create an output grid matching the size of this bounding box.
        c.  Fill the output grid: For each position within the bounding box, if the corresponding pixel in Subgrid A is the inner color `C`, place `C` in the output. Otherwise, place white (0).
    *   **If Shape A and Shape B are different:**
        a.  Determine if Shape B constitutes a solid, filled rectangle (a rectangular block of color `C` with no holes or missing internal pixels).
        b.  **If Shape B is a solid rectangle:** The output is a 1x1 grid containing only white (0).
        c.  **If Shape B is NOT a solid rectangle:**
            i.  Find the minimum bounding box containing Shape B within Subgrid B.
            ii. Create an output grid matching the size of this bounding box.
            iii. Fill the output grid: For each position within the bounding box, if the corresponding pixel in Subgrid B is the inner color `C`, place `C` in the output. Otherwise, place white (0).
5.  **Return Output:** Return the generated output grid.
