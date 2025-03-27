*   **Perception:** The task involves expanding an input grid by adding a border around it. The output grid is always two rows taller and two columns wider than the input grid. The content of the new border is derived from the border pixels of the original input grid, while the corners of the new border are filled with a default color (white/0).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    transformation: padding
    input_grid:
      description: A 2D grid of pixels with varying dimensions and colors.
      properties:
        height: H
        width: W
    output_grid:
      description: A 2D grid of pixels derived from the input grid.
      properties:
        height: H + 2
        width: W + 2
        relationship_to_input:
          - type: contains_copy
            source: input_grid
            location: center block (rows 1 to H, columns 1 to W)
          - type: border_population
            source: input_grid borders
            target: output_grid border (excluding corners)
            details:
              - Output top border (row 0, cols 1 to W) is a copy of Input top border (row 0).
              - Output bottom border (row H+1, cols 1 to W) is a copy of Input bottom border (row H-1).
              - Output left border (col 0, rows 1 to H) is a copy of Input left border (col 0).
              - Output right border (col W+1, rows 1 to H) is a copy of Input right border (col W-1).
          - type: corner_filling
            location: four corners of the output grid (0,0), (0, W+1), (H+1, 0), (H+1, W+1)
            value: white (0)
    objects:
      - id: input_grid
        pixels: contiguous block representing the entire input
      - id: output_grid
        pixels: contiguous block representing the entire output
      - id: central_block (in output)
        pixels: copy of the input_grid
      - id: border (in output)
        pixels: the outermost rows and columns of the output grid
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Create a new output grid with dimensions (H+2) x (W+2), initially filled entirely with the white color (0).
    3.  Copy the entire input grid into the center of the output grid, specifically placing the input grid's top-left corner at output grid coordinates (row 1, column 1). This fills the region from row 1 to H and column 1 to W of the output grid.
    4.  Copy the first row of the input grid (row 0) into the output grid's first row (row 0), but only for columns 1 through W.
    5.  Copy the last row of the input grid (row H-1) into the output grid's last row (row H+1), but only for columns 1 through W.
    6.  Copy the first column of the input grid (column 0) into the output grid's first column (column 0), but only for rows 1 through H.
    7.  Copy the last column of the input grid (column W-1) into the output grid's last column (column W+1), but only for rows 1 through H.
    8.  The four corner cells of the output grid (at coordinates (0,0), (0, W+1), (H+1, 0), and (H+1, W+1)) remain white (0) as set in step 2.
    9.  Return the completed output grid.