
## train_1

**input:**
```
0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0
```


## train_3

**input:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
```

*   **Perception:** The task involves manipulating single-row grids. Each input grid contains a contiguous horizontal segment of a single non-white color, flanked by white pixels on both sides or extending to one edge. The output grid shows the same colored segment, but shifted horizontally to the right by a fixed amount. The background color is consistently white (0). The size and color of the segment remain unchanged. The overall dimensions of the grid also remain unchanged. The shift appears consistent across all examples.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (represented as 1xN 2D array)
    grid_size_relation: output grid has the same dimensions as the input grid
    background_color: white (0)
    objects:
      - type: contiguous_horizontal_segment
        properties:
          - color: non-white (magenta, azure, red in examples)
          - size: variable length
          - count: exactly one per grid
    actions:
      - type: horizontal_shift
        parameters:
          - object: the non-white segment and surrounding white pixels
          - direction: right
          - amount: 3 pixels
        details: The entire content of the input row is shifted right by 3 positions. Pixels shifted beyond the right boundary are discarded. The leftmost 3 positions are filled with the background color (white).
    relationships:
      - The color and length of the non-white segment are preserved between input and output.
      - The position of the segment changes consistently.
    inferred_rule: Shift the entire input grid content 3 positions to the right, filling the newly vacated leftmost positions with white pixels.
    ```


*   **Natural Language Program:**
    1.  Receive the input grid (a single row).
    2.  Create a new output grid with the same dimensions as the input grid, initially filled with the background color white (0).
    3.  Iterate through the columns of the input grid from the first column up to the column at index `width - 1 - 3`.
    4.  For each column index `c` in this range, copy the pixel value from the input grid at `(0, c)` to the output grid at position `(0, c + 3)`.
    5.  The first 3 columns (indices 0, 1, 2) of the output grid remain white (0), as initialized.
