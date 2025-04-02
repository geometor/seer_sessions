*   **Perception**: The task involves filtering the input grid based on pixel color. Each input grid contains various colored pixels, including a significant number of azure (8) pixels, often interspersed within or forming patterns across other colored regions. The corresponding output grid retains only the azure (8) pixels in their original positions, while all other pixels are replaced with the background color, white (0). The dimensions of the grid remain unchanged. The transformation acts as a selective filter, isolating the azure pixels against a uniform white background.

*   **YAML Facts**:
    
```yaml
    task_context:
      grid_dimensions: Consistent between input and output.
      background_color_input: Variable (white (0) in examples 1 and 3, none explicit in example 2).
      background_color_output: Consistently white (0).
    objects:
      - type: pixel_groups
        properties:
          - color: Various colors present in input (e.g., green-3, magenta-6, orange-7, yellow-4, red-2, maroon-9, blue-1, azure-8, white-0).
          - special_color: Azure (8) is the key color.
    relationships:
      - type: positional_invariance
        description: The azure (8) pixels maintain their exact (row, column) coordinates from the input to the output grid.
    actions:
      - type: filter
        input: Input grid
        output: Output grid
        rule: Keep only pixels with azure (8) color.
      - type: replace
        target_pixels: All pixels that are NOT azure (8).
        replacement_color: White (0).
        condition: Apply to all non-azure pixels in the input grid to produce the output grid.

    ```


*   **Natural Language Program**:
    1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the white (0) color.
    2.  Iterate through each pixel of the input grid at every row and column position.
    3.  Check the color of the current pixel in the input grid.
    4.  If the color of the input pixel is azure (8), set the color of the pixel at the corresponding position in the output grid to azure (8).
    5.  If the color of the input pixel is any color other than azure (8), leave the corresponding pixel in the output grid as white (0).
    6.  Return the completed output grid.