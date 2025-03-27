*   **Perception:**
    *   Each input grid contains a distinct rectangular area composed entirely of `white` (0) pixels.
    *   The rest of the input grid contains various other colors, often forming a background or other shapes, but these seem irrelevant to the output.
    *   The `white` rectangle contains pixels of other colors (non-`white`).
    *   The output grid's dimensions match the dimensions of the `white` rectangle found in the input grid.
    *   The content of the output grid is identical to the content found within the boundaries of the `white` rectangle in the input grid.
    *   The task appears to be extracting the subgrid defined by the `white` rectangular region.

*   **Facts:**
    
```yaml
    task_elements:
      - item: input_grid
        description: A 2D grid of pixels with varying colors and dimensions.
        properties:
          - contains a unique rectangular region composed solely of white (0) pixels.
          - contains other colored pixels inside and outside the white rectangle.
      - item: white_rectangle
        description: A rectangular subgrid within the input_grid composed entirely of white (0) pixels.
        properties:
          - location: Varies between examples.
          - size: Varies between examples.
          - content: Pixels within its boundaries in the input grid can be any color, including white.
        relationship: Defines the boundaries for extraction.
      - item: output_grid
        description: A 2D grid of pixels.
        properties:
          - dimensions: Matches the dimensions of the white_rectangle in the corresponding input_grid.
          - content: Identical to the pixels found within the boundaries of the white_rectangle in the input_grid.
        relationship: Represents the extracted subgrid from the input_grid.
    transformation:
      action: extraction
      input: input_grid
      output: output_grid
      rule: Identify the white_rectangle in the input_grid and copy the pixels within its boundaries to create the output_grid.

    ```


*   **Natural Language Program:**
    1.  Identify the rectangular region within the input grid that consists entirely of `white` (0) pixels.
    2.  Determine the top-left and bottom-right coordinates of this `white` rectangle.
    3.  Create a new grid whose dimensions match the height and width of the identified `white` rectangle.
    4.  Copy the pixels from the input grid located within the boundaries of the `white` rectangle into the new grid, preserving their relative positions. This new grid is the output.