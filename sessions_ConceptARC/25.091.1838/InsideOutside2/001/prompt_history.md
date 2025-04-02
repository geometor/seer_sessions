
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the examples provided for this task.

**Perception of Elements:**

1.  **Grid Structure:** Both input and output are 10x10 grids.
2.  **Colors:** The primary colors involved are white (0 - background), red (2), and yellow (4).
3.  **Objects:** The colored elements are individual pixels (1x1 objects).
4.  **Input Composition:** Each input grid contains exactly two red pixels and one yellow pixel, scattered on a white background.
5.  **Output Composition:** Each output grid contains *either* the two red pixels *or* the one yellow pixel from the input, with the other color removed (changed to white). The positions of the kept pixels remain unchanged.
6.  **Transformation:** The core transformation involves selecting which color (red or yellow) to keep based on some condition, and removing the pixels of the other color.

**Key Observation & Hypothesis:**

The decision of whether to keep red or yellow seems to depend on the relative arrangement of the *red* pixels (the color that appears more frequently in the input).

*   In `train_1` and `train_4`, the two red pixels are aligned horizontally (share the same row). In these cases, the red pixels are kept, and the yellow pixel is removed.
*   In `train_2` and `train_3`, the two red pixels are *not* aligned either horizontally or vertically. In these cases, the yellow pixel is kept, and the red pixels are removed.

This suggests a rule based on the alignment of the most frequent color.

**YAML Fact Documentation:**


```yaml
task_context:
  grid_size: fixed (10x10 for all examples)
  colors_present:
    - white (0): background
    - red (2)
    - yellow (4)
  input_pattern: Contains exactly 2 red pixels and 1 yellow pixel.
  output_pattern: Contains either the 2 red pixels or the 1 yellow pixel from the input; the other color is removed (replaced by white).

objects:
  - type: pixel
    color: red (2)
    count_in_input: 2
    properties:
      - position (row, col)
  - type: pixel
    color: yellow (4)
    count_in_input: 1
    properties:
      - position (row, col)

relationships_and_conditions:
  - type: count_comparison
    color_1: red
    color_2: yellow
    result: count(red) > count(yellow) (in all examples)
  - type: spatial_alignment
    description: Check alignment of the pixels of the most frequent color (red).
    condition: Are all red pixels in the same row OR in the same column?
    values:
      - train_1: Yes (row 2)
      - train_2: No
      - train_3: No
      - train_4: Yes (row 0)

actions:
  - name: select_color_to_keep
    based_on: alignment of the most frequent color (red)
    rule:
      - if red pixels are aligned (horizontally or vertically): keep red
      - if red pixels are not aligned: keep yellow
  - name: remove_other_color
    description: Change pixels of the non-selected color to white (0).
    target: pixels of the color not selected in the previous step.

transformation_summary:
  The transformation identifies the most frequent color (red) and checks if its pixels are aligned horizontally or vertically.
  If aligned, keep the red pixels and remove the yellow pixel.
  If not aligned, keep the yellow pixel and remove the red pixels.
```


**Natural Language Program:**

1.  Identify all non-white pixels in the input grid and group them by color (red and yellow).
2.  Count the number of pixels for each color. Determine the color with the highest count (Majority Color - which is red in all examples) and the color with the lowest count (Minority Color - which is yellow in all examples).
3.  Find the coordinates (row, column) of all pixels belonging to the Majority Color (red).
4.  Check if all pixels of the Majority Color (red) lie in the same row *or* if they all lie in the same column.
5.  **If** the Majority Color pixels (red) are aligned (all share the same row index OR all share the same column index):
    *   Create the output grid by copying the input grid.
    *   Change all pixels of the Minority Color (yellow) to white (0). Keep the Majority Color pixels (red) as they are.
6.  **Else** (if the Majority Color pixels are *not* aligned):
    *   Create the output grid by copying the input grid.
    *   Change all pixels of the Majority Color (red) to white (0). Keep the Minority Color pixels (yellow) as they are.
7.  Output the resulting grid.
