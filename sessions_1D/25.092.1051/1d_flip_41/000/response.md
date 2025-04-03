Okay, analyzing the provided examples.

**Perception of Task Elements:**

1.  **Grid Structure:** The inputs and outputs appear to be single rows (1D grids).
2.  **Objects:** The primary objects are contiguous blocks of non-white pixels. In each example, there are two such objects immediately adjacent to each other:
    *   A block consisting of a single pixel (blue `1`, blue `1`, azure `8` in the examples).
    *   A block consisting of multiple pixels of the same color (green `3`, gray `5`, red `2` in the examples).
3.  **Background:** The rest of the grid is filled with white (`0`) pixels, acting as background.
4.  **Transformation:** The core transformation is a swap of position between the single-pixel object and the multi-pixel block object it is adjacent to. The single pixel effectively moves to the other end of the block, and the block shifts to occupy the original position of the single pixel.

**YAML Facts:**


```yaml
task_type: object_manipulation
grid_dimensionality: 1D # Effectively single rows
objects:
  - type: block
    count: 2 per example (excluding background)
    properties:
      - contiguity: yes
      - color: non-white (0)
      - size:
          - one block is always size 1
          - the other block is size > 1
relationships:
  - type: adjacency
    between: the single-pixel block and the multi-pixel block
    direction: side-by-side (horizontal)
actions:
  - name: swap_position
    target: the adjacent single-pixel block and multi-pixel block
    effect: The single pixel moves to the opposite end of the multi-pixel block's original span, and the multi-pixel block shifts into the single pixel's original position.
background:
  color: white (0)
  role: static, defines boundaries
invariance:
  - Background pixels remain unchanged.
  - The colors and total counts of non-white pixels remain unchanged.
  - The relative order of pixels *within* the multi-pixel block remains unchanged.
```


**Natural Language Program:**

1.  Identify all contiguous blocks of non-white pixels in the input row.
2.  Find two blocks that are directly adjacent to each other. One of these blocks will consist of a single pixel, and the other will consist of multiple pixels of the same color.
3.  Determine the positions (indices) occupied by the single pixel and the multi-pixel block.
4.  Create the output row by copying the input row.
5.  Place the single pixel at the index corresponding to the *opposite* end of the multi-pixel block's original position (if the single pixel was originally left, place it at the rightmost index of the block's span; if it was right, place it at the leftmost index).
6.  Shift the pixels of the multi-pixel block to occupy the remaining positions originally held by both blocks, including the original position of the single pixel. Ensure the internal order of the multi-pixel block is preserved.
7.  Leave all other pixels (background white pixels) unchanged.