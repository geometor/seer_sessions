*   **Perception:** The task operates on single-row grids (1D arrays). Each input grid contains a single contiguous block of a non-white color (magenta or yellow in the examples) surrounded by white pixels (color 0). The transformation involves shifting this colored block exactly two positions to the right within the grid boundaries. The size of the grid, the color of the block, and the length of the block remain unchanged. The white pixels are rearranged to fill the space around the shifted block.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    dimensionality: 1D (single row)
    input_features:
      - type: grid
        description: A single row containing pixels.
        properties:
          size: Variable width, height is 1.
          content: Contains a single contiguous block of one non-white color surrounded by white (0) pixels.
    output_features:
      - type: grid
        description: A single row representing the transformed input.
        properties:
          size: Same width as the input grid, height is 1.
          content: Contains the same non-white colored block as the input, shifted right by 2 positions, surrounded by white pixels.
    transformation:
      - action: identify_object
        target: Contiguous block of non-white pixels.
        properties:
          color: The non-white color present.
          start_index: The starting column index of the block.
          length: The number of pixels in the block.
      - action: shift_object
        target: The identified non-white block.
        direction: right
        distance: 2 positions
      - action: reconstruct_grid
        description: Create the output grid by placing the shifted block at its new position and filling the remaining positions with white pixels.
        details:
          new_start_index: original_start_index + 2
          output_grid:
            - range(0, new_start_index): white pixels
            - range(new_start_index, new_start_index + length): original non-white block pixels
            - range(new_start_index + length, grid_width): white pixels
    relationships:
      - The output grid dimensions are identical to the input grid dimensions.
      - The color and length of the non-white block are preserved between input and output.
      - The position of the non-white block changes consistently (shift right by 2).
    ```


*   **Natural Language Program:**
    1.  Receive the input grid (a single row).
    2.  Find the first and last index of the contiguous sequence of non-white pixels (the colored block).
    3.  Determine the color and length of this block.
    4.  Calculate the new starting index by adding 2 to the original starting index.
    5.  Create a new output grid of the same size as the input, initially filled entirely with white (0) pixels.
    6.  Copy the original colored block into the output grid, starting at the calculated new starting index.