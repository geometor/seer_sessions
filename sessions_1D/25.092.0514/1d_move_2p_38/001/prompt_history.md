
## train_1

**input:**
```
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
```


## train_2

**input:**
```
0 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 4 4 4 4 0 0
```


## train_3

**input:**
```
3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   All examples operate on 1x16 grids (single rows).
    *   Each input grid contains a single contiguous block of a non-white color (yellow in examples 1 and 2, green in example 3) surrounded by white (0) pixels.
    *   The output grid is identical in size to the input grid.
    *   The transformation involves shifting the non-white block horizontally to the right.
    *   The color, shape, and size of the block remain unchanged.
    *   The amount of the shift appears constant across examples. In example 1, the block `4 4 4` moves from index 5 to index 7 (shift of 2). In example 2, the block `4...4` moves from index 1 to index 3 (shift of 2). In example 3, the block `3 3 3 3` moves from index 0 to index 2 (shift of 2). The shift is consistently 2 positions to the right.

*   **YAML Facts**:
    
```yaml
    task_type: object_transformation
    grid_properties:
      dimensionality: 1D # Effectively 1D as height is always 1
      height: 1
      width: 16
      background_color: 0 # white
    objects:
      - count: 1
        description: A contiguous horizontal block of a single non-white color.
        properties:
          color: variable (non-zero)
          shape: horizontal line segment
          size: variable length
          contiguity: horizontal
    actions:
      - type: translation
        object: the non-white block
        direction: horizontal (right)
        magnitude: 2 pixels
    relationships:
      - input_output: The output grid contains the same object as the input grid, but shifted horizontally.
    invariants:
      - grid dimensions
      - background color
      - object color
      - object shape
      - object size (length)
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
    2.  Identify the contiguous horizontal segment (block) of non-white pixels in the input grid. Note its color, starting column index, and length.
    3.  Calculate the new starting column index for the block by adding 2 to its original starting column index.
    4.  Place the identified block (with its original color and length) into the output grid starting at the calculated new column index.
