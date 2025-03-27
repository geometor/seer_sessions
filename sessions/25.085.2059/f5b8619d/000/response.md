## Perception

1.  **Grid Size Change:** The output grid is always larger than the input grid. Observing the dimensions, the output grid appears to be exactly twice the height and twice the width of the input grid.
2.  **Tiling:** The pattern within the output grid repeats. Specifically, the output grid looks like a 2x2 tiling of a transformed version of the input grid. Let's call the transformed version the "unit pattern".
3.  **Unit Pattern Generation:** To understand the transformation, we can compare the input grid with the top-left quadrant of the output grid (which represents the unit pattern).
    *   **Non-white Pixels:** Any non-white pixel (gray `5` in train_1, red `2` in train_2, yellow `4` in train_3) in the input grid appears in the same position within the unit pattern in the output.
    *   **White Pixels (Background):** White pixels (`0`) in the input grid are treated differently. If a white pixel in the input grid is adjacent (horizontally, vertically, or diagonally) to *any* non-white pixel, it becomes an azure pixel (`8`) in the corresponding position in the unit pattern.
    *   **Other White Pixels:** White pixels in the input grid that are *not* adjacent to any non-white pixel remain white (`0`) in the unit pattern.
4.  **Final Output Construction:** The unit pattern, derived as described above, is then tiled 2x2 to create the final output grid.

## Facts


```yaml
elements:
  - item: input_grid
    description: A 2D grid of pixels with colors represented by integers 0-9. Contains white (0) background pixels and one or more non-white colored pixels.
  - item: output_grid
    description: A 2D grid of pixels, always 2 times the height and 2 times the width of the input_grid.
  - item: non_white_pixel
    description: Any pixel in the input_grid with a value other than 0. These pixels define the "objects" or "shapes".
  - item: white_pixel
    description: A pixel in the input_grid with the value 0. Represents the background.
  - item: azure_pixel
    description: A pixel with the value 8. Used in the output grid.
  - item: unit_pattern
    description: An intermediate grid with the same dimensions as the input_grid. It forms the basis for the final output.
  - item: adjacency
    description: The relationship between a pixel and its 8 neighbours (horizontal, vertical, and diagonal).

transformation:
  - step: 1
    action: Identify non_white_pixels in the input_grid.
  - step: 2
    action: Create the unit_pattern grid, initially identical to the input_grid.
  - step: 3
    action: Iterate through each white_pixel in the input_grid.
  - step: 4
    condition: If a white_pixel is adjacent (including diagonals) to any non_white_pixel in the input_grid.
    result: Change the corresponding pixel in the unit_pattern to azure_pixel (8).
  - step: 5
    action: Construct the output_grid by tiling the unit_pattern 2x2.

relationships:
  - output_grid dimensions are 2x width and 2x height of input_grid dimensions.
  - output_grid is composed of four identical copies (tiling) of the unit_pattern.
  - unit_pattern dimensions are identical to input_grid dimensions.
  - Pixels in the unit_pattern retain the color of corresponding non_white_pixels from the input_grid.
  - White_pixels in the input_grid may become azure_pixels (8) or remain white_pixels (0) in the unit_pattern based on adjacency to non_white_pixels.
```


## Natural Language Program

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Create a new intermediate grid, the "unit pattern", with the same dimensions `H` x `W`.
3.  Iterate through each pixel at position (`row`, `col`) in the input grid:
    a.  Get the color `C` of the input pixel at (`row`, `col`).
    b.  If `C` is not white (0):
        i.  Set the pixel at (`row`, `col`) in the unit pattern grid to color `C`.
    c.  If `C` is white (0):
        i.  Check all 8 neighbours (including diagonals) of the pixel at (`row`, `col`) in the *input* grid.
        ii. If any neighbour has a non-white color (not 0), set the pixel at (`row`, `col`) in the unit pattern grid to azure (8).
        iii. Otherwise (if all neighbours are white or out of bounds), set the pixel at (`row`, `col`) in the unit pattern grid to white (0).
4.  Create the final output grid with dimensions `2*H` x `2*W`.
5.  Copy the generated unit pattern grid into the four quadrants of the output grid:
    *   Top-left quadrant: `output[0:H, 0:W]` = `unit_pattern`
    *   Top-right quadrant: `output[0:H, W:2*W]` = `unit_pattern`
    *   Bottom-left quadrant: `output[H:2*H, 0:W]` = `unit_pattern`
    *   Bottom-right quadrant: `output[H:2*H, W:2*W]` = `unit_pattern`
6.  Return the final output grid.