## Perception
The input and output are single rows of pixels (1D grids).
Each input row contains:
1.  A contiguous block of a single color (e.g., magenta '6' or red '2'). Let's call this the "source color block".
2.  An orange pixel ('7'). Let's call this the "boundary pixel".
3.  White pixels ('0') acting as background, potentially surrounding the source color block and separating it from the boundary pixel.

The transformation involves extending the source color block to the right. The extension fills the white pixels ('0') between the original right edge of the source color block and the boundary pixel ('7') with the source color. The extension stops immediately before the boundary pixel. All other pixels, including those before the source color block, the boundary pixel itself, and any pixels after the boundary pixel, remain unchanged.

## Facts

```yaml
task_type: 1D array transformation
components:
  - type: background
    color: white (0)
    role: empty space, potentially filled
  - type: source_block
    description: A contiguous sequence of pixels of the same color, excluding white (0) and orange (7).
    properties:
      - color: variable (magenta '6' or red '2' in examples)
      - location: identifiable start and end indices
    role: expands to fill space
  - type: boundary_pixel
    color: orange (7)
    role: marks the rightmost limit for the expansion of the source_block
relationships:
  - source_block is always to the left of the boundary_pixel.
  - white (0) pixels may exist between the source_block and the boundary_pixel.
actions:
  - identify: locate the source_block and determine its color and rightmost index.
  - identify: locate the boundary_pixel and determine its index.
  - fill: change the color of all white (0) pixels located between the rightmost index of the source_block and the index of the boundary_pixel to the color of the source_block.
constraints:
  - The source_block color is preserved during filling.
  - The boundary_pixel is never overwritten.
  - Pixels to the left of the source_block and pixels at or after the boundary_pixel remain unchanged.
```


## Natural Language Program
1.  Scan the input row from left to right.
2.  Identify the first pixel that is not white (0) and not orange (7). This marks the start of the source color block. Note its color (let's call it `source_color`) and its index.
3.  Continue scanning to find the end of this contiguous block of `source_color`. Note the index of the last pixel in this block (let's call it `source_end_index`).
4.  Continue scanning from `source_end_index + 1` to find the index of the orange (7) pixel (let's call it `boundary_index`).
5.  Create a copy of the input row to serve as the output row.
6.  Iterate through the indices from `source_end_index + 1` up to (but not including) `boundary_index`.
7.  For each index in this range, change the pixel value in the output row to `source_color`.
8.  Return the modified output row.