
## train_1

**input:**
```
0 0 7 7 7 0 0 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 0 0 7 7 7 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 3 3 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 0 0 0 3 3 3 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 0 0 5 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 5 5 5 0 0 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**: The task operates on single-row grids. The input grids contain a white background (color 0) and one or more contiguous blocks of a single non-white color. Some blocks consist of a single colored pixel, while others consist of multiple adjacent colored pixels. The transformation rule depends on the size of these colored blocks. Single colored pixels in the input are expanded into a block of three pixels of the same color in the output, centered at the original pixel's position. Blocks containing more than one colored pixel are copied directly to the output without modification. The background remains white except where replaced by the expansion of single colored pixels.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively 1D arrays
    objects:
      - type: background
        color: white (0)
        role: canvas
      - type: block
        properties:
          color: non-white (varies per example: orange, green, gray)
          contiguity: horizontal
          size: number of pixels in the block (e.g., 1, 3)
          position: starting index and ending index
    actions:
      - identify_blocks: Find contiguous segments of non-white pixels in the input row.
      - check_block_size: Determine the number of pixels in each identified block.
      - expand_block: If a block size is 1, replace it and its immediate neighbors (if they exist within bounds) with the block's color.
      - copy_block: If a block size is greater than 1, copy the block to the output at the same position.
    relationships:
      - input_output_mapping: The output grid is derived from the input grid based on block size rules.
      - size_dependent_transformation: The action performed (expand or copy) depends on the size of the input block.
    state_changes:
      - Single-pixel blocks (size 1) are transformed into three-pixel blocks.
      - Multi-pixel blocks (size > 1) remain unchanged.
      - Some white pixels adjacent to single-pixel blocks may change color in the output.
    ```


*   **Natural Language Program**:
    1.  Create an output grid of the same dimensions as the input grid, initialized with the background color (white, 0).
    2.  Iterate through the input grid to identify contiguous blocks of non-white pixels. Record the color, starting position, and size (number of pixels) of each block.
    3.  For each identified block:
        a.  If the block size is exactly 1:
            i.  Let the color be `C` and the position (index) be `i`.
            ii. Write the color `C` to the output grid at index `i`.
            iii. If index `i-1` is within the grid bounds, write color `C` to the output grid at index `i-1`.
            iv. If index `i+1` is within the grid bounds, write color `C` to the output grid at index `i+1`.
        b.  If the block size is greater than 1:
            i.  Copy the pixels of this block from the input grid directly to the corresponding positions in the output grid.
    4.  Return the final output grid.
