*   **Perception:** The input grids contain one or more solid rectangular blocks of azure pixels (8) on a white background (0). The output grids retain the white background but replace the azure blocks with patterns composed of five colors: magenta (6), blue (1), red (2), green (3), and yellow (4). The pattern within each replaced block seems determined by the pixel's position relative to the block's boundaries and center. Specifically, there appears to be a border region (2 pixels thick) and a central region. The border color depends on which side (top, bottom, left, right) it belongs to and whether it's in the first or second half (vertically or horizontally) of that side. The central area is filled with yellow. The transformation is applied independently to each azure block found in the input.

*   **Facts:**
    
```yaml
    task_elements:
      - element: background
        color: white (0)
        properties: Remains unchanged in the output.
      - element: block
        color: azure (8)
        properties:
          - shape: rectangle
          - solid_color: true
          - location: variable
          - size: variable (height H, width W)
        actions:
          - Replaced by a multi-colored pattern in the output.
      - element: pattern
        colors: [magenta (6), blue (1), red (2), green (3), yellow (4)]
        properties:
          - Fills the area originally occupied by an azure block.
          - Structure depends on internal position within the block.
          - Contains a border region and a central region.
          - border_thickness: 2 pixels
          - central_color: yellow (4)
          - border_colors: determined by side (top/bottom/left/right) and position relative to block midpoints (H//2, W//2).
            - Top border: magenta (left half), blue (right half)
            - Bottom border: red (left half), green (right half)
            - Left border (excluding top/bottom): magenta (top half), red (bottom half)
            - Right border (excluding top/bottom): blue (top half), green (bottom half)
    relationships:
      - Each azure block in the input corresponds to exactly one patterned block in the output, occupying the same bounding box.
      - The pattern's structure (colors and their arrangement) is solely determined by the dimensions (H, W) of the original azure block and the relative coordinates within it.
    constants:
      - border_thickness: 2
      - pattern_colors: {top_left: 6, top_right: 1, bottom_left: 2, bottom_right: 3, center: 4}
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct, contiguous rectangular blocks composed solely of azure pixels (8).
    3.  For each identified azure block:
        a.  Determine its bounding box: top row (`r0`), leftmost column (`c0`), height (`H`), and width (`W`).
        b.  Calculate the horizontal midpoint index: `mid_h = H // 2`.
        c.  Calculate the vertical midpoint index: `mid_w = W // 2`.
        d.  Define the border thickness: `T = 2`.
        e.  Iterate through each pixel within the block's bounding box, using global coordinates (`row`, `col`) where `r0 <= row < r0 + H` and `c0 <= col < c0 + W`.
        f.  Calculate the local coordinates relative to the block's top-left corner: `r = row - r0`, `c = col - c0`.
        g.  Determine the output color for the pixel at (`row`, `col`) based on its local coordinates (`r`, `c`):
            i.  If `r < T` (pixel is in the top border rows): Set the output pixel color to magenta (6) if `c < mid_w`, otherwise set it to blue (1).
            ii. Else if `r >= H - T` (pixel is in the bottom border rows): Set the output pixel color to red (2) if `c < mid_w`, otherwise set it to green (3).
            iii. Else if `c < T` (pixel is in the left border columns, excluding already handled top/bottom border rows): Set the output pixel color to magenta (6) if `r < mid_h`, otherwise set it to red (2).
            iv. Else if `c >= W - T` (pixel is in the right border columns, excluding already handled top/bottom border rows): Set the output pixel color to blue (1) if `r < mid_h`, otherwise set it to green (3).
            v.  Else (pixel is in the central region): Set the output pixel color to yellow (4).
    4.  Return the modified output grid.