**Perception**

1.  **Grid Size:** The input and output grids have the same dimensions in all examples (19x19).
2.  **Background:** The background color is white (0) and remains unchanged in the output.
3.  **Input Pixels:** The input grids contain a few scattered non-white pixels. Their initial positions vary across examples, but they tend to be concentrated in one quadrant (e.g., top-left in example 2, top-right in example 1).
4.  **Output Pattern:** The output grid is created by taking each non-white pixel from the input grid and reflecting it across the grid's central horizontal axis, central vertical axis, and diagonally through the center point. This creates a four-way symmetry. The original input pixels are preserved in the output.
5.  **Reflection Logic:**
    *   For a grid of height H and width W, the central horizontal axis is conceptually between rows `floor((H-1)/2)` and `ceil((H-1)/2)`, and the central vertical axis is between columns `floor((W-1)/2)` and `ceil((W-1)/2)`.
    *   A pixel at `(r, c)` reflects horizontally to `(r, W - 1 - c)`.
    *   A pixel at `(r, c)` reflects vertically to `(H - 1 - r, c)`.
    *   A pixel at `(r, c)` reflects diagonally (horizontally then vertically, or vice versa) to `(H - 1 - r, W - 1 - c)`.
6.  **Color Preservation:** The color of the reflected pixels is the same as the color of the original pixel.

**YAML Facts**


```yaml
grid_properties:
  - dimensions: Input and output grids share the same height (H) and width (W).
  - background_color: white (0)
  - content: Sparse non-white pixels on a white background.

objects:
  - type: Pixel
    properties:
      - location: (row, column) coordinates
      - color: Integer value 1-9 (non-white)
  - type: Grid Center
    properties:
      - horizontal_axis: Between rows floor((H-1)/2) and ceil((H-1)/2)
      - vertical_axis: Between columns floor((W-1)/2) and ceil((W-1)/2)

actions:
  - name: Reflect Pixel
    input: A non-white pixel at (r, c) with color C
    operations:
      - Horizontal Reflection: Calculate target coordinates (r, W - 1 - c).
      - Vertical Reflection: Calculate target coordinates (H - 1 - r, c).
      - Diagonal Reflection: Calculate target coordinates (H - 1 - r, W - 1 - c).
    output: Three potential new pixel locations (or fewer if reflections overlap or map onto the original pixel).
  - name: Update Grid
    input: Input grid, reflection coordinates, color C
    operations:
      - Copy input grid to output grid.
      - For each non-white pixel in the input grid:
        - Determine its color C and location (r, c).
        - Calculate the three reflection coordinates: (r, W-1-c), (H-1-r, c), (H-1-r, W-1-c).
        - Set the color of the pixels at these calculated coordinates in the output grid to C.
    output: The final output grid with original pixels and their reflections.

relationships:
  - Symmetry: The output grid exhibits four-way symmetry (horizontal, vertical, rotational) around the grid's center. Each non-white pixel in the input generates a pattern of up to four identical pixels (including the original) in the output, placed symmetrically with respect to the center.
```


**Natural Language Program**

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Determine the height (H) and width (W) of the grid.
3.  Iterate through every cell (pixel) of the input grid, identifying its row `r`, column `c`, and color `C`.
4.  If the color `C` is not white (i.e., `C > 0`):
    a.  Calculate the horizontally reflected column index: `c_h = W - 1 - c`. Set the color of the pixel at `(r, c_h)` in the output grid to `C`.
    b.  Calculate the vertically reflected row index: `r_v = H - 1 - r`. Set the color of the pixel at `(r_v, c)` in the output grid to `C`.
    c.  Calculate the diagonally reflected position using the indices from steps 4a and 4b: `(r_v, c_h)`. Set the color of the pixel at `(r_v, c_h)` in the output grid to `C`.
5.  After iterating through all input pixels, return the completed output grid.