
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```


## train_3

**input:**
```
0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**: The task operates on single-row grids. Each input grid contains a contiguous block of a single non-white color ('yellow', 'orange', or 'gray' in the examples) surrounded by 'white' (0) background pixels. The output grid is the same size as the input grid. The transformation involves shifting the non-white block horizontally to the right by a fixed amount. The block retains its original color and length. The space vacated by the block on the left becomes 'white', and the block overwrites the 'white' pixels as it moves right.

*   **Facts**:
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (single row)
    background_color: white (0)
    objects:
      - type: contiguous_block
        properties:
          - color: non-white (varies per example: yellow(4), orange(7), gray(5))
          - shape: horizontal segment
          - length: variable
          - count: 1 per grid
    actions:
      - name: horizontal_shift
        target: contiguous_block
        properties:
          - direction: right
          - distance: 2 pixels
        effects:
          - block moves 2 positions to the right
          - block maintains color and length
          - vacated positions become background_color
          - grid dimensions remain constant
    ```


*   **Natural Language Program**:
    1.  Identify the input grid (a single row of pixels).
    2.  Locate the contiguous sequence (block) of non-white pixels. Record its color, starting index, and length.
    3.  Create a new output grid of the same length as the input grid, filled entirely with the background color ('white' - 0).
    4.  Calculate the new starting index for the block by adding 2 to its original starting index.
    5.  Copy the identified block (with its original color and length) into the output grid, starting at the calculated new index. Ensure the block does not extend beyond the grid boundaries (though in these examples, it doesn't appear to).
