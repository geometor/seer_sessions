*   **Perception:** The input and output grids are presented as single rows (or 1D arrays). The input grids contain only white (0) and yellow (4) pixels. The output grids contain white (0), green (3), magenta (6), and maroon (9) pixels. The transformation focuses on contiguous horizontal blocks of yellow pixels in the input. The white pixels remain unchanged. Each block of yellow pixels is replaced by a block of the same size but with a different color. The replacement color depends solely on the length (number of pixels) of the original yellow block.
    *   Yellow blocks of length 1 are replaced by maroon (9).
    *   Yellow blocks of length 2 are replaced by magenta (6).
    *   Yellow blocks of length 3 are replaced by green (3).

*   **YAML Facts:**
    
```yaml
    task_description: Replace contiguous horizontal blocks of yellow pixels with a new color based on the block's length.
    grid_dimensions:
      - input: 1xN
      - output: 1xN (same as input)
    color_palette:
      - input: [white (0), yellow (4)]
      - output: [white (0), green (3), magenta (6), maroon (9)]
    objects:
      - type: pixel
        properties:
          - color: Integer (0-9)
          - position: (row, column)
      - type: block
        description: A contiguous horizontal sequence of pixels of the same color.
        properties:
          - color: The color of the pixels in the block.
          - length: The number of pixels in the block.
          - pixels: List of pixel positions belonging to the block.
    transformations:
      - input_pixels: White (0)
        output_pixels: White (0) # No change
      - input_pixels: Yellow (4)
        condition: Part of a contiguous horizontal block of yellow pixels.
        action: Replace with a new color based on the block length.
        mapping:
          - block_length: 1
            output_color: Maroon (9)
          - block_length: 2
            output_color: Magenta (6)
          - block_length: 3
            output_color: Green (3)
        scope: All pixels within the identified block are changed to the determined output color.
    ```


*   **Natural Language Program:**
    1.  Iterate through the input grid horizontally to identify contiguous blocks of yellow (4) pixels.
    2.  For each identified yellow block, determine its length (number of consecutive yellow pixels).
    3.  Create the output grid, initially identical to the input grid.
    4.  For each identified yellow block in the input:
        *   If the block length is 1, change the corresponding pixel(s) in the output grid to maroon (9).
        *   If the block length is 2, change the corresponding pixel(s) in the output grid to magenta (6).
        *   If the block length is 3, change the corresponding pixel(s) in the output grid to green (3).
    5.  Leave all white (0) pixels unchanged in the output grid.
    6.  Return the modified output grid.