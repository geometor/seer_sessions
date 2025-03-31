*   **Perception:** The input grids consist of an azure (8) background with scattered blue (1) pixels, sometimes forming small horizontal or vertical pairs or single points. The output grids are nearly identical, but certain azure (8) pixels are changed to yellow (4). The positions of the blue (1) pixels remain unchanged. The transformation seems to identify specific locations based on the relative positions of the blue pixels. Specifically, an azure pixel changes color if it lies at the intersection of a "corridor" defined by blue pixels both horizontally and vertically.

*   **Facts YAML:**
    
```yaml
    task_description: Identify specific background pixels (azure, 8) based on the relative positions of foreground pixels (blue, 1) and change their color (to yellow, 4).
    grid_properties:
      - background_color: azure (8)
      - foreground_color: blue (1)
      - change_color: yellow (4)
    objects:
      - type: pixel
        properties:
          - color: Integer (0-9)
          - position: (row, column) coordinate
    actions:
      - name: change_pixel_color
        target_pixels: Azure (8) pixels meeting specific criteria
        new_color: yellow (4)
    conditions_for_change:
      - A pixel at position (r, c) with color azure (8) is changed to yellow (4) if and only if all four of the following conditions are met:
          1. Existence of a blue (1) pixel at position (r', c) where r' < r (above in the same column).
          2. Existence of a blue (1) pixel at position (r'', c) where r'' > r (below in the same column).
          3. Existence of a blue (1) pixel at position (r, c') where c' < c (left in the same row).
          4. Existence of a blue (1) pixel at position (r, c'') where c'' > c (right in the same row).
    invariants:
      - The positions and colors of all blue (1) pixels remain unchanged.
      - Azure (8) pixels not meeting the conditions remain unchanged.
      - The grid dimensions remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel of the input grid at position (row, column).
    3.  If the pixel at (row, column) is azure (8):
        a.  Check if there exists at least one blue (1) pixel in the same column `column` at any row `r_above` such that `r_above < row`.
        b.  Check if there exists at least one blue (1) pixel in the same column `column` at any row `r_below` such that `r_below > row`.
        c.  Check if there exists at least one blue (1) pixel in the same row `row` at any column `c_left` such that `c_left < column`.
        d.  Check if there exists at least one blue (1) pixel in the same row `row` at any column `c_right` such that `c_right > column`.
        e.  If all four conditions (a, b, c, d) are true, change the color of the pixel at (row, column) in the output grid to yellow (4).
    4.  Return the modified output grid.