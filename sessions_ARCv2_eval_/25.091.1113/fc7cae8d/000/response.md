*   **Perception**:
    *   The input grids are relatively large and contain various colors, often including border-like structures or noisy backgrounds.
    *   The output grids are significantly smaller than the corresponding input grids.
    *   Each input grid contains a distinct rectangular frame made of a single color (blue in train\_1, red in train\_2, azure in train\_3).
    *   This colored frame encloses a pattern composed of various colors.
    *   The output grid appears to be the pattern *inside* the colored frame found in the input grid.
    *   The frame itself is not included in the output.
    *   The color used for the frame is consistently the color that forms the largest single-colored rectangle (excluding the background color, white 0) in the input grid.

*   **Facts**:
    
```yaml
    task_elements:
      - item: input_grid
        properties:
          - contains multiple colors
          - includes background noise/elements (often white 0, gray 5)
          - features a large, single-colored rectangular frame (the 'bounding_frame')
          - bounding_frame encloses an inner pattern
      - item: bounding_frame
        properties:
          - rectangular shape
          - composed of a single, non-background color (color C)
          - appears to be the largest such rectangle in the input grid
          - defines the area of interest
        relationships:
          - encloses the inner_pattern
      - item: inner_pattern
        properties:
          - located spatially inside the bounding_frame
          - composed of various colors
        relationships:
          - is extracted to form the output_grid
      - item: output_grid
        properties:
          - smaller dimensions than input_grid
          - identical pixel values and arrangement to the inner_pattern
        relationships:
          - is the extracted inner_pattern from the input_grid

    transformation:
      - action: identify_rectangles
        actor: system
        input: input_grid
        output: list of single-colored rectangles (excluding background color 0)
        details: Find all maximal contiguous rectangular areas composed of a single color C != 0.
      - action: find_largest_rectangle
        actor: system
        input: list of rectangles
        output: the bounding_frame (largest rectangle by area)
        details: Select the rectangle with the maximum area.
      - action: determine_inner_bounds
        actor: system
        input: bounding_frame coordinates (top, left, bottom, right)
        output: inner_pattern coordinates (top+1, left+1, bottom-1, right-1)
      - action: extract_subgrid
        actor: system
        input: input_grid, inner_pattern coordinates
        output: output_grid
        details: Copy the portion of the input_grid defined by the inner_pattern coordinates.
    ```


*   **Natural Language Program**:
    1.  Scan the input grid to identify all contiguous rectangular blocks composed of a single color, ignoring the background color white (0).
    2.  Determine the area (height * width) of each identified rectangle.
    3.  Select the rectangle with the largest area. This rectangle acts as the "bounding frame".
    4.  Define a new, smaller rectangular area by taking the region strictly *inside* the bounding frame (i.e., exclude the frame's border pixels by incrementing the top/left coordinates and decrementing the bottom/right coordinates).
    5.  Extract the subgrid corresponding to this inner rectangular area from the input grid. This extracted subgrid is the output grid.