
## train_1

**input:**
```
0 0 0 0 0 0 0 8 2 2 2 2 2 2 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 2 2 2 2 2 8 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 2 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 6 6 6 6 6 2 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 4 5 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 4 0 0 0 0 0
```

*   **Perception**:
    *   The input and output are single rows (1D grids) of pixels.
    *   Each row consists primarily of a background color (white, 0).
    *   Within the background, there is a distinct pattern: a single pixel of one color ('mover') immediately followed by a contiguous block of pixels of another color ('block').
    *   Example 1: Azure (8) mover, Red (2) block.
    *   Example 2: Red (2) mover, Magenta (6) block.
    *   Example 3: Yellow (4) mover, Gray (5) block.
    *   The transformation involves swapping the position of the single 'mover' pixel with the adjacent 'block' of pixels. The mover pixel moves to the right end of the combined mover+block sequence, and the block shifts left to occupy the original mover position and the initial part of the block's original position.
    *   The colors and the length of the block remain unchanged. The background pixels also remain unchanged.

*   **YAML Facts**:
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D (row)
    background_color: white (0)
    objects_present:
      - type: mover_pixel
        description: A single pixel of a unique color within the non-background segment. Always appears first in the sequence.
        colors_observed: [azure (8), red (2), yellow (4)]
      - type: color_block
        description: A contiguous sequence of pixels of a single color, immediately following the mover_pixel.
        properties:
          - contiguity: yes
          - variable_length: yes
        colors_observed: [red (2), magenta (6), gray (5)]
    initial_state: The mover_pixel is immediately adjacent to the left of the color_block.
    transformation_rule:
      action: swap_elements
      elements_involved: [mover_pixel, color_block]
      description: The positions of the mover_pixel and the entire color_block are swapped relative to each other. The mover_pixel now appears immediately to the right of the color_block.
      invariants:
        - background pixel positions
        - mover_pixel color
        - color_block color
        - color_block length
        - relative order of pixels within the color_block
    ```


*   **Natural Language Program**:
    1.  Identify the sequence of non-background pixels in the input row.
    2.  The first pixel in this sequence is the 'mover' pixel. Record its color and original position.
    3.  The subsequent contiguous pixels of the same color form the 'color block'. Record its color, length, and the pixels themselves.
    4.  Construct the output row by replacing the original sequence (mover + block) with the new sequence (block + mover).
    5.  Place the recorded 'color block' pixels starting at the original position of the 'mover' pixel.
    6.  Place the recorded 'mover' pixel immediately after the end of the 'color block'.
    7.  Keep all background (white, 0) pixels in their original positions.
