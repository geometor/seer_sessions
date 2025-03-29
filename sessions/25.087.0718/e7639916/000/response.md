*   **Perception of the elements:**
    *   The input grids contain a background of white (0) pixels and several isolated azure (8) pixels.
    *   The output grids retain the original azure pixels.
    *   Blue (1) pixels are added to the output grid.
    *   The added blue pixels form a rectangular frame or bounding box.
    *   This bounding box encloses all the azure pixels present in the input.
    *   The boundary lines of the box are drawn such that they align with the outermost azure pixels in each direction (top, bottom, left, right).
    *   The corners of the bounding box correspond to the minimum and maximum row and column indices of the azure pixels.
    *   The blue pixels replace the white background pixels along the perimeter of this bounding box, but they do not overwrite the original azure pixels if they happen to fall on the boundary.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - background_color: white (0)
      - object_color: azure (8)
      - output_frame_color: blue (1)
    objects:
      - type: discrete_pixels
        color: azure (8)
        count: variable (2 or more in examples)
        distribution: scattered across the grid
    transformation:
      - action: identify_objects
        target: azure (8) pixels
        result: set of coordinates for all azure pixels
      - action: compute_bounding_box
        input: set of azure pixel coordinates
        output: min_row, max_row, min_col, max_col defining the smallest rectangle enclosing all azure pixels
      - action: copy_grid
        source: input grid
        target: output grid
      - action: draw_rectangle_frame
        target: output grid
        color: blue (1)
        location: perimeter defined by min_row, max_row, min_col, max_col
        condition: draw blue (1) only on white (0) pixels; preserve original azure (8) pixels if they lie on the frame perimeter.
    relationships:
      - The blue (1) frame in the output is determined by the spatial extent (min/max row/col) of the azure (8) pixels in the input.
      - The output grid preserves the original azure (8) pixels' locations.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Find the locations (row and column indices) of all azure (8) pixels in the input grid.
    3.  Determine the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among all identified azure pixel locations.
    4.  Iterate through the columns from `min_col` to `max_col`:
        *   If the pixel at (`min_row`, column) in the output grid is white (0), change it to blue (1).
        *   If the pixel at (`max_row`, column) in the output grid is white (0), change it to blue (1).
    5.  Iterate through the rows from `min_row` to `max_row`:
        *   If the pixel at (row, `min_col`) in the output grid is white (0), change it to blue (1).
        *   If the pixel at (row, `max_col`) in the output grid is white (0), change it to blue (1).
    6.  The resulting grid is the final output.