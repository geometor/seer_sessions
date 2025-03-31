*   **Perception:** The input grids contain a uniform background color and several objects composed of other distinct colors. These objects appear as hollow rectangular frames. The transformation involves filling the interior (the hollow part) of each rectangular frame with the color of the frame itself. The background color and the frame pixels remain unchanged.

*   **YAML Facts:**
    
```yaml
    background_color:
      description: The single color that occupies the majority of the grid cells in the input.
      value: Varies per example (green, red, yellow).
      unchanged: Yes
    objects:
      description: Contiguous groups of pixels with the same color, distinct from the background color.
      properties:
        - color: A single color per object (azure, yellow, red, blue, green).
        - shape: Hollow rectangles (frames).
    transformation:
      action: Fill interior
      target: Hollow rectangular objects
      details: The pixels inside the rectangular frame, which initially match the background color, are changed to the color of the frame.
      condition: The filling only occurs if a pixel is surrounded (directly or indirectly along cardinal axes) by pixels of the *same* non-background color on all four sides (top, bottom, left, right).
    ```


*   **Natural Language Program:**
    1.  Identify the background color, which is the most frequent color in the input grid.
    2.  Create a copy of the input grid to serve as the output grid.
    3.  Iterate through each pixel of the input grid that has the background color.
    4.  For each background pixel, check if it is enclosed within a hollow rectangular frame of a single non-background color. This check can be performed by verifying if there exists a path consisting solely of pixels of a single non-background color 'C' from the current background pixel position outwards in the up, down, left, and right directions, eventually reaching pixels of color 'C' in all four directions.
    5.  If a background pixel is found to be enclosed by a frame of color 'C' according to the check in step 4, change the color of the corresponding pixel in the output grid to color 'C'.
    6.  Pixels that are not part of the background or are background pixels not enclosed by a frame retain their original color in the output grid.
    7.  Return the modified output grid.