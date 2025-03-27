*   **Perception of Task Elements:**
    *   Each task involves an input grid and an output grid.
    *   The input grids have varying dimensions (8x8, 6x6, 12x6).
    *   The output grids consistently have dimensions 2x2.
    *   Visually comparing the input and output grids, the output grid appears to be a direct copy of a portion of the input grid.
    *   Specifically, the output grid matches the pixels found in the top-left 2x2 corner of the input grid in all examples.
    *   Example 1 Input: `[[2, 4, ...], [2, 5, ...], ...]` -> Output: `[[2, 4], [2, 5]]`
    *   Example 2 Input: `[[4, 3, ...], [6, 0, ...], ...]` -> Output: `[[4, 3], [6, 0]]`
    *   Example 3 Input: `[[3, 2, ...], [1, 4, ...], ...]` -> Output: `[[3, 2], [1, 4]]`
    *   Some input grids (Example 1 and 3) show patterns of repetition, but this seems irrelevant to the transformation rule itself, which focuses solely on the top-left corner.

*   **YAML Facts:**
    
```yaml
    task_description: Extract the top-left 2x2 subgrid from the input grid.
    
    elements:
      - element: input_grid
        description: A 2D grid of pixels with varying dimensions and colors.
      - element: output_grid
        description: A 2D grid of pixels with fixed dimensions 2x2.
        
    relationships:
      - type: subset
        from: output_grid
        to: input_grid
        detail: The output grid is a subgrid of the input grid.
        
    properties:
      - element: output_grid
        property: size
        value: [2, 2] # height, width
      - element: output_grid
        property: location_in_input
        value: top-left corner (rows 0-1, columns 0-1)
        
    transformation:
      action: extract_subgrid
      input: input_grid
      output: output_grid
      parameters:
        top_row: 0
        left_col: 0
        height: 2
        width: 2
        
    consistency_check:
      - example: 1
        input_top_left_2x2: [[2, 4], [2, 5]]
        output: [[2, 4], [2, 5]]
        match: true
      - example: 2
        input_top_left_2x2: [[4, 3], [6, 0]]
        output: [[4, 3], [6, 0]]
        match: true
      - example: 3
        input_top_left_2x2: [[3, 2], [1, 4]]
        output: [[3, 2], [1, 4]]
        match: true
    ```


*   **Natural Language Program:**
    1.  Identify the input grid.
    2.  Select the subgrid located at the top-left corner of the input grid.
    3.  This subgrid spans the first 2 rows (row index 0 and 1) and the first 2 columns (column index 0 and 1).
    4.  Create the output grid by copying the pixel values from this selected 2x2 subgrid.