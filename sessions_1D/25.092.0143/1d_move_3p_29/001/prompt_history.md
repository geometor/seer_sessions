
## train_1

**input:**
```
0 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 0
```


## train_2

**input:**
```
4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 0
```


## train_3

**input:**
```
8 8 8 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 0 0 0
```

*   **Perception:**
    *   The input and output are both 1x10 grids (or single rows).
    *   Each input grid contains a single contiguous block of a non-white color (red, yellow, or azure in the examples) surrounded by white pixels (color 0).
    *   The output grid contains the same block of non-white pixels and the same number of white pixels as the input.
    *   The core transformation is the movement (translation) of the non-white block within the grid.
    *   Comparing input and output, the non-white block appears to shift exactly 3 positions to the right.
    *   The size and color of the non-white block remain unchanged.
    *   The positions previously occupied by the block become white, and the positions newly occupied by the block take on its color.

*   **Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D # Effectively 1xN grids
    grid_size: fixed (1x10)
    background_color: white (0)
    objects:
      - type: contiguous_block
        count: 1 per grid
        color: non-white (variable across examples: red, yellow, azure)
        properties:
          - length (variable)
          - start_index (variable)
          - end_index (variable)
    actions:
      - name: shift_object
        target: non-white contiguous_block
        direction: right
        distance: 3 positions
    constraints:
      - The non-white block does not wrap around the grid edges.
      - The shifted block remains within the grid boundaries.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a 1x10 grid filled entirely with the background color (white, 0).
    2.  Scan the input 1x10 grid to identify the contiguous block of non-white pixels.
    3.  Determine the color, starting index, and length of this non-white block.
    4.  Calculate the new starting index for the block in the output grid by adding 3 to the original starting index.
    5.  Place the identified non-white block (with its original color and length) into the output grid starting at the calculated new index.
