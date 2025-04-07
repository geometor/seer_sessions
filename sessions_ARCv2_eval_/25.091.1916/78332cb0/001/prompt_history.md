
## train_1

**input:**
```
7 7 7 7 7 6 7 4 7 7 7
7 7 7 7 7 6 7 4 4 4 7
7 7 7 7 7 6 7 7 7 4 7
7 2 2 2 7 6 7 7 7 4 7
7 7 2 7 7 6 7 7 7 4 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 1 7 6 7 7 3 7 7
7 1 1 1 7 6 7 3 3 7 7
7 1 1 1 7 6 7 3 7 7 7
7 1 1 1 7 6 7 3 7 7 7
7 7 7 7 7 6 7 3 7 7 7
```


**output:**
```
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 2 2 2 7
7 7 2 7 7
6 6 6 6 6
7 7 3 7 7
7 3 3 7 7
7 3 7 7 7
7 3 7 7 7
7 3 7 7 7
6 6 6 6 6
7 4 7 7 7
7 4 4 4 7
7 7 7 4 7
7 7 7 4 7
7 7 7 4 7
6 6 6 6 6
7 7 7 1 7
7 1 1 1 7
7 1 1 1 7
7 1 1 1 7
7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7
7 7 8 8 7
7 7 8 8 7
8 8 8 7 7
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
2 2 2 7 7
7 7 2 2 7
7 7 7 2 2
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
7 9 7 9 9
7 9 9 9 7
7 9 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
7 9 7 9 9 6 2 2 2 7 7 6 7 7 8 8 7
7 9 9 9 7 6 7 7 2 2 7 6 7 7 8 8 7
7 9 7 7 7 6 7 7 7 2 2 6 8 8 8 7 7
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 6 7 7 1 7 7 6 7 7 9 7 7
7 8 8 8 7 6 7 7 1 7 7 6 7 9 9 9 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
```


**output:**
```
7 7 7 7 7
7 8 8 8 7
7 7 8 7 7
7 7 8 7 7
7 7 8 7 7
6 6 6 6 6
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
6 6 6 6 6
7 7 9 7 7
7 9 9 9 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
```

Okay, let's break down this task.

**Perception**

1.  **Input Structure:** The input grids contain smaller, distinct square patterns (subgrids, typically 5x5) composed of various colors against a white (7) background.
2.  **Separators:** These subgrids are separated by lines or columns of magenta (6). These separators can be horizontal, vertical, or both (forming a cross).
3.  **Transformation Goal:** The core task is to rearrange these subgrids based on the orientation of the magenta separators. The separators themselves are transformed (from vertical to horizontal, or vice-versa) or standardized (in the cross case).
4.  **Arrangement Logic:**
    *   If the input has **vertical** magenta separators (subgrids arranged horizontally), the output stacks the subgrids **vertically**, separated by horizontal magenta lines. The order is preserved (leftmost input subgrid becomes topmost output subgrid).
    *   If the input has **horizontal** magenta separators (subgrids arranged vertically), the output arranges the subgrids **horizontally**, separated by vertical magenta columns. The order is reversed (topmost input subgrid becomes rightmost output subgrid).
    *   If the input has **both** horizontal and vertical magenta separators (forming a cross), the output stacks the subgrids **vertically**, separated by horizontal magenta lines. The order follows a specific pattern: top-left, bottom-left, top-right, bottom-right from the input grid quadrants.
5.  **Subgrid Integrity:** The content (pixels) within each subgrid remains unchanged during the transformation.
6.  **Output Separators:** The separators in the output grid are always single lines/columns of magenta (6), matching the new arrangement (horizontal lines for vertical stacking, vertical columns for horizontal arrangement).

**Facts**


```yaml
task_type: rearrangement
components:
  - type: grid
    properties:
      - contains_subgrids
      - contains_separators
  - type: subgrid
    properties:
      - composed_of_pixels_other_than_separator_color
      - typically_square_(5x5_in_examples)
      - background_color_is_white_(7)
      - maintains_internal_pattern_during_transformation
  - type: separator
    properties:
      - color_is_magenta_(6)
      - can_be_horizontal_line
      - can_be_vertical_column
      - can_be_both_(cross_shape)
      - divides_grid_into_regions_containing_subgrids
      - determines_output_arrangement_and_separator_orientation
relationships:
  - separator_divides_grid_into_subgrids
  - input_separator_orientation_determines_output_arrangement
actions:
  - identify_separator_type (horizontal, vertical, or both)
  - extract_subgrids based on separators
  - rearrange_subgrids according to rules based on separator type
  - construct_output_grid with rearranged subgrids and new separators
rules:
  - rule:
      condition: input_separator_is_vertical
      action: stack_subgrids_vertically_in_output
      order: preserve_left_to_right_order
      output_separator: horizontal_magenta_line
  - rule:
      condition: input_separator_is_horizontal
      action: arrange_subgrids_horizontally_in_output
      order: reverse_top_to_bottom_order
      output_separator: vertical_magenta_column
  - rule:
      condition: input_separators_are_horizontal_and_vertical (cross)
      action: stack_subgrids_vertically_in_output
      order: top_left, bottom_left, top_right, bottom_right
      output_separator: horizontal_magenta_line
```


**Natural Language Program**

1.  Analyze the input grid to identify the presence and orientation of magenta (6) lines or columns that fully span the grid's height or width, acting as separators.
2.  **Case 1: Vertical Separator(s) Found:**
    a.  Identify the subgrids located between the vertical separators (and grid edges).
    b.  Extract these subgrids in order from left to right.
    c.  Construct the output grid by stacking these extracted subgrids vertically, in the same order they were extracted.
    d.  Insert a single horizontal line of magenta (6) pixels between each stacked subgrid.
3.  **Case 2: Horizontal Separator(s) Found:**
    a.  Identify the subgrids located between the horizontal separators (and grid edges).
    b.  Extract these subgrids in order from top to bottom.
    c.  Construct the output grid by arranging these extracted subgrids horizontally, in the *reverse* order (bottommost subgrid becomes leftmost, topmost becomes rightmost).
    d.  Insert a single vertical column of magenta (6) pixels between each horizontally arranged subgrid.
4.  **Case 3: Both Horizontal and Vertical Separators Found (Cross Shape):**
    a.  Identify the four subgrids located in the quadrants defined by the separators: Top-Left (TL), Bottom-Left (BL), Top-Right (TR), Bottom-Right (BR).
    b.  Extract these subgrids.
    c.  Construct the output grid by stacking these extracted subgrids vertically in the specific order: TL, BL, TR, BR.
    d.  Insert a single horizontal line of magenta (6) pixels between each stacked subgrid.
5.  Ensure the dimensions of the output grid correctly accommodate the rearranged subgrids and the new separators. The content within each subgrid remains unchanged.
