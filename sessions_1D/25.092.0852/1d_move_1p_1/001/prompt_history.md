
## train_1

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on single-row grids. Each input grid contains a single contiguous block of non-white pixels surrounded by white pixels (color 0). The transformation involves shifting this non-white block exactly one position to the right. The output grid maintains the same size as the input grid. The position where the block started in the input becomes white in the output.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D # Single row
    input_features:
      - background_color: white (0)
      - objects:
          - type: contiguous_block
            color: non-white (varies: gray(5), blue(1), orange(7))
            count: 1
            properties:
              - location: defined by start and end index
              - size: variable length
    transformation:
      - type: spatial_shift
        direction: right
        distance: 1 pixel
        target: the non-white block
    output_features:
      - grid_size: same as input
      - background_color: white (0)
      - objects:
          - type: contiguous_block (same as input)
            location: original start index + 1
            size: same as input block
    relationship:
      - The non-white block in the output is identical in color and length to the block in the input.
      - The block's start position in the output is one index greater than its start position in the input.
      - The grid position corresponding to the input block's start index becomes white (0) in the output.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Scan the input grid to find the contiguous sequence (block) of non-white pixels.
    3.  Record the starting index and the pixel values of this non-white block.
    4.  Determine the starting index for the block in the output grid by adding 1 to the starting index found in the input grid.
    5.  Place the recorded sequence of non-white pixels into the output grid, beginning at the calculated new starting index.
