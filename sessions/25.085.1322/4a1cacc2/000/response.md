*   **Perception of Task Elements:**
    *   The input grids consist primarily of a single background color (Azure, 8).
    *   Each input grid contains exactly one pixel of a different, non-background color. Let's call this the "trigger pixel".
    *   The output grid retains the same dimensions and background color as the input grid.
    *   The trigger pixel's color and position in the input determine the color and location of a solid rectangle drawn in the output grid.
    *   The position of the trigger pixel relative to the center of the grid determines which corner the rectangle is anchored to and expands from/towards.
    *   The rectangle in the output always includes the original position of the trigger pixel and is filled with the trigger pixel's color.

*   **YAML Fact Documentation:**
    
```yaml
    task_description: Identify a single unique pixel and use its color and position relative to the grid center to draw a filled rectangle in the corresponding corner quadrant of the output grid.

    elements:
      - element: grid
        properties:
          - background_color: Azure (8), the most frequent color.
          - dimensions: Height (H) and Width (W) vary between examples.
      - element: trigger_pixel
        properties:
          - type: The single pixel with a color different from the background.
          - color: C (varies: Yellow, Maroon, Magenta).
          - position: (row, col).
      - element: output_rectangle
        properties:
          - color: Same as trigger_pixel color C.
          - shape: Solid rectangle.
          - position_anchor: Determined by the quadrant of the trigger_pixel.
          - dimensions: Determined by the trigger_pixel position (row, col) and grid dimensions (H, W).

    relationships:
      - relationship: trigger_pixel_to_quadrant
        description: The quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) is determined by comparing the trigger_pixel's (row, col) to the grid's center (H/2, W/2).
          - Top-Left: row < H/2 and col < W/2
          - Top-Right: row < H/2 and col >= W/2
          - Bottom-Left: row >= H/2 and col < W/2
          - Bottom-Right: row >= H/2 and col >= W/2
      - relationship: quadrant_to_rectangle_definition
        description: The determined quadrant dictates the bounds of the output_rectangle.
          - Top-Left: Rows 0 to row, Columns 0 to col.
          - Top-Right: Rows 0 to row, Columns col to W-1.
          - Bottom-Left: Rows row to H-1, Columns 0 to col.
          - Bottom-Right: Rows row to H-1, Columns col to W-1.

    transformation:
      - action: copy_grid
        source: input_grid
        target: output_grid
        description: Initialize the output grid as a copy of the input grid.
      - action: identify_trigger
        source: input_grid
        target: trigger_pixel (color C, position (row, col))
        description: Find the single pixel that is not the background color.
      - action: determine_quadrant
        source: trigger_pixel position (row, col), grid dimensions (H, W)
        target: quadrant name
        description: Calculate which quadrant the trigger pixel falls into.
      - action: fill_rectangle
        source: quadrant name, trigger_pixel color C, grid dimensions (H, W)
        target: output_grid
        description: Fill the rectangular area corresponding to the determined quadrant with color C.
    ```


*   **Natural Language Program:**
    1.  Create the output grid as an exact copy of the input grid.
    2.  Identify the background color, which is the most frequent color in the input grid (Azure, 8).
    3.  Locate the single pixel in the input grid that has a color different from the background color. Let this pixel's color be `C` and its position be `(row, col)`.
    4.  Determine the dimensions of the grid: height `H` and width `W`.
    5.  Determine the quadrant where the pixel at `(row, col)` is located by comparing its coordinates to the center of the grid (`H/2`, `W/2`).
        *   If `row < H / 2` and `col < W / 2`, the quadrant is Top-Left.
        *   If `row < H / 2` and `col >= W / 2`, the quadrant is Top-Right.
        *   If `row >= H / 2` and `col < W / 2`, the quadrant is Bottom-Left.
        *   If `row >= H / 2` and `col >= W / 2`, the quadrant is Bottom-Right.
    6.  Based on the determined quadrant, fill a rectangular region in the output grid with color `C`:
        *   For Top-Left quadrant: Fill all pixels `(r, c)` where `0 <= r <= row` and `0 <= c <= col`.
        *   For Top-Right quadrant: Fill all pixels `(r, c)` where `0 <= r <= row` and `col <= c < W`.
        *   For Bottom-Left quadrant: Fill all pixels `(r, c)` where `row <= r < H` and `0 <= c <= col`.
        *   For Bottom-Right quadrant: Fill all pixels `(r, c)` where `row <= r < H` and `col <= c < W`.