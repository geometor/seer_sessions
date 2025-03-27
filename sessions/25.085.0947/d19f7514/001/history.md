
## train_1

**input:**
```
3 3 0 0
3 0 0 0
0 0 0 3
0 0 3 3
3 0 0 0
3 3 3 3
0 5 0 0
5 5 0 0
5 0 5 0
5 5 5 5
5 5 5 0
5 0 5 0
```


**output:**
```
4 4 0 0
4 4 0 0
4 0 4 4
4 4 4 4
4 4 4 0
4 4 4 4
```


## train_2

**input:**
```
3 3 0 3
3 0 3 3
0 3 0 0
0 0 3 0
3 0 3 0
0 0 0 3
5 0 0 0
0 5 5 5
5 0 0 5
0 5 5 5
5 5 5 0
5 0 0 0
```


**output:**
```
4 4 0 4
4 4 4 4
4 4 0 4
0 4 4 4
4 4 4 0
4 0 0 4
```


## train_3

**input:**
```
3 3 0 0
0 3 3 3
3 3 0 3
0 3 3 0
3 0 3 0
3 0 0 0
0 5 5 5
5 5 5 5
5 5 5 0
5 5 5 5
5 0 0 0
0 5 5 0
```


**output:**
```
4 4 4 4
4 4 4 4
4 4 4 4
4 4 4 4
4 0 4 0
4 4 4 0
```


## train_4

**input:**
```
0 3 3 3
0 3 0 3
0 0 0 0
3 0 3 3
3 0 0 0
0 3 0 3
0 5 0 5
0 0 0 0
0 0 0 0
5 0 5 0
5 0 0 0
5 5 0 5
```


**output:**
```
0 4 4 4
0 4 0 4
0 0 0 0
4 0 4 4
4 0 0 0
4 4 0 4
```

**Perception:**

1.  **Grid Structure:** The input grids consistently have a height that is exactly double the height of the output grids, while the width remains the same.
2.  **Color Mapping:** The input grids primarily contain green (3), gray (5), and white (0) pixels. The output grids contain yellow (4) and white (0) pixels.
3.  **Transformation Logic:** The transformation involves comparing pixels vertically across the two halves of the input grid. The output grid seems to be a result of an operation applied to corresponding pixels in the top and bottom halves of the input grid.
4.  **Rule Identification:** By observing the examples, a pattern emerges: If a pixel in the top half of the input grid is green (3), OR the corresponding pixel in the bottom half (same column, row index + half the input height) is gray (5), then the corresponding pixel in the output grid becomes yellow (4). If neither of these conditions is met, the output pixel is white (0).

**Facts:**


```yaml
task_description: Combine information from the top and bottom halves of the input grid based on specific color rules to generate the output grid.
grid_properties:
  - input_height: 2 * N
  - input_width: M
  - output_height: N
  - output_width: M
color_rules:
  - input_colors: [green (3), gray (5), white (0)]
  - output_colors: [yellow (4), white (0)]
transformation:
  - type: Pixel-wise combination
  - input_halves:
      - top: rows 0 to N-1
      - bottom: rows N to 2N-1
  - rule: For each coordinate (row, col) from 0 to N-1, 0 to M-1:
      - condition_top: input_grid[row][col] == green (3)
      - condition_bottom: input_grid[row + N][col] == gray (5)
      - output_pixel: yellow (4) if condition_top OR condition_bottom else white (0)
```


**Natural Language Program:**

1.  Determine the height (`H_in`) and width (`W`) of the input grid.
2.  Calculate the height of the output grid (`H_out`) as `H_in / 2`. The width of the output grid is the same as the input width (`W`).
3.  Create a new output grid of size `H_out` x `W`, initialized with white (0) pixels.
4.  Iterate through each row `r` from 0 to `H_out - 1` and each column `c` from 0 to `W - 1`.
5.  For the current position `(r, c)`, check the color of the pixel at `(r, c)` in the input grid (top half).
6.  Check the color of the pixel at `(r + H_out, c)` in the input grid (bottom half).
7.  If the pixel in the top half is green (3) OR the pixel in the bottom half is gray (5), set the pixel at `(r, c)` in the output grid to yellow (4).
8.  Otherwise (if neither condition in step 7 is true), the pixel at `(r, c)` in the output grid remains white (0).
9.  Return the generated output grid.
