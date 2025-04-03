
## train_1

**input:**
```
0 0 0 0 6 6 6 6 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 0 0 0 0 0 0 6 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0
```

*   **Perception**: Each task example consists of a single row of pixels. The input row contains a contiguous block of a single non-white color (magenta or green) surrounded by white pixels. The output row retains the white pixels and modifies the colored block. Specifically, only the first and last pixels of the original colored block remain in the output; all pixels between them are changed to white. The dimensions of the grid remain the same.

*   **Facts**:
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (represented as 1xN grid)
    background_color: white (0)
    objects:
      - type: contiguous_block
        color: non-white (magenta(6) or green(3) in examples)
        properties:
          - length: variable (8, 5, 10 in examples)
          - position: variable start and end indices
    transformation:
      - action: identify_block
        target: non-white contiguous block
      - action: identify_endpoints
        target: the identified block
        result: start_index, end_index
      - action: modify_block_interior
        target: pixels between start_index + 1 and end_index - 1 (inclusive)
        change: set color to background_color (white, 0)
      - action: preserve_pixels
        target: pixels at start_index and end_index
        change: none
      - action: preserve_pixels
        target: pixels outside the original block (background pixels)
        change: none
    output_characteristics:
      - maintains_dimensions: true
      - modifies_pixels: only the interior of the non-white block
      - preserves_pixels: background pixels and endpoints of the non-white block
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous block of non-white pixels in the input row. Note its color, start index, and end index.
    2.  Create an output row identical to the input row initially.
    3.  Iterate through the indices from `start_index + 1` to `end_index - 1`.
    4.  For each index in this range, change the pixel value in the output row to white (0).
    5.  Leave all other pixels (the background pixels and the pixels at the `start_index` and `end_index`) unchanged.
    6.  Return the modified row as the output.
