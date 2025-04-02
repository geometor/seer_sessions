*   **Perception:**
    *   The input and output data are presented as single rows of pixels (1D grids).
    *   The background color is consistently white (0).
    *   The inputs contain non-white pixels appearing either as isolated single pixels or as horizontal lines of three identical pixels.
    *   The outputs show that some of the isolated single non-white pixels from the input have been transformed into horizontal lines of three identical pixels, using the same color as the original isolated pixel.
    *   Existing horizontal lines of three identical non-white pixels in the input remain unchanged in the output.
    *   The transformation seems localized around the isolated pixels.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively 1xN grids
    background_color: white (0)
    objects:
      - type: isolated_pixel
        definition: A single non-white pixel C at index i, where the pixel at index i-1 is white and the pixel at index i+1 is white.
        color: Any non-white color (e.g., red, azure, orange).
        properties:
          - position: index i
          - color: C
          - context: surrounded horizontally by white pixels.
      - type: horizontal_line
        definition: Three consecutive pixels of the same non-white color C at indices j, j+1, j+2.
        color: Any non-white color.
        properties:
          - length: 3
          - orientation: horizontal
    actions:
      - name: expand_pixel
        input_object: isolated_pixel (color C at index i)
        output_object: horizontal_line (color C at indices i-1, i, i+1)
        condition: The pixel must be an isolated_pixel as defined above.
        effect: Replaces the pixels at indices i-1, i, and i+1 in the output grid with the color C.
    relationships:
      - The transformation specifically targets isolated_pixel objects.
      - horizontal_line objects in the input are preserved in the output without modification.
      - The color of the isolated_pixel determines the color of the resulting horizontal_line.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel in the input grid from the second pixel (index 1) to the second-to-last pixel (index width-2).
    3.  For the current pixel at index `i` with color `C`:
        a.  Check if the color `C` is not white (0).
        b.  Check if the pixel to the left (at index `i-1`) is white (0).
        c.  Check if the pixel to the right (at index `i+1`) is white (0).
    4.  If all three conditions (3a, 3b, 3c) are true, then modify the output grid:
        a.  Set the color of the pixel at index `i-1` in the output grid to `C`.
        b.  Set the color of the pixel at index `i` in the output grid to `C`.
        c.  Set the color of the pixel at index `i+1` in the output grid to `C`.
    5.  Return the modified output grid.