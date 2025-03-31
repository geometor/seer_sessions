
## train_1

**input:**
```
2 0
0 0
```


**output:**
```
2 2 0 0
2 2 0 0
0 0 1 0
0 0 0 1
```


## train_2

**input:**
```
0 0 0 5 0
0 5 0 0 0
0 0 0 0 0
0 5 0 0 0
0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 5 5 0 0
0 1 0 0 0 0 5 5 0 0
0 0 5 5 0 0 0 0 1 0
0 0 5 5 0 0 0 0 0 1
1 0 0 0 1 0 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 0 5 5 0 0 1 0 0 0
0 0 5 5 0 0 0 1 0 0
0 0 0 0 1 0 0 0 1 0
0 0 0 0 0 1 0 0 0 1
```


## train_3

**input:**
```
0 0 0 0 0 3
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3
1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0
```

Okay, let's break down the task based on the examples provided.

## Perception

1.  **Grid Size Transformation:** The output grid is always exactly twice the height and twice the width of the input grid. For an input of HxW, the output is (2H)x(2W).
2.  **Pixel Mapping:** Each pixel in the input grid corresponds to a 2x2 block of pixels in the output grid. An input pixel at `(row, col)` maps to the output block covering `(2*row, 2*col)` to `(2*row + 1, 2*col + 1)`.
3.  **Color Transformation Rule:** The way an input pixel's color determines the content of its corresponding 2x2 output block depends on whether the input pixel is white (0) or non-white (1-9).
    *   **Non-white Input Pixels:** If an input pixel has a non-white color `C`, the corresponding 2x2 block in the output is filled entirely with that color `C`.
    *   **White Input Pixels (0):** If an input pixel is white (0), the corresponding 2x2 block in the output follows a specific pattern: the top-left and bottom-right pixels are blue (1), and the top-right and bottom-left pixels are white (0). This pattern looks like `[[1, 0], [0, 1]]`.
4.  **Color Introduction:** The color blue (1) is introduced into the output grid specifically as part of the transformation rule for white input pixels. Other non-white colors present in the input are preserved in their corresponding output blocks.

## YAML Facts


```yaml
task_context:
  grid_relationship: Output grid dimensions are 2x the input grid dimensions (height and width).
  mapping: Each input pixel at (r, c) maps to a 2x2 block in the output grid starting at (2*r, 2*c).
objects:
  - type: input_pixel
    properties:
      - location: (row, column)
      - color: integer (0-9)
  - type: output_block
    properties:
      - location: (start_row, start_col) spanning 2x2 area
      - pattern: 2x2 grid of colors
transformation:
  type: conditional_pixel_expansion
  conditions:
    - if: input_pixel.color == 0 (white)
      then:
        output_block.pattern: [[1, 0], [0, 1]]  # blue diagonal, white off-diagonal
        output_block.colors_used: [blue(1), white(0)]
    - if: input_pixel.color != 0 (non-white)
      then:
        output_block.pattern: [[C, C], [C, C]] where C is input_pixel.color
        output_block.colors_used: [C] # Only the original non-white color
relationships:
  - Each input_pixel uniquely determines one output_block.
  - The color of the input_pixel dictates the pattern and colors within the corresponding output_block.
```


## Natural Language Program

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Create a new output grid with dimensions (`2*H`, `2*W`).
3.  Iterate through each pixel of the input grid, using its row index `r` (from 0 to `H-1`) and column index `c` (from 0 to `W-1`).
4.  For each input pixel at `(r, c)`:
    a.  Get the color `input_color` of the pixel.
    b.  Calculate the top-left coordinates of the corresponding 2x2 block in the output grid: `output_r = 2*r`, `output_c = 2*c`.
    c.  **Check the `input_color`:**
        i.  **If `input_color` is white (0):**
            *   Set the output pixel at `(output_r, output_c)` to blue (1).
            *   Set the output pixel at `(output_r, output_c + 1)` to white (0).
            *   Set the output pixel at `(output_r + 1, output_c)` to white (0).
            *   Set the output pixel at `(output_r + 1, output_c + 1)` to blue (1).
        ii. **If `input_color` is non-white (1-9):**
            *   Set the output pixel at `(output_r, output_c)` to `input_color`.
            *   Set the output pixel at `(output_r, output_c + 1)` to `input_color`.
            *   Set the output pixel at `(output_r + 1, output_c)` to `input_color`.
            *   Set the output pixel at `(output_r + 1, output_c + 1)` to `input_color`.
5.  Return the completed output grid.
