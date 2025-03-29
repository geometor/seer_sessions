**Perception**

1.  **Grid Structure:** Each input and output grid is 10x10. They consistently feature a border of grey pixels (5). The interior contains a mix of grey (5) and white (0) pixels.
2.  **Color Transformation:** The core transformation involves changing *some* white pixels (0) in the input to azure pixels (8) in the output. Grey pixels (5) remain unchanged.
3.  **Pattern of Change:** The pixels that change from white (0) to azure (8) always lie along a specific diagonal line within the grid (excluding the border).
4.  **Diagonal Determination:** The specific diagonal path chosen depends on the configuration of pixels in the input grid, specifically the colors of the inner corner pixels or the location of the top-leftmost white pixel.
    *   If the inner top-left corner (1,1) is white, the main diagonal (top-left to bottom-right, `r=c`) is used.
    *   If the inner top-left is grey but the inner top-right corner (1,8 for a 10x10 grid) is white, the anti-diagonal (top-right to bottom-left, `r+c = constant`) is used.
    *   If both inner top corners are grey, the diagonal starts at the overall top-most, left-most white pixel and proceeds downwards and to the right (`c = r + constant`).
5.  **Transformation Rule:** The transformation rule iterates through the cells along the determined diagonal. If a cell on this diagonal contains a white pixel (0) in the input, it is changed to an azure pixel (8) in the output. All other pixels retain their original color from the input.

**YAML Facts**


```yaml
---
task_description: Change specific white pixels to azure along a determined diagonal path within a grey-bordered grid.

grid_properties:
  - dimensions: 10x10 (consistent across examples)
  - border: 1-pixel wide border of grey (5)
  - background_color: grey (5)
  - object_color: white (0)
  - transformed_color: azure (8)

objects:
  - id: grid
    description: The 2D array of pixels.
  - id: border
    description: The outer frame of grey pixels.
    properties:
      color: 5
      thickness: 1
  - id: inner_grid
    description: The grid excluding the border.
    properties:
      - top_left_corner: cell at (1, 1)
      - top_right_corner: cell at (1, width-2)
  - id: pixels
    description: Individual cells within the grid.
    properties:
      - color: 0-9 (specifically 0, 5, 8 observed in this task)
      - location: (row, column)

relationships:
  - type: diagonal_path
    description: A line of cells where row and column indices follow a linear relationship (r=c, r+c=k, or c=r+k).
    determination_rule:
      - condition: Input inner top-left corner (1,1) is white (0).
        path: Main diagonal (r=c).
      - condition: Input inner top-left corner (1,1) is not white (0) AND inner top-right corner (1, W-2) is white (0).
        path: Anti-diagonal (r+c = W-1).
      - condition: Both input inner top corners (1,1) and (1, W-2) are not white (0).
        path: Down-right diagonal starting from the top-most, left-most white pixel (r_min, c_min) in the input grid (c = r + c_min - r_min).

actions:
  - name: determine_diagonal
    input: input_grid
    output: specific_diagonal_path
    logic: Apply the determination_rule based on inner corner colors or the first white pixel.
  - name: transform_pixels
    input: input_grid, specific_diagonal_path
    output: output_grid
    logic: Iterate through cells (r, c) on the specific_diagonal_path. If input_grid[r][c] is white (0), set output_grid[r][c] to azure (8). Otherwise, copy input_grid[r][c] to output_grid[r][c].

constants:
  - white: 0
  - grey: 5
  - azure: 8

```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Get the dimensions of the input grid (Height H, Width W).
3.  Check the color of the pixel at the inner top-left corner: `input_grid[1][1]`.
4.  **If** `input_grid[1][1]` is white (0):
    *   Define the diagonal path by the rule `row == column`.
    *   Iterate through rows `r` from 1 to H-2 and columns `c` from 1 to W-2.
    *   If `r == c` and `input_grid[r][c]` is white (0), set `output_grid[r][c]` to azure (8).
5.  **Else if** the color of the pixel at the inner top-right corner `input_grid[1][W-2]` is white (0):
    *   Define the diagonal path by the rule `row + column == W - 1`.
    *   Iterate through rows `r` from 1 to H-2 and columns `c` from 1 to W-2.
    *   If `r + c == W - 1` and `input_grid[r][c]` is white (0), set `output_grid[r][c]` to azure (8).
6.  **Else** (neither inner top corner is white):
    *   Find the coordinates (`r_min`, `c_min`) of the top-most, then left-most white pixel (0) within the inner grid (rows 1 to H-2, columns 1 to W-2).
    *   Calculate the diagonal constant `k = c_min - r_min`.
    *   Define the diagonal path by the rule `column == row + k`.
    *   Iterate through rows `r` from 1 to H-2 and columns `c` from 1 to W-2.
    *   If `c == r + k` and `input_grid[r][c]` is white (0), set `output_grid[r][c]` to azure (8).
7.  Return the modified output grid.