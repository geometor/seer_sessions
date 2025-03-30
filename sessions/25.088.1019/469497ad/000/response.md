**Perception:**

The core transformation observed across all examples is a scaling operation. The input grid is enlarged to produce the output grid. The scaling factor is consistent within each example but differs between examples (3x for example 1, 2x for example 2, 4x for example 3). It appears the scaling factor can be determined by dividing the output dimension (height or width) by the corresponding input dimension.

Each pixel in the input grid corresponds to a square block of pixels in the output grid, with the size of the block determined by the scaling factor (e.g., a 3x scaling factor means each input pixel maps to a 3x3 output block).

The content of the output block depends on the color of the corresponding input pixel:
1.  **Non-white input pixels:** If an input pixel has a color other than white (0), the corresponding block in the output grid is filled entirely with that same color.
2.  **White input pixels (0):** If an input pixel is white (0), the corresponding block in the output grid is primarily white (0), but with red pixels (2) placed along its main diagonal (from top-left to bottom-right within the block).

**Facts:**


```yaml
task_type: Grid Transformation (Scaling and Pattern Replacement)

observations:
  - transformation: Scaling
    input_property: Grid Dimensions (height H_in, width W_in)
    output_property: Grid Dimensions (height H_out, width W_out)
    relationship: H_out = H_in * S, W_out = W_in * S, where S is an integer scaling factor.
    details: The scaling factor S is constant for a given example pair but varies between examples. S = H_out / H_in = W_out / W_in.
  - element: Pixel
    input_location: (r, c)
    input_value: V
    output_mapping: Maps to an S x S block in the output grid starting at (r * S, c * S).
    conditions:
      - condition: Input pixel value V is not white (V != 0)
        output_block_content: Filled entirely with color V.
      - condition: Input pixel value V is white (V == 0)
        output_block_content:
          background: White (0)
          pattern: Red pixels (2) placed along the main diagonal of the S x S block.
          pattern_details: For a block pixel at local coordinates (br, bc) where 0 <= br < S and 0 <= bc < S, the pixel value is 2 if br == bc, otherwise it is 0.

examples_scaling_factors:
  - example: train_1
    input_dims: 5x5
    output_dims: 15x15
    scaling_factor_S: 3
  - example: train_2
    input_dims: 5x5
    output_dims: 10x10
    scaling_factor_S: 2
  - example: train_3
    input_dims: 5x5
    output_dims: 20x20
    scaling_factor_S: 4

involved_colors:
  - White (0): Background color in input and special output blocks.
  - Red (2): Used for the diagonal pattern in blocks corresponding to white input pixels.
  - Other colors (1, 3, 4, 6, 7, 8, 9): Copied directly when scaling non-white pixels.
```


**Natural Language Program:**

1.  Determine the integer scaling factor `S` by dividing the height of the output grid by the height of the input grid (or width by width, as they should yield the same factor).
2.  Create a new output grid with dimensions `input_height * S` by `input_width * S`.
3.  Iterate through each pixel of the input grid at coordinates `(row_in, col_in)` with value `V`.
4.  For each input pixel `V`:
    a.  Calculate the top-left corner coordinates `(row_out_start, col_out_start)` for the corresponding block in the output grid: `row_out_start = row_in * S`, `col_out_start = col_in * S`.
    b.  If the input pixel value `V` is **not** white (i.e., `V != 0`):
        i.  Fill the `S x S` block in the output grid, starting from `(row_out_start, col_out_start)`, entirely with the color `V`.
    c.  If the input pixel value `V` **is** white (i.e., `V == 0`):
        i.  Fill the `S x S` block in the output grid, starting from `(row_out_start, col_out_start)`, initially with white (0).
        ii. Iterate through the local coordinates `(i, j)` within this block, where `0 <= i < S` and `0 <= j < S`.
        iii.If the local row index `i` equals the local column index `j` (`i == j`), set the pixel at the absolute output grid coordinates `(row_out_start + i, col_out_start + j)` to red (2).
5.  Return the completed output grid.