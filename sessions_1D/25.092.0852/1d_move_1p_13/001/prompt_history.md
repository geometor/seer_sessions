
## train_1

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0
```

**Perception of Task Elements:**

The task operates on single-row grids (1D arrays). Each input grid consists of a sequence of pixels, primarily white (0), but containing a single contiguous horizontal block of a non-white color (e.g., orange (7) or yellow (4)). The output grid is a transformation of the input grid where the entire sequence of pixels appears to have been shifted. Observing the examples, the shift is consistently one position to the right, with the element originally at the far right wrapping around to the far left position. This is characteristic of a circular or rotational shift operation applied to the row.

**YAML Facts:**


```yaml
task_type: transformation
grid_dimensionality: 1D (single row)
input_features:
  - type: pixel_sequence
    description: A single row of pixels.
  - type: background_color
    value: white (0)
  - type: foreground_object
    description: A contiguous horizontal block of a single non-white color.
    properties:
      - color: variable (orange, yellow in examples)
      - length: variable
      - position: variable
output_features:
  - type: pixel_sequence
    description: The transformed single row of pixels.
transformation:
  - type: operation
    name: circular_shift
    direction: right
    amount: 1 position
    target: the entire input row
    details: The pixel at the last position moves to the first position, and all other pixels shift one position to the right.
```


**Natural Language Program:**

1.  Receive the input grid, which is a single row of pixels.
2.  Perform a circular shift of the entire row one position to the right.
3.  To achieve this:
    *   Take the pixel value from the rightmost position of the input row.
    *   Place this value at the leftmost position of the output row.
    *   Shift all remaining pixels from the input row (from the first position up to the second-to-last position) one position to the right to fill the rest of the output row.
4.  The resulting row is the output grid.
