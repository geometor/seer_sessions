*   **Perception:** The task operates on 1D arrays or single rows/columns of a 2D grid. It identifies specific patterns of non-white pixels (colors) and modifies them based on their context. White pixels (0) seem to act as background or empty space. The core transformation involves expanding isolated, single, non-white pixels into horizontal blocks of three identical pixels, centered on the original position. Existing horizontal blocks of three identical non-white pixels remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: pattern_modification
    dimensionality: 1D (or applies row-wise independently)
    objects:
      - type: pixel
        properties:
          color: integer (0-9)
          is_background: true (if color is 0)
          is_foreground: true (if color is not 0)
      - type: horizontal_sequence
        properties:
          pixels: list of adjacent pixels in a row
          length: integer
          color: integer (if all pixels have the same non-white color)
    actions:
      - name: identify_single_foreground_pixel
        description: Find a non-white pixel whose immediate left and right neighbors are white (or grid boundaries).
      - name: expand_pixel_horizontally
        input: position (r, c), color (C)
        output_effect: Modifies the output grid at (r, c-1), (r, c), (r, c+1) to color C, respecting boundaries.
        trigger: identify_single_foreground_pixel
      - name: identify_three_block
        description: Find three adjacent pixels in a row with the same non-white color.
      - name: preserve_block
        description: Ensure an identified block (like a 1x3 block) remains unchanged in the output.
        trigger: identify_three_block (implicitly handled by default copy and selective expansion)
    relationships:
      - type: adjacency
        direction: horizontal (left, right)
        relevance: Determines if a pixel is 'single' or part of a larger block.
    ```


*   **Natural Language Program:**
    1.  Create an output grid initialized as a copy of the input grid.
    2.  Iterate through each row `r` and column `c` of the input grid.
    3.  Let `C` be the color of the pixel at `input[r][c]`.
    4.  If `C` is not white (i.e., `C > 0`):
        a.  Check if the pixel to the left (`input[r][c-1]`) is white or if `c` is the first column (index 0).
        b.  Check if the pixel to the right (`input[r][c+1]`) is white or if `c` is the last column.
        c.  If both conditions (a and b) are true (meaning the pixel `C` is horizontally isolated):
            i.  Set the color of the pixel at `output[r][c]` to `C`.
            ii. If `c` is not the first column, set the color of the pixel at `output[r][c-1]` to `C`.
            iii.If `c` is not the last column, set the color of the pixel at `output[r][c+1]` to `C`.
    5.  Return the final output grid.