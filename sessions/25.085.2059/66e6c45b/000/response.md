## Perception

The input grid is a 4x4 grid with a white background (color 0). In the center, there is a 2x2 block composed of four distinct non-white pixels. In the first example, these are gray (5), magenta (6), azure (8), and green (3). In the second example, they are green (3), yellow (4), orange (7), and magenta (6).

The output grid is also a 4x4 grid with a white background. The four non-white pixels from the input's central 2x2 block have been moved to the four corners of the output grid. Specifically:
- The pixel that was at the top-left of the 2x2 block in the input moves to the top-left corner (0,0) of the output.
- The pixel that was at the top-right of the 2x2 block in the input moves to the top-right corner (0, width-1) of the output.
- The pixel that was at the bottom-left of the 2x2 block in the input moves to the bottom-left corner (height-1, 0) of the output.
- The pixel that was at the bottom-right of the 2x2 block in the input moves to the bottom-right corner (height-1, width-1) of the output.

All other positions in the output grid are filled with the background color (white, 0). The size of the grid remains unchanged.

## Facts


```yaml
task_context:
  grid_size:
    input_dimensions: [4, 4]
    output_dimensions: [4, 4]
    consistent_size: true
  background_color: 0 # white
objects:
  - object_type: block
    description: A 2x2 block of non-background pixels located centrally in the input grid.
    pixels:
      - identifier: pixel_tl # Top-Left of the 2x2 block
        color: non-zero
        input_location: [1, 1] # Example 1: (1,1) gray(5), Example 2: (1,1) green(3)
        output_location: [0, 0] # Top-Left corner of the output grid
      - identifier: pixel_tr # Top-Right of the 2x2 block
        color: non-zero
        input_location: [1, 2] # Example 1: (1,2) magenta(6), Example 2: (1,2) yellow(4)
        output_location: [0, 3] # Top-Right corner of the output grid
      - identifier: pixel_bl # Bottom-Left of the 2x2 block
        color: non-zero
        input_location: [2, 1] # Example 1: (2,1) azure(8), Example 2: (2,1) orange(7)
        output_location: [3, 0] # Bottom-Left corner of the output grid
      - identifier: pixel_br # Bottom-Right of the 2x2 block
        color: non-zero
        input_location: [2, 2] # Example 1: (2,2) green(3), Example 2: (2,2) magenta(6)
        output_location: [3, 3] # Bottom-Right corner of the output grid
transformation:
  action: move_pixels
  details: Each of the four pixels comprising the central 2x2 block in the input is moved to a specific corner of the output grid.
relationships:
  - type: position_mapping
    description: The relative position within the 2x2 block determines the destination corner in the output grid.
    mapping:
      - input_relative_pos: top-left -> output_absolute_pos: top-left_corner
      - input_relative_pos: top-right -> output_absolute_pos: top-right_corner
      - input_relative_pos: bottom-left -> output_absolute_pos: bottom-left_corner
      - input_relative_pos: bottom-right -> output_absolute_pos: bottom-right_corner
  - type: grid_fill
    description: All pixels in the output grid not assigned a color from the input block are set to the background color.
```


## Natural Language Program

1.  **Initialize Output Grid**: Create a new grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  **Identify Input Pixels**: Locate the four non-background pixels in the input grid. These pixels form a 2x2 block. Let the coordinates of the top-left pixel of this block be (r, c). The four pixels will be at (r, c), (r, c+1), (r+1, c), and (r+1, c+1).
3.  **Map Pixels to Corners**:
    a.  Take the pixel value from input grid location (r, c) and place it at the top-left corner (0, 0) of the output grid.
    b.  Take the pixel value from input grid location (r, c+1) and place it at the top-right corner (0, width-1) of the output grid, where 'width' is the width of the grid.
    c.  Take the pixel value from input grid location (r+1, c) and place it at the bottom-left corner (height-1, 0) of the output grid, where 'height' is the height of the grid.
    d.  Take the pixel value from input grid location (r+1, c+1) and place it at the bottom-right corner (height-1, width-1) of the output grid.
4.  **Return Output**: The resulting grid is the final output.