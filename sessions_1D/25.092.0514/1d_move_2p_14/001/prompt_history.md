
## train_1

**input:**
```
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0
```


## train_2

**input:**
```
0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0
```

*   **Perception:** The task operates on single-row grids (1xN). Each input grid contains a single contiguous horizontal block of a non-white color, surrounded by white pixels (color 0). The output grid has the same dimensions and the same non-white block, but the block is shifted horizontally to the right by exactly 2 positions. The white pixels effectively wrap around or redistribute to maintain the grid size and accommodate the shift.

*   **YAML:**
    
```yaml
    task_description: Shift a horizontal colored block 2 positions to the right within a single-row grid.
    grid_properties:
      - dimensionality: 1D (single row)
      - size_invariance: true (output size equals input size)
    objects:
      - object_type: background
        color: white (0)
        role: Fills space not occupied by the block.
      - object_type: block
        count: 1
        description: A contiguous horizontal segment of a single non-white color.
        properties:
          - color: non-white (varies per example: 6, 3, 5)
          - shape: horizontal line segment
          - size_invariance: true (length does not change)
    actions:
      - action: horizontal_shift
        target_object: block
        direction: right
        magnitude: 2 pixels
        effect_on_background: White pixels are rearranged to fill the space vacated by the block on the left and are displaced by the block on the right. The total number of white pixels remains constant.
    relationships:
      - The block is always surrounded by white pixels in the input.
      - The block's position changes relative to the grid boundaries in the output.
    ```


*   **Natural Language Program:**
    1.  Identify the input grid, which consists of a single row.
    2.  Locate the contiguous horizontal segment (the "block") composed of non-white pixels. Note its color, starting column index, and ending column index.
    3.  Create a new output grid of the same dimensions as the input grid, initially filled entirely with white (0) pixels.
    4.  Calculate the new starting column index for the block by adding 2 to its original starting column index.
    5.  Copy the identified non-white block from the input grid into the output grid, placing it starting at the calculated new starting column index. Ensure the block retains its original color and length.
