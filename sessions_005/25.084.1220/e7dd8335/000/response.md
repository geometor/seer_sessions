*   **Perception**:
    The task involves transforming an input grid containing white (0) background pixels and a distinct shape made of blue (1) pixels into an output grid. The output grid retains the overall structure and background of the input grid, but modifies the color of some blue pixels within the shape. Specifically, the blue pixels located in the lower portion of the shape's vertical extent are changed to red (2). The division between the unchanged upper portion and the changed lower portion appears to be determined by the vertical midpoint of the blue shape.

*   **Facts**:
    
```yaml
    elements:
      - type: grid
        properties:
          height: variable (e.g., 8, 7, 9)
          width: variable (e.g., 9, 7, 9)
      - type: color
        values:
          - white: 0 (background)
          - blue: 1 (input shape color)
          - red: 2 (output changed color)
      - type: object
        description: A single contiguous or structured shape composed of blue pixels.
        properties:
          color: blue (1)
          location: variable within the grid
          vertical_extent:
            min_row: minimum row index containing a blue pixel
            max_row: maximum row index containing a blue pixel
    transformation:
      - action: identify_pixels
        target_color: blue (1)
        result: coordinates of all blue pixels
      - action: calculate_bounds
        input: coordinates of blue pixels
        result: minimum and maximum row indices (min_row, max_row)
      - action: calculate_midpoint_row
        formula: floor((min_row + max_row) / 2)
        result: dividing_row_index
      - action: determine_change_threshold
        formula: dividing_row_index + 1
        result: change_start_row
      - action: copy_grid
        source: input grid
        destination: output grid
      - action: change_color
        target: output grid
        condition: pixel is blue (1) AND its row index >= change_start_row
        new_color: red (2)
    relationship:
      - The color change from blue to red is spatially dependent on the vertical position relative to the overall vertical center of all blue pixels combined.
    ```


*   **Natural Language Program**:
    1.  Identify all pixels in the input grid that have the color blue (1).
    2.  Determine the minimum row index (`min_row`) and the maximum row index (`max_row`) occupied by any blue pixel.
    3.  Calculate the row index that marks the beginning of the lower half of the blue shape's vertical extent. This is `change_start_row = floor((min_row + max_row) / 2) + 1`.
    4.  Create the output grid as a copy of the input grid.
    5.  Iterate through each pixel of the copied grid. If a pixel has the color blue (1) and its row index is greater than or equal to `change_start_row`, change its color to red (2).
    6.  Leave all other pixels in the output grid unchanged from the input grid.