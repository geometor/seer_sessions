*   **Perception:** The input grids are one-dimensional arrays (or 1xN grids) containing mostly white pixels (0) and one other color (red, yellow, or blue in the examples). Each input grid features one large contiguous block of the non-white color and several isolated single pixels of the same color. The output grid retains only the largest contiguous block of the non-white color, positioned exactly as it was in the input. All other pixels, including the previously isolated non-white pixels and all original white pixels, become white in the output. The transformation identifies and isolates the single largest contiguous segment of non-background color, discarding all smaller segments and isolated pixels of that color.

*   **Facts:**
    
```yaml
    task_type: filtering
    grid_dimensionality: 1D # presented as 1xN
    background_color: white (0)
    objects:
      - type: contiguous_block
        color: non-white (variable: red, yellow, blue in examples)
        properties:
          - size: count of pixels in the block
          - location: start and end indices
    relationships:
      - multiple blocks of the same non-white color can exist within one input grid.
      - blocks vary in size (some are size 1, others are larger).
    actions:
      - identify_all_contiguous_blocks: find all groups of adjacent non-white pixels.
      - calculate_block_size: determine the number of pixels in each block.
      - find_largest_block: identify the block with the maximum size. If there's a tie for largest, the examples don't cover this, but assume one is chosen (e.g., the first one encountered).
      - filter_blocks: keep only the largest block.
      - generate_output: create a new grid of the same dimensions as the input, initially filled with the background color (white).
      - place_largest_block: copy the pixels corresponding to the largest block from the input to their original positions in the new output grid.
    result: The output grid contains only the largest contiguous block of non-white color from the input, with all other positions set to white.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Identify all contiguous blocks of non-white pixels in the input grid. For each block, record its color, starting position, ending position, and size (number of pixels).
    3.  If no non-white blocks are found, return the initialized white output grid.
    4.  Determine the maximum size among all identified blocks.
    5.  Select the block(s) that have this maximum size. (Based on the examples, there appears to be only one unique largest block per input).
    6.  For the selected largest block, copy its pixels (color and position) from the input grid to the corresponding positions in the output grid.
    7.  Return the final output grid.