
## train_1

**input:**
```
0 0 0 0 6 7 7 7 7 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 7 6 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 2 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 5 1 1 1 1 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 1 1 1 1 1 5 0
```

**Perception of the Elements:**

The task operates on 1x16 grids. Each input grid contains a background of white pixels (0) and a single contiguous block (object) of non-white pixels. The transformation involves modifying only this non-white block, leaving the white background pixels unchanged. Specifically, the first pixel of the non-white block is moved to the end position of that block, effectively shifting all other pixels within the block one position to the left. The overall grid dimensions remain the same.

**Facts:**


```yaml
task_type: object_transformation
grid_properties:
  - dimension: 1x16 (single row)
  - background_color: white (0)
objects:
  - type: contiguous_block
    pixels: non-white
    count: 1 per grid
transformation:
  - type: modification
    target: non-white_block
    action: cyclic_shift_left
    details: The first pixel of the block is moved to the last position of the block. All other pixels in the block shift one position to the left.
relationships:
  - The position and extent of the white background pixels remain unchanged relative to the grid boundaries.
  - The length of the non-white block remains unchanged.
  - The set of colors within the non-white block remains the same, only their order changes.
```


**Natural Language Program:**

1.  Identify the contiguous block of non-white pixels within the input grid row.
2.  Determine the starting and ending indices of this non-white block.
3.  Isolate the sequence of pixels forming this block.
4.  Perform a left cyclic shift on this sequence: move the first pixel of the sequence to the end of the sequence.
5.  Construct the output grid by replacing the original non-white block segment in the input grid with the shifted sequence, keeping all white pixels in their original positions.
