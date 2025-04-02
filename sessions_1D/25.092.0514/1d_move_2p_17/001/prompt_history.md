
## train_1

**input:**
```
0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   The inputs and outputs are single-row grids (1x16).
    *   Each input grid contains a single contiguous horizontal block of a non-white color (blue or red) surrounded by white pixels.
    *   The corresponding output grid also contains a single contiguous block of the *same* non-white color and the *same* length as the input block, surrounded by white pixels.
    *   The position of the colored block changes between the input and output. Comparing the start index of the block in the input and output, the block appears to shift horizontally to the right.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_properties:
      - shape: [1, 16] # All examples are 1x16
      - background_color: 0 # White
    objects:
      - type: contiguous_horizontal_block
        color: non_white # Color varies (1: blue, 2: red) but is preserved
        properties:
          - length # Length of the block is preserved
          - start_index # Starting column index
          - end_index # Ending column index
    actions:
      - name: horizontal_shift
        direction: right
        amount: 2 # The block shifts 2 columns to the right
        target: the non_white contiguous_horizontal_block
    relationships:
      - input_block.color == output_block.color
      - input_block.length == output_block.length
      - output_block.start_index == input_block.start_index + 2
      - output_block.end_index == input_block.end_index + 2
    state_change:
      - The area occupied by the input block becomes white in the output.
      - The area to the left of the input block remains white.
      - The area to the right of the input block remains white, except where the shifted block is placed.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid, but filled entirely with the background color (white, 0).
    2.  Identify the single contiguous horizontal block of non-white pixels in the input grid. Note its color, starting column index, and ending column index.
    3.  Calculate the new starting column index for the block by adding 2 to its original starting column index.
    4.  Calculate the new ending column index for the block by adding 2 to its original ending column index.
    5.  Fill the cells in the output grid from the new starting column index to the new ending column index (inclusive) with the original color of the block identified in step 2.
