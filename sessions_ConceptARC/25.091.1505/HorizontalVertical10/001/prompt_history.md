
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 4 4 4 0 0 0 8
0 0 0 2 2 2 0 0 0 8
0 0 0 3 3 3 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

## Perception

1.  **Input/Output Structure**: Both examples show a 10x10 grid as input and a 10x10 grid as output. The background is white (0).
2.  **Core Content Preservation**: In both examples, the central colored shapes present in the input grid are exactly preserved in their original positions and colors in the output grid.
3.  **Modification**: The key difference between input and output is the addition of a single line (either a full row or a full column) filled with the color azure (8).
4.  **Conditional Modification Location**:
    *   In `train_1`, the color azure (8) is *not* present in the input grid. The modification is the addition of an azure (8) line in the *rightmost column*.
    *   In `train_2`, the color azure (8) *is* present in the input grid (as part of the central shape). The modification is the addition of an azure (8) line in the *topmost row*.
5.  **Hypothesis**: The transformation rule appears to depend on the presence or absence of the color azure (8) within the input grid. If azure (8) is absent, the rightmost column is filled with azure (8). If azure (8) is present, the topmost row is filled with azure (8). The original content of the input grid remains otherwise unchanged.

## Facts


```yaml
task_type: conditional_modification
grid_properties:
  size: constant (10x10 in examples)
  background_color: white (0)

input_elements:
  - type: grid
  - objects:
      - type: contiguous_pixel_group
        properties:
          - color: varies (non-white)
          - shape: varies (horizontal bars, block)
          - location: varies (central area)
  - key_color: azure (8)

output_elements:
  - type: grid
  - objects:
      - type: preserved_input_objects
        description: All non-white objects from the input grid are copied to the output grid in the same location.
      - type: added_line
        properties:
          - color: azure (8)
          - orientation: depends on input condition (row or column)
          - location: depends on input condition (topmost row or rightmost column)
          - length: spans the full width or height of the grid

transformation_rule:
  - condition: Check if the key_color (azure, 8) exists anywhere in the input grid.
  - action_if_true:
      - Copy the input grid to the output grid.
      - Fill the topmost row (row 0) of the output grid with the key_color (azure, 8).
  - action_if_false:
      - Copy the input grid to the output grid.
      - Fill the rightmost column (last column index) of the output grid with the key_color (azure, 8).

relationships:
  - The presence or absence of azure (8) in the input grid determines the location (top row vs. right column) of the added azure (8) line in the output grid.
```


## Natural Language Program

1.  Examine the input grid to determine if any pixel has the color azure (8).
2.  Create the output grid by copying the input grid exactly.
3.  If the color azure (8) **was found** anywhere in the input grid, modify the output grid by changing all pixels in the topmost row (row 0) to azure (8).
4.  If the color azure (8) **was not found** anywhere in the input grid, modify the output grid by changing all pixels in the rightmost column to azure (8).
5.  Return the modified output grid.
