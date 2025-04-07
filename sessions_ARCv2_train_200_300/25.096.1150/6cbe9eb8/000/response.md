*   **Perception:**
    *   The input is a grid of single digits.
    *   There is a clear repeating background pattern composed of low digits (e.g., `0 1 2 3` or `0 1`).
    *   Embedded within the background are distinct shapes or regions formed by digits other than the background pattern digits (e.g., `8`, `3`, `4`, `5`, `6`).
    *   One of these shapes acts as an outer frame or boundary.
    *   The output is a smaller grid derived from a specific region of the input.
    *   The output grid seems to capture the content within the identified outer frame.
    *   The background pattern digits within the frame in the input are replaced by `0` in the output, while the frame itself and any other embedded shapes within it are preserved.

*   **Facts:**
    
```yaml
    task_elements:
      - item: input_grid
        description: A 2D array of integers.
        properties:
          - contains_background_pattern: True
          - background_digits: Low integers, repeating sequence (e.g., [0, 1, 2, 3] or [0, 1]).
          - contains_embedded_shapes: True
          - shape_digits: Integers distinct from background digits (e.g., 8, 3, 4, 5, 6).
          - framing_shape: One specific embedded shape acts as an outer boundary for the relevant area.
      - item: output_grid
        description: A 2D array of integers, smaller than the input grid.
        properties:
          - derived_from: input_grid
          - content: Corresponds to the area within and including the framing_shape from the input.
          - background_replacement: Background pattern digits from the input, if inside the frame, are replaced with 0.
          - preserved_elements: The framing_shape digits and any other embedded_shape digits within the frame are kept.
    actions:
      - action: identify_background_pattern
        input: input_grid
        output: background_digits list
      - action: identify_non_background_shapes
        input: input_grid, background_digits
        output: list of shapes (connected components of non-background digits)
      - action: identify_framing_shape
        input: list of shapes
        description: Determine which shape forms the outermost boundary enclosing other non-background elements or the largest relevant area. This seems to often be the shape defining the largest bounding box containing other non-background shapes.
        output: framing_shape (a specific shape object/data)
      - action: get_bounding_box
        input: framing_shape
        output: coordinates (min_row, min_col, max_row, max_col)
      - action: extract_subgrid
        input: input_grid, bounding_box
        output: initial_output_grid (subgrid from input corresponding to bounding box)
      - action: transform_subgrid
        input: initial_output_grid, framing_shape, background_digits
        description: Iterate through the extracted subgrid. If a cell's value is part of the background_digits list AND it's not part of the framing_shape itself, change its value to 0. Otherwise, keep the original value.
        output: final_output_grid
    relationships:
      - The output grid's dimensions and content are determined by the framing_shape identified in the input grid.
      - Digits within the output grid are either preserved from the input (framing shape, other embedded shapes) or replaced with 0 (background pattern digits inside the frame).
    ```


*   **Natural Language Program:**
    1.  Analyze the input grid to identify the repeating background pattern digits (usually low integers like 0, 1, 2, 3).
    2.  Identify all connected components (shapes) formed by digits that are *not* part of the background pattern.
    3.  Determine which of these shapes serves as the "framing shape". This is typically the shape that forms the outermost boundary enclosing other non-background shapes or defines the primary region of interest. (Heuristically, this might be the shape whose bounding box contains most or all other non-background pixels).
    4.  Calculate the bounding box (minimum and maximum row and column indices) of the identified framing shape.
    5.  Create the output grid with dimensions matching the bounding box.
    6.  Iterate through each cell within the bounding box coordinates in the input grid.
    7.  For each cell `(row, col)` within the bounding box:
        *   Get the digit `d` from the input grid at `(row, col)`.
        *   Check if `d` is one of the background pattern digits identified in step 1.
        *   Check if the cell `(row, col)` belongs to the framing shape identified in step 3.
        *   If `d` is a background digit AND the cell `(row, col)` is *not* part of the framing shape, place `0` in the corresponding cell of the output grid.
        *   Otherwise (if `d` is not a background digit, or if it is part of the framing shape), place the original digit `d` in the corresponding cell of the output grid.
    8.  Return the final output grid.