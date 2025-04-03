
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 0 0 6 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 6 0
```


## train_2

**input:**
```
0 0 0 0 0 0 1 1 1 1 1 0 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 1 1 1 6 0
```


## train_3

**input:**
```
0 5 5 5 5 5 5 5 5 5 0 0 6 0 0
```


**output:**
```
0 0 0 5 5 5 5 5 5 5 5 5 6 0 0
```

*   **Perception**: The task operates on single-row grids. The transformation rearranges pixels within the row without changing their colors or counts. The core operation involves identifying two specific adjacent blocks of pixels: the first contiguous block of non-white pixels and the immediately following contiguous block of white pixels. These two blocks swap their positions, while all other pixels retain their positions relative to this swapped pair.

*   **YAML Facts**:
    
```yaml
    task_type: pixel_rearrangement
    grid_dimensionality: 1D # single row
    transformation: positional_swap
    objects:
      - type: pixel_block
        description: A contiguous sequence of pixels.
        attributes:
          - color_type: white (0) or non-white (1-9)
          - position: start and end index
          - length: number of pixels
    identified_elements:
      - element: initial_segment
        description: Optional sequence of pixels preceding the first non-white block. Can be empty.
      - element: block_A
        description: The first contiguous block of non-white pixels found when scanning from left to right.
      - element: block_B
        description: The contiguous block of white pixels immediately following block_A. Must exist for the swap to occur.
      - element: final_segment
        description: Optional sequence of pixels following block_B. Can be empty.
    action:
      - type: swap
        operands: [block_A, block_B]
        condition: Both block_A and block_B must exist and be adjacent in the input sequence `[..., block_A, block_B, ...]`.
    input_structure: '[initial_segment] [block_A] [block_B] [final_segment]'
    output_structure: '[initial_segment] [block_B] [block_A] [final_segment]'
    invariants:
      - grid_dimensions
      - pixel_colors
      - pixel_counts
    ```


*   **Natural Language Program**:
    1.  Scan the input grid (row) from left to right to identify the first contiguous block of non-white pixels (call this `block_A`). Record its start and end indices.
    2.  Check the pixels immediately following `block_A`. Identify the contiguous block of white pixels starting right after `block_A` (call this `block_B`). Record its start and end indices.
    3.  If both `block_A` and `block_B` are found and `block_B` starts immediately after `block_A` ends:
        a.  Identify the segment of the grid *before* `block_A` (call this `initial_segment`). This might be empty.
        b.  Identify the segment of the grid *after* `block_B` (call this `final_segment`). This might be empty.
        c.  Construct the output grid by concatenating the segments in the order: `initial_segment`, `block_B`, `block_A`, `final_segment`.
    4.  If `block_A` is not found, or if `block_B` is not found immediately following `block_A`, the output grid is identical to the input grid.
