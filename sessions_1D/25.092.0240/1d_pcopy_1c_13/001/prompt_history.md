
## train_1

**input:**
```
0 0 7 7 7 0 0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 0 7 7 7 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 9 9 9 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The inputs and outputs are single-row grids (1D arrays).
    *   Each input contains at least one contiguous block of identical non-white pixels and potentially some isolated single non-white pixels of the same color.
    *   The transformation identifies the first contiguous block of 2 or more identical non-white pixels. This block acts as a "pattern".
    *   Any isolated single pixel (surrounded by white pixels or grid boundaries) that has the same color as the pattern is replaced.
    *   The replacement involves inserting the identified pattern into the grid, centered around the position of the isolated pixel. Specifically, if the pattern has length L and the isolated pixel is at index `i`, the pattern replaces the grid content starting from index `i - floor(L/2)`. In the given examples where L=3, the pattern starts at `i-1`.
    *   The original pattern block remains unchanged in the output.
    *   White background pixels remain unchanged unless overwritten by the pattern replacement.

*   **Facts:**
    
```yaml
    task_type: pattern_replacement
    grid_dimensionality: 1D (single row)
    objects:
      - type: pattern_block
        description: The first contiguous sequence of 2 or more identical non-white pixels.
        properties:
          - color: The color of the pixels in the block.
          - length: The number of pixels in the block.
          - content: The sequence of pixel values.
      - type: target_pixel
        description: An isolated single non-white pixel (surrounded by white pixels or grid boundaries).
        properties:
          - color: The color of the pixel. Must match the color of the pattern_block.
          - position: The index of the pixel in the grid.
      - type: background_pixel
        description: White pixels (value 0).
    actions:
      - action: identify_pattern
        input: input_grid
        output: pattern_block (content, color, length)
      - action: identify_targets
        input: input_grid, pattern_color
        output: list of target_pixel positions
      - action: replace_targets
        input: output_grid (initially copy of input), target_positions, pattern_content
        output: modified_output_grid
        details: For each target at index `i`, replace the segment of the output grid starting at index `i - 1` with the pattern_content. The original pattern_block location remains untouched.
    relationships:
      - The color of a target_pixel must match the color of the pattern_block for replacement to occur.
      - The replacement position is relative to the target_pixel's position (starts 1 position to the left in the examples).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Scan the input grid from left to right to find the first contiguous sequence of two or more identical non-white pixels. Store this sequence as the `pattern` and note its color and length. If no such sequence exists, return the unchanged input grid.
    3.  Iterate through the input grid again, examining each pixel at index `i`.
    4.  Check if the pixel at index `i` is an "isolated target":
        *   It must not be white (color > 0).
        *   It must have the same color as the identified `pattern`.
        *   The pixel to its left (index `i-1`) must be white (0) or out of bounds.
        *   The pixel to its right (index `i+1`) must be white (0) or out of bounds.
    5.  If a pixel at index `i` is identified as an isolated target, replace the segment in the *output* grid starting at index `i-1` and extending for the length of the `pattern` with the `pattern` sequence itself. Ensure the replacement indices stay within the grid boundaries.
    6.  After checking all pixels, return the final output grid.
