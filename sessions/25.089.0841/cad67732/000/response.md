*   **Perception:**
    *   The task involves resizing the input grid and duplicating its content.
    *   In all examples, the output grid's dimensions are exactly double the input grid's dimensions (both height and width).
    *   The original input grid pattern is consistently copied into the top-left quadrant of the output grid.
    *   An identical copy of the input grid pattern is also placed in the bottom-right quadrant of the output grid.
    *   The remaining two quadrants (top-right and bottom-left) of the output grid are filled entirely with the background color, which is white (0) in all examples.
    *   There are no modifications to the pixel values themselves; the transformation is purely structural (resizing and copying).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    input_grid:
        properties:
            - variable_size: H x W (height x width)
            - contains_pixels: values 0-9
            - background_color: typically 0 (white) but potentially others
    output_grid:
        properties:
            - size: 2H x 2W (double the input dimensions)
            - background_color: matches input background (0 in examples)
    transformation:
        actions:
            - resize: create an output grid of size 2H x 2W, initialized with the background color.
            - copy: place the entire input grid into the top-left quadrant of the output grid (coordinates [0:H, 0:W]).
            - duplicate: place an identical copy of the input grid into the bottom-right quadrant of the output grid (coordinates [H:2H, W:2W]).
        relationships:
            - output_size_is_double_input_size
            - output_contains_two_copies_of_input
            - copies_are_placed_diagonally_adjacent
            - other_quadrants_are_filled_with_background
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Create a new output grid with height 2H and width 2W.
    3.  Initialize all cells of the new output grid with the background color (white/0).
    4.  Copy the content of the input grid into the top-left quadrant of the output grid (rows 0 to H-1, columns 0 to W-1).
    5.  Copy the content of the input grid again into the bottom-right quadrant of the output grid (rows H to 2H-1, columns W to 2W-1).
    6.  Return the completed output grid.