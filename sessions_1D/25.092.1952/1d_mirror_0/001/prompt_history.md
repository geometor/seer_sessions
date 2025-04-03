
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 3 3 3 3 3 3 3 3 0 0
```


## train_2

**input:**
```
0 0 6 6 6 6 6 6 6 6 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 5 5 5 5 5 5 5 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0
```

**Perception of the Elements:**

The task operates on single-row grids (1D arrays). Each input grid contains exactly two distinct non-white elements:
1.  A contiguous block of pixels of a single color (e.g., green, magenta, gray).
2.  A single maroon pixel (color 9).
These two elements are separated by one or more white pixels (color 0). The rest of the grid is filled with white pixels.

The transformation rearranges the order of the maroon pixel and the colored block. In the input, the colored block always appears before the maroon pixel. In the output, the maroon pixel appears first, followed by the gap, and then the colored block. The size of the gap between the two elements is preserved. The starting position of the maroon pixel in the output grid is the same as its starting position in the input grid.

**Facts:**


```yaml
task_type: object_rearrangement
grid_dimensionality: 1D (single row)

input_elements:
  - object: colored_block
    description: A contiguous sequence of pixels of the same color, not white (0) and not maroon (9).
    properties:
      - color: The color of the pixels in the block (e.g., 3, 6, 5).
      - length: The number of pixels in the block.
      - start_index: The column index where the block begins.
      - end_index: The column index where the block ends.
  - object: marker_pixel
    description: A single pixel with the color maroon (9).
    properties:
      - color: 9 (maroon)
      - length: 1
      - index: The column index of the pixel.
  - object: gap
    description: A contiguous sequence of one or more white pixels (0) located between the colored_block and the marker_pixel.
    properties:
      - color: 0 (white)
      - length: The number of white pixels in the gap.
      - start_index: The column index where the gap begins (end_index of colored_block + 1).
      - end_index: The column index where the gap ends (index of marker_pixel - 1).

relationship:
  - type: spatial_order (input)
    description: The colored_block appears first, followed by the gap, followed by the marker_pixel along the row.
  - type: spatial_order (output)
    description: The marker_pixel appears first, followed by the gap, followed by the colored_block along the row.

transformation:
  action: rearrange_elements
  details:
    - The relative order of the colored_block and marker_pixel is reversed.
    - The gap between them is preserved in size and placed between the rearranged elements.
    - The starting position of the marker_pixel in the output is identical to its starting position in the input.
    - The overall size of the grid remains unchanged.
    - Pixels outside the rearranged {marker_pixel, gap, colored_block} structure are white (0).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid filled entirely with the background color (white, 0).
2.  Scan the input grid to locate the contiguous block of non-white, non-maroon pixels (the "colored block"). Record its color, starting index, and length.
3.  Scan the input grid to locate the single maroon pixel (color 9, the "marker pixel"). Record its index.
4.  Determine the gap size: calculate the number of white pixels between the end of the colored block and the start of the marker pixel. (Gap size = marker pixel index - colored block end index - 1).
5.  In the output grid, place the marker pixel (color 9) at its original index found in step 3.
6.  Place a sequence of white pixels (0) representing the gap, with the length determined in step 4, immediately following the marker pixel in the output grid.
7.  Place the colored block (using the color and length recorded in step 2) immediately following the gap in the output grid.
