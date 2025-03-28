Okay, let's analyze the provided examples.

**Perception**

1.  **Grid Structure:** The input grids are consistently 10x10, while the output grids are 5x5.
2.  **Quadrants:** The 10x10 input grid can be naturally divided into four 5x5 quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR).
3.  **Color Distribution:** Each quadrant in the input seems associated with a primary non-white color, though it also contains white (0) pixels:
    *   TL: Primarily yellow (4)
    *   TR: Primarily green (3)
    *   BL: Primarily maroon (9)
    *   BR: Primarily azure (8)
4.  **Transformation:** The output 5x5 grid appears to be a composite of the four input quadrants. For each pixel position `(r, c)` in the output grid, the color seems to be determined by looking at the corresponding position `(r, c)` within each of the four input quadrants, following a specific priority order.
5.  **Priority Rule:** By comparing input quadrants with the output grid across examples, a consistent pattern emerges. For a given output coordinate `(r, c)` (where `0 <= r < 5`, `0 <= c < 5`):
    *   Check the input grid at `(r + 5, c)` (BL quadrant). If the color is not white (0), use this color for the output pixel `(r, c)`.
    *   If the BL pixel is white, check the input grid at `(r + 5, c + 5)` (BR quadrant). If the color is not white (0), use this color for the output pixel `(r, c)`.
    *   If the BR pixel is white, check the input grid at `(r, c)` (TL quadrant). If the color is not white (0), use this color for the output pixel `(r, c)`.
    *   If the TL pixel is white, check the input grid at `(r, c + 5)` (TR quadrant). If the color is not white (0), use this color for the output pixel `(r, c)`.
    *   If all four corresponding pixels in the input quadrants are white (0), the output pixel `(r, c)` is also white (0).
    *   This implies a priority order for non-white colors: BL > BR > TL > TR.

**Facts**


```yaml
input_grid:
  type: Grid
  properties:
    height: 10
    width: 10
    pixels: Values from 0-9 representing colors.
  structure: Composed of four 5x5 quadrants.
    quadrants:
      - name: Top-Left (TL)
        coordinates: rows 0-4, cols 0-4
      - name: Top-Right (TR)
        coordinates: rows 0-4, cols 5-9
      - name: Bottom-Left (BL)
        coordinates: rows 5-9, cols 0-4
      - name: Bottom-Right (BR)
        coordinates: rows 5-9, cols 5-9

output_grid:
  type: Grid
  properties:
    height: 5
    width: 5
    pixels: Values from 0-9 representing colors.

transformation:
  type: Pixel-wise Composition
  description: >
    Each pixel in the output grid is determined by the color of the
    corresponding pixel in the input grid's quadrants, checked in a
    specific priority order.
  priority_order: [BL, BR, TL, TR]
  rule: >
    For each output coordinate (r, c):
    1. Get color from input at (r + 5, c) [BL]. If non-white, use it.
    2. Else, get color from input at (r + 5, c + 5) [BR]. If non-white, use it.
    3. Else, get color from input at (r, c) [TL]. If non-white, use it.
    4. Else, get color from input at (r, c + 5) [TR]. Use it (even if white).
    5. If all checked pixels were white, the output is white (0).

colors:
  - white: 0
  - yellow: 4 (primarily in TL)
  - green: 3 (primarily in TR)
  - maroon: 9 (primarily in BL)
  - azure: 8 (primarily in BR)
```


**Natural Language Program**

1.  Initialize an empty 5x5 output grid, filled with white (0).
2.  Iterate through each row `r` from 0 to 4 and each column `c` from 0 to 4 of the target output grid.
3.  For the current output coordinate `(r, c)`, determine the corresponding coordinates in the four quadrants of the 10x10 input grid:
    *   Bottom-Left (BL): `(r + 5, c)`
    *   Bottom-Right (BR): `(r + 5, c + 5)`
    *   Top-Left (TL): `(r, c)`
    *   Top-Right (TR): `(r, c + 5)`
4.  Check the color of the pixel at the BL coordinate in the input grid. If this color is not white (0), set the output grid pixel at `(r, c)` to this color and proceed to the next output coordinate `(r, c+1)` or `(r+1, 0)`.
5.  If the BL pixel color is white (0), check the color of the pixel at the BR coordinate in the input grid. If this color is not white (0), set the output grid pixel at `(r, c)` to this color and proceed to the next output coordinate.
6.  If the BR pixel color is also white (0), check the color of the pixel at the TL coordinate in the input grid. If this color is not white (0), set the output grid pixel at `(r, c)` to this color and proceed to the next output coordinate.
7.  If the TL pixel color is also white (0), check the color of the pixel at the TR coordinate in the input grid. Set the output grid pixel at `(r, c)` to this color (regardless of whether it is white or not).
8.  After iterating through all `(r, c)` coordinates, the resulting 5x5 grid is the final output.