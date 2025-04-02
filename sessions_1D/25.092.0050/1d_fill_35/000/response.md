**Perception:**

The input and output are always single-row grids (effectively 1D arrays).
The input grid contains mostly white pixels (0) and a few non-white pixels. In the provided examples, there are exactly two non-white pixels in each input.
The output grid is formed by filling the segment between the first and last non-white pixels (inclusive) with the color of the *first* non-white pixel found in the input.
The pixels outside this filled segment (before the first non-white pixel and after the last non-white pixel) remain white (0).
The color used for filling is always the color of the leftmost non-white pixel in the input.

**Facts YAML:**


```yaml
task_description: Fill the segment between the first and last non-white pixels in a 1D grid with the color of the first non-white pixel.
grid_properties:
  dimensionality: 1D (represented as a 1xN grid)
  background_color: 0 (white)
objects:
  - type: non-white_pixel
    properties:
      - color: Any color other than 0 (white)
      - position: Column index
relationships:
  - type: segment
    definition: The range of columns starting from the index of the leftmost non-white pixel and ending at the index of the rightmost non-white pixel.
    properties:
      - start_index: Index of the leftmost non-white pixel.
      - end_index: Index of the rightmost non-white pixel.
      - fill_color: The color of the pixel at the start_index in the input.
actions:
  - action: find_boundary_pixels
    inputs:
      - input_grid
    outputs:
      - leftmost_non_white_pixel_index
      - rightmost_non_white_pixel_index
      - fill_color (color of the leftmost non-white pixel)
  - action: fill_segment
    inputs:
      - input_grid_dimensions
      - leftmost_non_white_pixel_index
      - rightmost_non_white_pixel_index
      - fill_color
    outputs:
      - output_grid
    description: Create an output grid of the same dimensions as the input, initially filled with white (0). Then, set the color of pixels from the leftmost index to the rightmost index (inclusive) to the fill_color.
```


**Natural Language Program:**

1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
2.  Scan the input grid from left to right to find the column index of the first (leftmost) non-white pixel. Record its color and index.
3.  Scan the input grid from right to left to find the column index of the last (rightmost) non-white pixel. Record its index.
4.  If no non-white pixels are found, the output grid remains entirely white.
5.  If non-white pixels are found, iterate through the columns of the output grid starting from the leftmost non-white pixel's index up to and including the rightmost non-white pixel's index.
6.  Set the color of each pixel within this range in the output grid to the color recorded from the leftmost non-white pixel in step 2.
7.  Return the modified output grid.