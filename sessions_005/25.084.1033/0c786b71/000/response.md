*   **Perception**
    *   The input is a rectangular grid of pixels with varying colors.
    *   The output is also a rectangular grid of pixels, using the same colors as the input.
    *   The output grid's dimensions are exactly double the input grid's dimensions (twice the height and twice the width).
    *   Visually, the output grid appears to be composed of four copies of the input grid, each transformed (flipped or rotated) and arranged in a 2x2 layout.
    *   Specifically, comparing the input and output across the examples:
        *   The bottom-right quadrant of the output looks identical to the input grid.
        *   The bottom-left quadrant looks like the input grid flipped horizontally.
        *   The top-right quadrant looks like the input grid flipped vertically.
        *   The top-left quadrant looks like the input grid flipped both horizontally and vertically (or rotated 180 degrees).

*   **Facts**
    
```yaml
    task_description: Construct a larger grid by arranging transformed versions of the input grid.

    elements:
      - element: input_grid
        description: A grid of pixels with height H and width W.
      - element: output_grid
        description: A grid of pixels with height 2*H and width 2*W.
        properties:
          - composed_of_four_quadrants
          - each_quadrant_size: H x W

    transformations:
      - transformation: flip_horizontal
        input: input_grid
        output: grid_flipped_h
      - transformation: flip_vertical
        input: input_grid
        output: grid_flipped_v
      - transformation: rotate_180
        description: Equivalent to flipping horizontally and then vertically.
        input: input_grid
        output: grid_rotated_180

    relationships:
      - relationship: quadrant_placement
        description: The output grid is formed by placing grids into four quadrants.
        details:
          - quadrant: top_left (rows 0 to H-1, cols 0 to W-1)
            content: grid_rotated_180
          - quadrant: top_right (rows 0 to H-1, cols W to 2*W-1)
            content: grid_flipped_v
          - quadrant: bottom_left (rows H to 2*H-1, cols 0 to W-1)
            content: grid_flipped_h
          - quadrant: bottom_right (rows H to 2*H-1, cols W to 2*W-1)
            content: input_grid # The original input grid
    ```


*   **Natural Language Program**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Create a new output grid with height 2*H and width 2*W.
    3.  Generate three transformed versions of the input grid:
        a.  `flipped_h`: Flip the input grid horizontally.
        b.  `flipped_v`: Flip the input grid vertically.
        c.  `rotated_180`: Rotate the input grid by 180 degrees (or flip horizontally then vertically).
    4.  Populate the four quadrants of the output grid:
        a.  Copy the `rotated_180` grid into the top-left quadrant (rows 0 to H-1, columns 0 to W-1).
        b.  Copy the `flipped_v` grid into the top-right quadrant (rows 0 to H-1, columns W to 2*W-1).
        c.  Copy the `flipped_h` grid into the bottom-left quadrant (rows H to 2*H-1, columns 0 to W-1).
        d.  Copy the original input grid into the bottom-right quadrant (rows H to 2*H-1, columns W to 2*W-1).
    5.  Return the completed output grid.