## Perception

The task operates on 1-dimensional grids (or single rows). Each input grid contains a single contiguous block of a non-white color against a white (color 0) background. The output grid preserves the non-white colored block (same color, same length) but shifts its position horizontally within the grid. The rest of the output grid is filled with the white background color. By comparing the starting position of the colored block in the input and output across all examples, it consistently shifts 2 positions to the right.

## Facts


```yaml
task_type: object_transformation
grid_dimensionality: 1D (single row)
background_color: 0 (white)
objects:
  - type: contiguous_block
    count: 1
    properties:
      color: non-white (variable, e.g., magenta(6), red(2))
      length: variable
      shape: horizontal_line
object_attributes_invariant:
  - color
  - length
transformation:
  type: translation
  direction: horizontal_right
  magnitude: 2 positions
input_output_relation:
  - The single non-white block identified in the input grid is moved 2 cells to the right to produce the output grid.
  - All cells in the output grid not occupied by the shifted block are set to the background color (white).
```


## Natural Language Program

1.  Identify the single contiguous block of non-white pixels in the input grid. Note its color, length, and starting index.
2.  Calculate the new starting index for the block by adding 2 to the original starting index.
3.  Create a new output grid of the same dimensions as the input grid, initially filled with the background color (white, 0).
4.  Place the identified block (with its original color and length) into the output grid starting at the calculated new starting index. Ensure the placement respects the grid boundaries; if the shift causes the block to extend beyond the right edge, only the part fitting within the grid is placed (although this edge case isn't explicitly shown in the examples, it's implied by standard grid operations).