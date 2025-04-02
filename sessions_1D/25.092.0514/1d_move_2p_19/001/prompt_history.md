
## train_1

**input:**
```
0 0 0 1 1 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 0 0 0 0
```


## train_2

**input:**
```
0 5 5 5 5 5 5 5 0 0 0 0
```


**output:**
```
0 0 0 5 5 5 5 5 5 5 0 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 0 0 0
```

**Perception:**

The task operates on single-row grids. Each input grid contains a single contiguous block of non-white pixels surrounded by white (0) pixels. The output grid is the same size as the input and also contains the same non-white block, but its position is shifted. Observing the examples:

1.  **Example 1:** The block `1 1 1` (blue) starts at index 3 in the input and index 5 in the output. The shift is +2 positions.
2.  **Example 2:** The block `5 5 5 5 5 5 5` (gray) starts at index 1 in the input and index 3 in the output. The shift is +2 positions.
3.  **Example 3:** The block `4 4 4 4 4 4 4` (yellow) starts at index 0 in the input and index 2 in the output. The shift is +2 positions.

In all cases, the single contiguous block of non-white pixels is shifted exactly 2 positions to the right. The pixels originally occupied by the block become white (0) in the output, and the block overwrites the pixels at its new location.

**Facts:**

```yaml
task_type: object_manipulation
grid_dimensionality: 1D # Effectively operating on rows
input_features:
  - name: background_pixels
    value: 0
    color: white
  - name: foreground_object
    description: A single contiguous block of non-white pixels.
    properties:
      - color: Varies (blue, gray, yellow in examples)
      - length: Varies (3 or 7 in examples)
      - start_index: Varies (0, 1, 3 in examples)
output_features:
  - name: background_pixels
    value: 0
    color: white
  - name: foreground_object
    description: The same block as in the input, but shifted.
    properties:
      - color: Same as input block
      - length: Same as input block
      - start_index: Input start_index + 2
transformation:
  - action: identify_block
    target: foreground_object
    details: Find the start index, end index, and pixel values of the non-white contiguous block.
  - action: calculate_new_position
    input: block_start_index
    operation: add 2
    output: new_start_index
  - action: construct_output
    details: Create a new grid of the same size filled with white pixels, then place the identified block at the calculated new_start_index.
inferred_rule: The single contiguous block of non-white pixels is shifted 2 positions to the right.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but with all pixels set to white (0).
2.  Scan the input grid to find the first non-white pixel. This marks the start of the block. Let its index be `start_index`.
3.  Continue scanning from `start_index` to find the end of the contiguous block of non-white pixels. Let its index be `end_index`.
4.  Determine the pixel values (colors) of the block from `start_index` to `end_index` in the input grid.
5.  Calculate the new starting position for the block in the output grid: `new_start_index = start_index + 2`.
6.  Copy the sequence of pixel values identified in step 4 into the output grid, starting at `new_start_index`.
