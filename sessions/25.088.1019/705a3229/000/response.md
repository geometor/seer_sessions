*   **Perception:** The input grids contain a few scattered, non-white pixels on a white background. The output grids show L-shaped lines originating from the positions of the input pixels. Each line segment extends either vertically or horizontally from the original pixel's location towards the nearest edge of the grid. The color of the lines matches the color of the original pixel. If there are multiple colored pixels in the input, the output is the overlay of the corresponding L-shapes.

*   **YAML Facts:**
    
```yaml
    task_description: Draw L-shaped lines from each non-white pixel to its two nearest cardinal edges.
    grid_properties:
      - background_color: 0 (white)
      - dimensions: Variable height and width (observed range: 11x8 to 14x15).
    objects:
      - name: source_pixel
        description: A single pixel with a color other than white (0).
        properties:
          - location: (row, column) coordinates.
          - color: An integer from 1 to 9.
    relationships:
      - type: spatial
        description: Each source_pixel determines the location and color of generated lines.
        from: source_pixel
        to: output_lines
      - type: distance_based
        description: The extent and direction of the lines depend on the source_pixel's distance to the four grid edges (top, bottom, left, right).
    actions:
      - name: identify_source_pixels
        input: input_grid
        output: List of (row, column, color) for each non-white pixel.
      - name: determine_nearest_edges
        input: source_pixel location (r, c), grid dimensions (H, W)
        output: Nearest vertical edge (top or bottom row index), Nearest horizontal edge (left or right column index).
        details: Compare distance to top (r) vs bottom (H-1-r). Choose the smaller distance. If equal, choose top (row 0). Compare distance to left (c) vs right (W-1-c). Choose the smaller distance. If equal, choose left (col 0).
      - name: draw_lines
        input: source_pixel (r, c, color), nearest vertical edge row (r_target), nearest horizontal edge column (c_target), output_grid
        output: Modified output_grid with lines drawn.
        details: Draw a vertical line segment of the source_pixel's color connecting (r, c) to (r_target, c). Draw a horizontal line segment of the source_pixel's color connecting (r, c) to (r, c_target).
      - name: overlay_results
        input: Lines drawn for all source_pixels.
        output: Final output grid.
        details: Combine all drawn lines onto an initial white grid of the same dimensions as the input.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
    2.  Iterate through each pixel `(r, c)` of the input grid.
    3.  If the pixel at `(r, c)` is not the background color (white, 0):
        a.  Record its color, `pixel_color`.
        b.  Get the grid dimensions: height `H` and width `W`.
        c.  Determine the target row `r_target`: if the distance to the top edge (`r`) is less than or equal to the distance to the bottom edge (`H - 1 - r`), set `r_target` to 0 (top edge); otherwise, set `r_target` to `H - 1` (bottom edge).
        d.  Determine the target column `c_target`: if the distance to the left edge (`c`) is less than or equal to the distance to the right edge (`W - 1 - c`), set `c_target` to 0 (left edge); otherwise, set `c_target` to `W - 1` (right edge).
        e.  Draw the vertical line segment: For each row `i` from `min(r, r_target)` to `max(r, r_target)` (inclusive), set the pixel at `(i, c)` in the output grid to `pixel_color`.
        f.  Draw the horizontal line segment: For each column `j` from `min(c, c_target)` to `max(c, c_target)` (inclusive), set the pixel at `(r, j)` in the output grid to `pixel_color`.
    4.  After checking all pixels in the input grid, return the final output grid.