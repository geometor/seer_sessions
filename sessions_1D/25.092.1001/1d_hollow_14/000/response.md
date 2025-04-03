*   **Perception:**
    *   The input and output grids are single rows (1D arrays).
    *   Each input grid contains exactly one contiguous horizontal segment of a non-white color. The rest of the grid is white (0).
    *   The non-white color differs across examples (magenta, green, yellow).
    *   The transformation modifies the colored segment.
    *   In the output grid, only the first and last pixels of the original colored segment retain their color.
    *   All the pixels *between* the first and last pixels of the original segment are changed to white (0).
    *   Pixels outside the original segment remain white (0).
    *   The dimensions of the grid remain unchanged.

*   **Facts:**
    
```yaml
    objects:
      - id: input_grid
        description: A 1xN grid.
      - id: output_grid
        description: A 1xN grid, derived from the input grid.
      - id: colored_segment
        description: A contiguous horizontal sequence of identical non-white pixels within the input grid.
        properties:
          - color: The non-white color of the pixels in the segment (e.g., magenta, green, yellow).
          - start_index: The column index of the first pixel in the segment.
          - end_index: The column index of the last pixel in the segment.
          - length: The number of pixels in the segment (end_index - start_index + 1).
      - id: background_pixels
        description: Pixels with the color white (0).
    relationships:
      - type: containment
        subject: colored_segment
        object: input_grid
      - type: spatial
        description: The colored_segment is surrounded by background_pixels in the input grid.
      - type: transformation
        subject: input_grid
        object: output_grid
        action: endpoints_preservation
    actions:
      - id: identify_segment
        description: Locate the start and end indices and the color of the colored_segment in the input grid.
      - id: endpoints_preservation
        description: Create the output grid by preserving only the first and last pixels of the input's colored_segment and setting all other pixels (including those originally inside the segment) to white (0).
        inputs:
          - input_grid
          - colored_segment properties (start_index, end_index, color)
        outputs:
          - output_grid
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
    2.  Identify the contiguous horizontal segment of non-white pixels in the input grid. Note its color, its starting column index, and its ending column index.
    3.  In the output grid, set the pixel at the identified starting column index to the color of the segment.
    4.  In the output grid, set the pixel at the identified ending column index to the color of the segment.