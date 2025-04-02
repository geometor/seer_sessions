*   **Perception:** The task involves operating on 1-dimensional grids (or grids with a single row). Each input grid contains a single contiguous block of a non-white color, surrounded by white (0) pixels. The transformation involves shifting this colored block exactly 3 positions to the right within the grid, while maintaining the grid's dimensions and the surrounding white pixels. The specific color and length of the block can vary between examples.

*   **Facts:**
    
```yaml
    task_type: Grid transformation
    grid_dimensionality: 1D (single row)
    input_characteristics:
      - Contains a single contiguous block of non-white pixels.
      - The non-white block is surrounded by white (0) pixels.
      - The color of the block varies (azure, green, orange in examples).
      - The length of the block varies.
      - The starting position of the block varies.
      - Grid dimensions are consistent between input and output.
    output_characteristics:
      - Contains the same non-white block as the input.
      - The block is shifted compared to the input.
      - Surrounded by white (0) pixels.
      - Grid dimensions are consistent with the input.
    transformation:
      - Identify the contiguous block of non-white pixels.
      - Determine the starting index of this block.
      - Shift the entire block exactly 3 positions to the right (increase starting index by 3).
      - Maintain the background white pixels and grid dimensions.
    relationships:
      - The non-white block is treated as a single object.
      - The action is a spatial translation (shift) applied to this object.
      - The magnitude of the shift is constant (3 positions to the right).
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to find the start index, end index, and color of the contiguous block of non-white pixels.
    2.  Create a new output grid with the same dimensions as the input grid, initially filled with white (0) pixels.
    3.  Calculate the new start index for the block by adding 3 to the original start index found in step 1.
    4.  Copy the identified non-white block from the input grid into the output grid, starting at the calculated new start index.