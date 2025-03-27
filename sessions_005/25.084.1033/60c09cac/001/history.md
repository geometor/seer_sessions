
## train_1

**input:**
```
0 0 8 0
0 8 5 5
0 0 0 5
0 0 0 0
```


**output:**
```
0 0 0 0 8 8 0 0
0 0 0 0 8 8 0 0
0 0 8 8 5 5 5 5
0 0 8 8 5 5 5 5
0 0 0 0 0 0 5 5
0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 3 0
0 7 7
0 0 0
```


**output:**
```
0 0 3 3 0 0
0 0 3 3 0 0
0 0 7 7 7 7
0 0 7 7 7 7
0 0 0 0 0 0
0 0 0 0 0 0
```

**Perception of Task Elements:**

The task involves a geometric transformation of the input grid. I observe that the output grid is consistently larger than the input grid. Specifically, the output grid's dimensions appear to be double the input grid's dimensions in both height and width. Each individual pixel from the input grid seems to be expanded into a 2x2 block of the same color in the output grid, maintaining its relative position within the scaled-up structure. The colors themselves are preserved during this transformation.

**YAML Facts:**


```yaml
task_type: geometric_transformation
transformation: scaling
scale_factor: 2
input_grid:
  properties:
    - variable_size
    - contains_pixels_of_various_colors
output_grid:
  properties:
    - height: double the input height
    - width: double the input width
    - derived_from_input
mapping:
  type: pixel_to_block
  input_element: each pixel at (row, col) with color C
  output_element: a 2x2 block of pixels in the output grid
  output_location: top-left corner at (2*row, 2*col)
  output_color: all pixels in the 2x2 block have color C
color_preservation: all colors from the input are maintained in the output
background_color: white (0) pixels are scaled just like any other color
```


**Natural Language Program:**

1.  Determine the height (H_in) and width (W_in) of the input grid.
2.  Calculate the dimensions of the output grid: height (H_out) = 2 * H_in, width (W_out) = 2 * W_in.
3.  Create a new output grid of size H_out x W_out.
4.  For each pixel located at `(row, col)` in the input grid (where `0 <= row < H_in` and `0 <= col < W_in`):
    a.  Identify the color `C` of the input pixel at `(row, col)`.
    b.  Determine the corresponding top-left coordinate `(out_row, out_col)` in the output grid, where `out_row = 2 * row` and `out_col = 2 * col`.
    c.  Fill the 2x2 block of pixels in the output grid starting at `(out_row, out_col)` with the color `C`. This involves setting the pixels at `(out_row, out_col)`, `(out_row, out_col + 1)`, `(out_row + 1, out_col)`, and `(out_row + 1, out_col + 1)` to color `C`.
5.  Return the fully constructed output grid.
