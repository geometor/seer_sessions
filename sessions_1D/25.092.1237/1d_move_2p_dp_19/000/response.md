*   **Perception:**
    *   The input and output are single-row grids (1D arrays).
    *   Each input grid contains a contiguous block of pixels of a single color (e.g., blue, gray, yellow), distinct from white (0) and maroon (9).
    *   Each input grid also contains exactly one maroon (9) pixel.
    *   The remaining pixels are white (0).
    *   In the output grid, the contiguous block of colored pixels has shifted horizontally to the right.
    *   The final position of the block is such that its rightmost pixel is immediately adjacent to the left of the maroon (9) pixel.
    *   The original positions occupied by the colored block before the shift are replaced with white (0) pixels.
    *   The maroon pixel and all other white pixels remain in their original positions.

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D
    objects:
      - type: block
        description: A contiguous sequence of pixels of the same color, not white (0) or maroon (9).
        properties:
          - color: Varies (blue, gray, yellow in examples)
          - length: Varies (3, 7, 7 in examples)
          - start_index: The index of the leftmost pixel of the block.
          - end_index: The index of the rightmost pixel of the block.
        count: 1 per grid
      - type: target_pixel
        description: A single pixel with the color maroon (9).
        properties:
          - color: maroon (9)
          - index: The position of the maroon pixel.
        count: 1 per grid
      - type: background
        description: Pixels with the color white (0).
    actions:
      - name: identify_block
        description: Locate the start index, end index, and color of the non-white, non-maroon contiguous block.
      - name: identify_target
        description: Locate the index of the maroon (9) pixel.
      - name: calculate_shift
        description: Determine the destination start index for the block so its end index is `target_index - 1`. The new start index is `target_index - block_length`.
      - name: move_block
        description: Create a new grid, initially filled with white (0). Copy the block pixels to their new positions based on the calculated shift.
      - name: preserve_target
        description: Copy the maroon (9) target pixel to its original position in the new grid.
      - name: preserve_background
        description: Ensure all other pixels in the new grid remain white (0), effectively replacing the original block position with white.
    relationships:
      - type: adjacency
        description: In the output, the rightmost pixel of the moved block is immediately to the left of the target pixel (index `target_index - 1`).
    state_changes:
      - The identified block changes its position (start and end indices).
      - The grid cells originally occupied by the block become white (0).
    constraints:
      - There is exactly one movable block.
      - There is exactly one target (maroon) pixel.
      - The block always moves rightwards.
      - The grid dimensions remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, but fill it entirely with white (0) pixels.
    2.  Scan the input grid to identify the contiguous block of non-white (0) and non-maroon (9) pixels. Record its color, length, and start index.
    3.  Scan the input grid to find the index of the single maroon (9) pixel (the target index).
    4.  Calculate the new start index for the block in the output grid. This index is `target_index - block_length`.
    5.  Copy the pixels of the identified block (using its recorded color) into the output grid, starting at the calculated new start index and extending for the block's length.
    6.  Copy the maroon (9) pixel into the output grid at its original target index.
    7.  Return the modified output grid.