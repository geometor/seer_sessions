*   **Perception**:
    *   The input and output data are presented as 1D arrays (or flattened 2D grids) of integers representing colors.
    *   Each input array contains a single contiguous block of non-white (non-zero) pixels, surrounded by white (zero) pixels.
    *   The non-white block consists of pixels of the same color (e.g., all red, all blue, all gray).
    *   In the output, this block of non-white pixels appears shifted one position to the right compared to its position in the input.
    *   The leftmost pixel of the original block becomes white (0).
    *   The white (0) pixel immediately to the right of the original block takes on the color of the block.

*   **Facts**:
    
```yaml
    task_type: array_manipulation
    data_representation: 1D_array_of_colors
    background_color: 0 # white
    objects:
      - type: contiguous_block
        color: non-white (variable, e.g., 2, 1, 5)
        properties:
          - single_color_within_block
          - surrounded_by_background_color (at least on the right)
    actions:
      - identify_object: locate the start and end indices of the non-white block
      - shift_object: move the block one position to the right
      - update_pixels:
          - change the leftmost pixel of the original block position to the background color (0)
          - change the pixel immediately to the right of the original block position to the block's color
    relationships:
      - spatial: the block is shifted relative to its original position
      - adjacency: the pixel immediately to the right of the block is involved in the transformation
    constraints:
      - only one non-white block exists
      - the block has space to shift right (i.e., there's a white pixel to its right)
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous sequence (block) of non-white pixels in the input array. Note the color of this block and its start and end indices.
    2.  Create a copy of the input array to serve as the output array.
    3.  Change the pixel at the start index of the identified block in the output array to white (0).
    4.  Change the pixel at the index immediately following the end index of the block in the output array to the color noted in step 1.
    5.  Return the modified output array.