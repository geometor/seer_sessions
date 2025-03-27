## Perception

1.  **Input/Output Size**: The input grids are consistently 5x7, while the output grids are 5x3.
2.  **Separator**: All input grids feature a vertical line of blue pixels (color 1) in the 4th column (index 3). This line consistently separates the grid into a 5x3 left section and a 5x3 right section. The blue line itself does not appear in the output.
3.  **Content**: Input grids contain white (0), blue (1), and maroon (9) pixels. Output grids contain only white (0) and azure (8) pixels.
4.  **Output Origin**: The dimensions of the output grid (5x3) match the dimensions of the left section of the input grid. This suggests the output is primarily derived from this left section, possibly influenced by the right section.
5.  **Transformation Rule**: By comparing the left section (`Input[r, 0:3]`) with the right section (`Input[r, 4:7]`) cell by cell for each row `r`:
    *   An output cell at `(r, c)` becomes azure (8) if, and only if, the corresponding cell in the left section (`Input[r, c]`) and the corresponding cell in the right section (`Input[r, c+4]`) are *both* white (0).
    *   In all other cases (cells don't match, or they match but are not white), the output cell at `(r, c)` is white (0).

## Facts


```yaml
task_structure:
  grid_dimensionality: 2D
  input_grid_size: [5, 7]
  output_grid_size: [5, 3]

components:
  - type: separator
    properties:
      color: blue (1)
      location: column index 3
      orientation: vertical
      role: divides input grid into left and right sections of equal size (5x3)
  - type: subgrid
    name: left_section
    properties:
      location: columns 0, 1, 2
      size: [5, 3]
      content_colors: [white (0), maroon (9)]
  - type: subgrid
    name: right_section
    properties:
      location: columns 4, 5, 6
      size: [5, 3]
      content_colors: [white (0), maroon (9)]
  - type: output_grid
    properties:
      size: [5, 3] (same as left_section)
      content_colors: [white (0), azure (8)]

relationships_and_actions:
  - action: comparison
    input_1: left_section
    input_2: right_section
    details: Compare cells at the same relative position (r, c) within each section.
  - action: conditional_mapping
    condition: |
      For a given position (r, c):
      left_section[r, c] == right_section[r, c] AND left_section[r, c] == white (0)
    true_output: Set output_grid[r, c] to azure (8).
    false_output: Set output_grid[r, c] to white (0).
```


## Natural Language Program

1.  Identify the vertical blue line (color 1) in the input grid; this is the separator at column index 3.
2.  Extract the 5x3 subgrid to the left of the separator (columns 0, 1, 2). Call this `LeftGrid`.
3.  Extract the 5x3 subgrid to the right of the separator (columns 4, 5, 6). Call this `RightGrid`.
4.  Initialize an output grid of the same dimensions as `LeftGrid` (5x3) and fill it with white pixels (color 0). Call this `OutputGrid`.
5.  Iterate through each cell position `(r, c)` from `r = 0` to `4` and `c = 0` to `2`.
6.  At each position `(r, c)`, compare the pixel value in `LeftGrid` (`LeftGrid[r, c]`) with the pixel value in `RightGrid` (`RightGrid[r, c]`).
7.  If `LeftGrid[r, c]` is equal to `RightGrid[r, c]` AND the value is white (0), then set the corresponding cell in the `OutputGrid` (`OutputGrid[r, c]`) to azure (8).
8.  Otherwise (if the values are not equal, or if they are equal but not white), leave the corresponding cell in the `OutputGrid` as white (0).
9.  Return the final `OutputGrid`.