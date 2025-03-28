**Perception**

The task involves transforming an input grid into an output grid that is twice the height and twice the width of the input. The transformation rule depends on the color of each pixel in the input grid.

1.  **Scaling:** The output grid dimensions are consistently double the input grid dimensions (2 * height, 2 * width).
2.  **Pixel Mapping:** Each pixel in the input grid corresponds to a 2x2 area in the output grid. An input pixel at position (row `r`, column `c`) maps to the output area covering rows `2*r` to `2*r + 1` and columns `2*c` to `2*c + 1`.
3.  **Color Transformation:**
    *   If an input pixel is non-white (color value > 0), the corresponding 2x2 area in the output grid is filled entirely with that same color.
    *   If an input pixel is white (color value 0), the corresponding 2x2 area in the output grid is filled with a specific pattern:
        
```
        blue white
        white blue
        ```

        or numerically:
        
```
        1 0
        0 1
        ```


**Facts**


```yaml
task_context:
  grid_relationship: Output grid dimensions are double the input grid dimensions (height and width).
  transformation_type: Pixel-wise replacement with scaling.

input_elements:
  - element: grid
    properties:
      - Contains pixels with color values 0-9.
      - Colors observed: white (0), gray (5), red (2), green (3).
  - element: pixel
    properties:
      - Has a color value.
      - Has a position (row, column).

output_elements:
  - element: grid
    properties:
      - Dimensions: 2 * input_height, 2 * input_width.
  - element: block_2x2
    properties:
      - Occupies a 2x2 area in the output grid.
      - Corresponds to a single pixel in the input grid.
      - Content depends on the corresponding input pixel's color.

transformation_rules:
  - rule: Map each input pixel at (r, c) to the output 2x2 block starting at (2*r, 2*c).
  - condition: If input pixel color is C (where C > 0):
    action: Fill the corresponding output 2x2 block entirely with color C.
  - condition: If input pixel color is 0 (white):
    action: Fill the corresponding output 2x2 block with the pattern [[1, 0], [0, 1]] (blue, white / white, blue).

constants:
  - name: white_replacement_pattern
    value: [[1, 0], [0, 1]]
  - name: scaling_factor
    value: 2
```


**Natural Language Program**

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Create a new output grid with dimensions `2*H` height and `2*W` width, initialized with a default color (e.g., white/0, although the process will overwrite everything).
3.  Iterate through each pixel of the input grid, using its row index `r` (from 0 to `H-1`) and column index `c` (from 0 to `W-1`).
4.  For each input pixel at `(r, c)`:
    a.  Identify its color `C`.
    b.  Determine the top-left coordinates `(out_r, out_c)` for the corresponding 2x2 block in the output grid: `out_r = 2 * r`, `out_c = 2 * c`.
    c.  If the input pixel color `C` is not white (i.e., `C > 0`):
        i.  Fill the 2x2 block in the output grid starting at `(out_r, out_c)` with the color `C`. This means setting the pixels at `(out_r, out_c)`, `(out_r+1, out_c)`, `(out_r, out_c+1)`, and `(out_r+1, out_c+1)` to `C`.
    d.  If the input pixel color `C` is white (i.e., `C == 0`):
        i.  Fill the 2x2 block in the output grid starting at `(out_r, out_c)` with the specific pattern:
            - Set output pixel at `(out_r, out_c)` to blue (1).
            - Set output pixel at `(out_r+1, out_c)` to white (0).
            - Set output pixel at `(out_r, out_c+1)` to white (0).
            - Set output pixel at `(out_r+1, out_c+1)` to blue (1).
5.  Return the completed output grid.