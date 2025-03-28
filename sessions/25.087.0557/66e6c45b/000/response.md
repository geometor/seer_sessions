**Perception**

The input grid contains a 2x2 block of four distinct non-white pixels, centered within a larger grid filled with white pixels. The output grid has the same dimensions as the input grid but is entirely white except for the four corners. Each of the four non-white pixels from the input's central 2x2 block is moved to one of the four corners in the output grid. The relative positions are preserved: the top-left pixel of the input block moves to the top-left corner, the top-right pixel moves to the top-right corner, the bottom-left pixel moves to the bottom-left corner, and the bottom-right pixel moves to the bottom-right corner.

**Facts**


```yaml
- task_type: transformation
- grid_properties:
    - input_size: 4x4
    - output_size: 4x4
    - background_color: white (0)
- objects:
    - type: pixel_block
      description: A 2x2 block of four non-white pixels in the input grid.
      location: Centered within the input grid.
      pixels:
        - relative_position: top-left
        - relative_position: top-right
        - relative_position: bottom-left
        - relative_position: bottom-right
    - type: corner_pixels
      description: Four individual pixels located at the corners of the output grid.
      colors: Derived from the pixels in the input 2x2 block.
      location:
        - (0, 0) # top-left corner
        - (0, width-1) # top-right corner
        - (height-1, 0) # bottom-left corner
        - (height-1, width-1) # bottom-right corner
- relationships:
    - mapping: The pixel at the top-left of the input 2x2 block maps to the top-left corner (0, 0) of the output grid.
    - mapping: The pixel at the top-right of the input 2x2 block maps to the top-right corner (0, width-1) of the output grid.
    - mapping: The pixel at the bottom-left of the input 2x2 block maps to the bottom-left corner (height-1, 0) of the output grid.
    - mapping: The pixel at the bottom-right of the input 2x2 block maps to the bottom-right corner (height-1, width-1) of the output grid.
- actions:
    - identify: Locate the 2x2 block of non-white pixels in the input grid.
    - extract: Determine the colors and relative positions of the four pixels within this block.
    - create: Generate a new grid of the same dimensions as the input, filled with the background color (white).
    - place: Move the extracted pixels to the corresponding corners of the new grid based on their relative position in the original 2x2 block.
```


**Natural Language Program**

1.  Identify the background color (typically white, 0).
2.  Find the contiguous 2x2 block of pixels that are not the background color within the input grid.
3.  Determine the colors of the four pixels within this 2x2 block:
    *   Top-left pixel color.
    *   Top-right pixel color.
    *   Bottom-left pixel color.
    *   Bottom-right pixel color.
4.  Determine the dimensions (height H, width W) of the input grid.
5.  Create a new output grid of the same dimensions (H x W) and fill it entirely with the background color.
6.  Place the identified top-left pixel color at the top-left corner (row 0, column 0) of the output grid.
7.  Place the identified top-right pixel color at the top-right corner (row 0, column W-1) of the output grid.
8.  Place the identified bottom-left pixel color at the bottom-left corner (row H-1, column 0) of the output grid.
9.  Place the identified bottom-right pixel color at the bottom-right corner (row H-1, column W-1) of the output grid.
10. Return the modified output grid.