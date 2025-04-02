*   **Perception:**
    *   The input and output grids are single rows (1xN).
    *   Each input grid contains a contiguous horizontal block of a single non-white color (magenta, blue, gray).
    *   Each input grid also contains a single green pixel (color 3).
    *   The non-white, non-green block is always located to the left of the green pixel.
    *   There are white pixels (color 0) between the colored block and the green pixel.
    *   The transformation involves extending the colored block to the right.
    *   The extension stops just before the green pixel.
    *   The white pixels between the original end of the colored block and the green pixel are replaced by the color of the block.
    *   The green pixel itself, and any pixels to its right, remain unchanged.
    *   Pixels to the left of the original colored block also remain unchanged.

*   **Facts YAML:**
    
```yaml
    task_type: array_manipulation_1d
    grid_dimensions: 1xN (single row)
    objects:
      - object_type: contiguous_block
        properties:
          color: non-white (0), non-green (3) # e.g., magenta (6), blue (1), gray (5)
          location: left of the green pixel
          shape: horizontal line segment
          identifier: fill_block
      - object_type: single_pixel
        properties:
          color: green (3)
          location: right of the fill_block
          identifier: boundary_pixel
      - object_type: background_pixels
        properties:
          color: white (0)
          location: between fill_block and boundary_pixel, and potentially elsewhere
    actions:
      - action_type: extend
        actor: fill_block
        direction: right
        target: boundary_pixel (exclusive)
        affected_pixels: background_pixels between fill_block and boundary_pixel
        result: affected_pixels change color to match fill_block color
    relationships:
      - type: spatial
        subject: fill_block
        relation: left_of
        object: boundary_pixel
      - type: boundary
        subject: boundary_pixel
        role: stops the extension of fill_block
    invariants:
      - boundary_pixel color and position
      - pixels to the right of boundary_pixel
      - pixels to the left of the original fill_block
      - color of the fill_block (used for filling)
    ```


*   **Natural Language Program:**
    1.  Identify the column index of the single green pixel (color 3). Let this be `green_col`.
    2.  Find the contiguous horizontal block of a single non-white, non-green color located to the left of `green_col`. Identify its color (let's call it `fill_color`) and the column index of its rightmost pixel (let's call it `fill_end_col`).
    3.  Iterate through the columns from `fill_end_col + 1` up to `green_col - 1`.
    4.  For each column index in this range, change the pixel's color to `fill_color`.
    5.  Leave all other pixels unchanged.