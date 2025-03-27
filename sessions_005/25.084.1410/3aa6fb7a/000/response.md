## Perception

The input and output grids are the same size. The primary color in the input is 'azure' (8) against a 'white' (0) background. The output grid retains all the 'azure' pixels from the input but changes some 'white' pixels to 'blue' (1).

Observing the locations where 'white' changes to 'blue', they appear consistently in relation to specific patterns of 'azure' pixels. Specifically, the change occurs at a 'white' pixel that forms the missing corner of a 2x2 square where the other three pixels are 'azure'. This configuration corresponds to the 'inner corner' of a 3-pixel L-shape formed by the 'azure' pixels.

## Facts


```yaml
task_elements:
  - element: grid
    properties:
      - background_color: white (0)
      - foreground_color: azure (8)
      - transformation_color: blue (1)
  - element: object
    type: L-shape
    definition: Three azure (8) pixels within a 2x2 area, where one pixel is adjacent to the other two, and those two are not adjacent to each other.
    examples:
      - coordinates: [(r, c), (r+1, c), (r, c+1)]
      - coordinates: [(r, c), (r+1, c), (r+1, c+1)]
      - coordinates: [(r, c), (r, c+1), (r+1, c+1)]
      - coordinates: [(r+1, c), (r, c+1), (r+1, c+1)]
  - element: target_pixel
    properties:
      - color: white (0)
      - location: The single white pixel within a 2x2 area that otherwise contains three azure (8) pixels (forming an L-shape). It occupies the 'inner corner' of the L-shape.
  - element: transformation
    action: Change color
    input_pixel: white (0) target_pixel
    output_pixel: blue (1)
    condition: The pixel must be the white pixel completing a 2x2 square with three azure pixels.
    scope: Applies to all such target pixels identified in the input grid.
    preservation: All other pixels (azure pixels and white pixels not meeting the condition) retain their original color and position.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through all possible 2x2 subgrids within the input grid. For each 2x2 subgrid starting at position (row `r`, column `c`), examine the four pixels: `(r, c)`, `(r+1, c)`, `(r, c+1)`, and `(r+1, c+1)`.
3.  Count the number of 'azure' (8) pixels and 'white' (0) pixels within the 2x2 subgrid.
4.  If the count is exactly three 'azure' pixels and one 'white' pixel:
    a.  Identify the coordinates `(tr, tc)` of the single 'white' pixel within that 2x2 subgrid.
    b.  In the output grid, change the color of the pixel at coordinates `(tr, tc)` to 'blue' (1).
5.  Return the modified output grid.