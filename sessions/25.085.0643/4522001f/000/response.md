**Perception**

1.  **Grid Size Transformation:** The output grid dimensions are consistently 3 times the input grid dimensions in both height and width. For example, a 3x3 input grid results in a 9x9 output grid.
2.  **Pixel Mapping:** Each pixel in the input grid corresponds to a 3x3 block of pixels in the output grid. The top-left corner of the 3x3 output block corresponding to the input pixel at `(row, col)` is located at `(row * 3, col * 3)` in the output grid.
3.  **Color Transformation Rules:**
    *   If an input pixel is white (0), the corresponding 3x3 block in the output grid is filled entirely with white (0).
    *   If an input pixel is green (3), the corresponding 3x3 block in the output grid is filled entirely with green (3).
    *   If an input pixel is red (2), the corresponding 3x3 block in the output grid is filled entirely with green (3).
4.  **Color Palette:** The input grids contain white (0), red (2), and green (3). The output grids contain only white (0) and green (3). The red color is effectively replaced by green during the transformation.

**Facts**


```yaml
task_type: scaling_and_color_replacement
grid_relationship:
  input_size: H x W
  output_size: (H * 3) x (W * 3)
  scaling_factor: 3
pixel_mapping:
  type: block_expansion
  input_pixel_location: (r, c)
  output_block_top_left: (r * 3, c * 3)
  output_block_size: 3x3
color_transformation:
  - input_color: white (0)
    output_block_color: white (0)
  - input_color: green (3)
    output_block_color: green (3)
  - input_color: red (2)
    output_block_color: green (3) # Red pixels are replaced by green blocks
involved_colors:
  input: [white (0), red (2), green (3)]
  output: [white (0), green (3)]
```


**Natural Language Program**

1.  Determine the height (H) and width (W) of the input grid.
2.  Create a new output grid with dimensions (H * 3) rows and (W * 3) columns, initially filled with a default color (e.g., white).
3.  Iterate through each pixel of the input grid at location `(row, col)` from `row = 0` to `H-1` and `col = 0` to `W-1`.
4.  For each input pixel:
    a.  Identify its color.
    b.  Determine the target color for the corresponding output block:
        *   If the input color is white (0), the target color is white (0).
        *   If the input color is green (3), the target color is green (3).
        *   If the input color is red (2), the target color is green (3).
    c.  Identify the 3x3 block in the output grid corresponding to the input pixel. This block spans rows `row * 3` to `row * 3 + 2` and columns `col * 3` to `col * 3 + 2`.
    d.  Fill this 3x3 output block entirely with the determined target color.
5.  Return the completed output grid.