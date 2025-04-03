
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 2 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 7 7 0 0 0
```

## Perception

1.  **Grid Structure:** All examples involve 1xN grids (single rows). The specific size seen is 1x14.
2.  **Pixel Colors:** The grids contain white (0) pixels as background and blocks of a single non-white color (red=2, orange=7).
3.  **Objects:** Each input grid features exactly one contiguous horizontal block (object) of a single non-white color.
4.  **Transformation:** The core transformation observed is the horizontal translation (shift) of the non-white object.
5.  **Shift Direction & Magnitude:** In all examples, the non-white object shifts exactly one position to the right.
6.  **Background Handling:** The background color (white) fills the position vacated by the object on its left and remains in all other positions not occupied by the shifted object.
7.  **Object Integrity:** The color, shape (length), and internal arrangement of the non-white object remain unchanged during the shift.

## Facts


```yaml
task_type: grid_transformation
dimensionality: 1D (represented as 1xN 2D grid)
grid_properties:
  size: fixed (1x14 in examples)
  background_color: white (0)
objects:
  - type: contiguous_block
    count: 1 per grid
    color: single non-white color (e.g., red, orange)
    shape: horizontal segment
    properties:
      - length: variable
      - color: variable (non-white)
actions:
  - name: identify_object
    target: the single non-white contiguous block
  - name: translate_object
    target: the identified block
    direction: right
    magnitude: 1 position
    constraints: preserves object color and length
output_generation:
  - create_new_grid:
      size: same as input
      initial_fill: background_color (white)
  - place_object:
      object: the translated block
      position: original_start_index + 1
```


## Natural Language Program

1.  Identify the single contiguous block of non-white pixels within the input row. Note its color and length.
2.  Determine the starting column index of this block.
3.  Create a new output row of the same length as the input row, initially filled entirely with white (0) pixels.
4.  Copy the identified non-white block into the new output row, starting at the original starting column index plus one.
