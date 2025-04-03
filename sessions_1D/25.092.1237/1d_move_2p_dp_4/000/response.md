**Perception:**

The input and output are both 1D arrays (or grids of height 1) of the same length.
The arrays contain pixels of different colors: white (0), green (3), gray (5), blue (1), and azure (8).
In each example, the input contains a single contiguous block of a non-white, non-azure color and a single azure (8) pixel. The rest of the pixels are white (0).
The output shows that the contiguous block of color has shifted its position horizontally to the right.
The azure (8) pixel does not change its position.
The block of color moves rightwards until its rightmost pixel is immediately adjacent (to the left) of the azure (8) pixel.
The pixels originally occupied by the left part of the block before the shift become white (0) in the output. The relative positions of other white pixels and the azure pixel remain unchanged, except for those replaced by the shifted block or those filling the vacated space.

**Facts:**


```yaml
task_type: array_manipulation_1d
components:
  - type: background
    color: white (0)
  - type: object
    identifier: colored_block
    description: A contiguous horizontal block of a single color, excluding white (0) and azure (8).
    properties:
      - color: variable (green, gray, blue in examples)
      - contiguous: true
      - count: 1 per input array
  - type: marker
    identifier: anchor_pixel
    description: A single pixel used as a reference point.
    properties:
      - color: azure (8)
      - count: 1 per input array
      - static_position: true
actions:
  - name: identify_components
    inputs: [input_array]
    outputs: [colored_block, anchor_pixel]
    steps:
      - Scan the array to find the start and end indices of the contiguous block of non-white, non-azure color.
      - Scan the array to find the index of the azure (8) pixel.
  - name: calculate_shift
    inputs: [colored_block_end_index, anchor_pixel_index]
    outputs: [shift_amount]
    description: Determine how many positions the block needs to move right.
    calculation: target_end_index = anchor_pixel_index - 1; shift_amount = target_end_index - colored_block_end_index
  - name: apply_shift
    inputs: [input_array, colored_block_start_index, colored_block_end_index, shift_amount]
    outputs: [output_array]
    steps:
      - Create a copy of the input array, initialized with white (0) pixels.
      - Copy the non-block pixels (excluding the block area in the input) to the output array, maintaining their original positions relative to the array boundaries or the anchor pixel, except for the area that will be occupied by the shifted block. Specifically, copy the anchor pixel and any pixels to its right. Copy pixels to the left of the original block position.
      - Calculate the new start and end indices for the block: new_start = colored_block_start_index + shift_amount, new_end = colored_block_end_index + shift_amount.
      - Copy the pixels of the colored_block from the input array to the output array at the new indices [new_start, new_end].
      - Ensure the space originally occupied by the block (from colored_block_start_index up to new_start - 1) is filled with white (0) in the output array.
relationships:
  - type: spatial_adjacency
    between: [colored_block, anchor_pixel]
    state: target
    details: In the output, the rightmost pixel of the colored_block must be immediately to the left of the anchor_pixel.
```


**Natural Language Program:**

1.  Initialize the output array as a copy of the input array.
2.  Identify the contiguous horizontal block of pixels that are not white (0) and not azure (8). Record its color, start index, and end index.
3.  Identify the location (index) of the single azure (8) pixel.
4.  Calculate the target end index for the colored block, which is the index immediately to the left of the azure (8) pixel (azure index - 1).
5.  Calculate the necessary shift distance for the block: `shift = target_end_index - current_block_end_index`.
6.  If the shift distance is greater than 0:
    a.  Determine the new start index (`current_block_start_index + shift`) and new end index (`current_block_end_index + shift`) for the block.
    b.  Fill the original positions of the block in the output array (from `current_block_start_index` to `current_block_end_index`) with white (0) pixels.
    c.  Place the pixels of the colored block into the output array at the new positions (from `new_start_index` to `new_end_index`).
7.  Return the modified output array.