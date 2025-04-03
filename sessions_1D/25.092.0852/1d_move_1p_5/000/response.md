*   **Perception:** The task involves processing single-row grids (1D arrays). Each input grid contains a single contiguous block of non-white pixels against a white background. The transformation shifts this non-white block exactly one position to the right within the grid. The color of the block, the length of the block, and the size of the grid remain unchanged. The background remains white.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (single row)
    input_features:
      - background:
          color: white (0)
          extent: fills the grid except for the object
      - object:
          count: 1 per grid
          shape: contiguous horizontal block (segment)
          color: non-white (red, green, yellow in examples)
          properties:
            - variable color
            - variable length
            - variable starting position
    transformation:
      - type: translation
      - target: the non-white object
      - parameters:
          direction: right
          distance: 1 pixel (cell)
    output_features:
      - background: same as input
      - object:
          color: same as input object
          length: same as input object
          position: shifted one pixel right compared to input
    grid_properties:
      - size: remains constant between input and output
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input row. Note its color, starting index, and ending index.
    2.  Create an output row of the same length as the input row, initially filled with white pixels (0).
    3.  Copy the identified block of non-white pixels from the input row into the output row, placing it so that its starting index is one greater than its original starting index.