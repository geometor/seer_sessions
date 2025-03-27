*   **Perception:**
    *   All input grids are 8x8.
    *   The background color is consistently orange (7).
    *   Each input grid contains exactly one pixel of a non-orange color, located at one of the four corners: (0,0), (0,7), (7,0), or (7,7).
    *   The output grid is also 8x8, with an orange background.
    *   In the output grid, the original non-orange pixel from the input corner is replaced by the orange background color.
    *   A new 3-pixel shape, using the same non-orange color as the input pixel, appears in the output grid.
    *   The specific shape and location of this 3-pixel object depend deterministically on which corner the original non-orange pixel occupied in the input.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_size: [8, 8]
      background_color: 7 # orange
    
    input_elements:
      - object: background
        color: 7
        shape: full_grid
      - object: marker_pixel
        count: 1
        color: non_orange (1, 8, 0, or 9 in examples)
        location: one_of_four_corners [(0,0), (0,7), (7,0), (7,7)]
        
    output_elements:
      - object: background
        color: 7
        shape: full_grid
      - object: output_shape
        count: 1
        color: same_as_marker_pixel
        pixels: 3
        shape_and_location: dependent_on_marker_pixel_corner_location
        
    transformations:
      - action: find_marker_pixel
        input: input_grid
        output: marker_pixel_location, marker_pixel_color
      - action: identify_corner
        input: marker_pixel_location
        output: corner_type (top_left, top_right, bottom_left, bottom_right)
      - action: initialize_output_grid
        size: [8, 8]
        fill_color: 7 # orange
      - action: draw_output_shape
        target: output_grid
        color: marker_pixel_color
        shape_definition: specific_3_pixel_pattern
        location_rule: specific_offset_based_on_corner_type_and_marker_pixel_location
        
    corner_specific_rules:
      - corner: top_left (0, 0)
        output_shape_relative_coords: [(+1,+1), (+1,+2), (+2,+1)] 
      - corner: top_right (0, 7)
        output_shape_relative_coords: [(+1,-2), (+1,-1), (+2,-1)] 
      - corner: bottom_left (7, 0)
        output_shape_relative_coords: [(-3,+2), (-2,+2), (-1,+3)] 
      - corner: bottom_right (7, 7)
        output_shape_relative_coords: [(-3,-2), (-2,-2), (-1,-3)] 
    ```


*   **Natural Language Program:**
    1.  Identify the single non-orange pixel (the "marker pixel") in the 8x8 input grid. Record its color and its coordinates `(row, col)`.
    2.  Determine which corner the marker pixel occupies:
        *   If `(row, col)` is `(0, 0)`, it's the top-left corner.
        *   If `(row, col)` is `(0, 7)`, it's the top-right corner.
        *   If `(row, col)` is `(7, 0)`, it's the bottom-left corner.
        *   If `(row, col)` is `(7, 7)`, it's the bottom-right corner.
    3.  Create a new 8x8 output grid filled entirely with orange (7).
    4.  Based on the identified corner, draw a specific 3-pixel shape using the marker pixel's color onto the output grid at coordinates relative to the original marker pixel's location `(row, col)`:
        *   If the corner was top-left `(0, 0)`, draw pixels at `(row+1, col+1)`, `(row+1, col+2)`, and `(row+2, col+1)`.
        *   If the corner was top-right `(0, 7)`, draw pixels at `(row+1, col-2)`, `(row+1, col-1)`, and `(row+2, col-1)`.
        *   If the corner was bottom-left `(7, 0)`, draw pixels at `(row-3, col+2)`, `(row-2, col+2)`, and `(row-1, col+3)`.
        *   If the corner was bottom-right `(7, 7)`, draw pixels at `(row-3, col-2)`, `(row-2, col-2)`, and `(row-1, col-3)`.
    5.  The resulting grid is the final output.