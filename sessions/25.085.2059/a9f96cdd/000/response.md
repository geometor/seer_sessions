**Perception**

1.  **Input Grid:** Each input grid contains a single non-white pixel, which is always red (color 2). All other pixels are white (color 0). The position of the red pixel varies across examples.
2.  **Output Grid:** Each output grid has the same dimensions as its corresponding input grid. The original red pixel from the input is replaced with white (color 0). Several new non-white pixels appear in the output grid.
3.  **Transformation:** The transformation involves locating the single red pixel in the input. Four specific colors (green-3, magenta-6, azure-8, orange-7) are placed in the output grid at positions diagonally adjacent to the original red pixel's location.
4.  **Diagonal Placement:**
    *   Green (3) appears at the position diagonally up-left (-1 row, -1 column) relative to the red pixel.
    *   Magenta (6) appears diagonally up-right (-1 row, +1 column).
    *   Azure (8) appears diagonally down-left (+1 row, -1 column).
    *   Orange (7) appears diagonally down-right (+1 row, +1 column).
5.  **Boundary Condition:** A colored pixel is only placed in the output if its calculated diagonal position falls within the bounds of the grid. If a diagonal position is outside the grid (e.g., row index < 0 or column index >= width), no pixel is placed for that direction.
6.  **Consistency:** The colors associated with each diagonal direction are consistent across all examples.

**Facts**


```yaml
task_elements:
  - description: Input grid contains a single non-white pixel.
    properties:
      color: red (2)
      quantity: 1
  - description: Output grid matches input dimensions.
  - description: The original red pixel location becomes white (0) in the output.
  - description: Four potential output pixels are generated based on the input red pixel's location.
    properties:
      - color: green (3)
        location_rule: Relative to input pixel at (r, c), place at (r-1, c-1)
      - color: magenta (6)
        location_rule: Relative to input pixel at (r, c), place at (r-1, c+1)
      - color: azure (8)
        location_rule: Relative to input pixel at (r, c), place at (r+1, c-1)
      - color: orange (7)
        location_rule: Relative to input pixel at (r, c), place at (r+1, c+1)
  - description: Placement constraint for output pixels.
    properties:
      condition: The calculated row and column indices must be within the grid boundaries (0 <= row < height, 0 <= col < width).
      action_if_false: Do not place the pixel.
```


**Natural Language Program**

1.  Create an output grid with the same dimensions as the input grid, initially filled with white (0) pixels.
2.  Find the coordinates (row `r`, column `c`) of the single red (2) pixel in the input grid.
3.  Define the four diagonal target positions and their corresponding colors:
    *   Up-Left: (`r-1`, `c-1`), color green (3)
    *   Up-Right: (`r-1`, `c+1`), color magenta (6)
    *   Down-Left: (`r+1`, `c-1`), color azure (8)
    *   Down-Right: (`r+1`, `c+1`), color orange (7)
4.  For each of the four target positions (target\_r, target\_c) and its associated color:
    *   Check if `target_r` is within the valid row range (0 to height-1) of the output grid.
    *   Check if `target_c` is within the valid column range (0 to width-1) of the output grid.
    *   If both conditions are true, place the associated color at (`target_r`, `target_c`) in the output grid.
5.  Return the completed output grid.