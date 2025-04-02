*   **Perception:** The task operates on single-row grids (1xN). Each example uses white (0) as a background color and one other color (yellow, blue, or azure). The transformation involves modifying sequences of the non-white color. Specifically, isolated non-white pixels (pixels surrounded by white pixels on both sides) are expanded horizontally into a sequence of three identical pixels, overwriting the adjacent white pixels. Existing sequences of three or more non-white pixels remain unchanged.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D # All examples are single rows
    background_color: 0 # White
    objects:
      - type: pixel_sequence
        color: non-white # Yellow (4), Blue (1), Azure (8) in examples
        properties:
          - length: Integer (number of contiguous pixels)
          - position: Start and end indices
          - context: Neighboring pixels (especially if they are white)
    transformation:
      action: conditional_expansion
      target: isolated_pixels # Non-white pixels with white neighbors on both sides
      condition: pixel is non-white AND left_neighbor is white AND right_neighbor is white
      effect: replace the sequence [white, pixel, white] with [pixel, pixel, pixel]
      preservation: non-white pixel sequences of length >= 3 are unchanged
    output_grid: Same dimensions as input, modified according to the transformation rule.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel of the input grid from the second pixel (index 1) up to the second-to-last pixel (index width-2).
    3.  For the current pixel at index `i`:
        a.  Check if the pixel is non-white (value > 0).
        b.  Check if the pixel to its left (index `i-1`) is white (value 0).
        c.  Check if the pixel to its right (index `i+1`) is white (value 0).
    4.  If all three conditions (non-white current pixel, white left neighbor, white right neighbor) are true:
        a.  Get the color of the current pixel.
        b.  Set the pixel at index `i-1` in the output grid to this color.
        c.  Set the pixel at index `i` in the output grid to this color.
        d.  Set the pixel at index `i+1` in the output grid to this color.
    5.  Return the modified output grid.