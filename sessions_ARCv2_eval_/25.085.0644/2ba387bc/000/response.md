## Perception

1.  **Input Grid Structure:** The input grids contain various non-overlapping 4x4 patterns scattered amidst a background of white pixels (0).
2.  **Pattern Types:** These 4x4 patterns are of two main types:
    *   **Solid:** A 4x4 square where all 16 pixels share the same non-white color.
    *   **Hollow:** A 4x4 square where the 12 border pixels share the same non-white color, and the 4 interior pixels are white (0).
3.  **Output Grid Structure:** The output grid is a composite grid formed by rearranging the identified 4x4 patterns from the input. The output grid has a fixed width of 8 pixels and a height that is a multiple of 4, determined by the number of patterns found.
4.  **Transformation Logic:** The transformation involves identifying all solid and hollow 4x4 squares in the input, sorting them based on their original position, and arranging them into two columns in the output grid. Hollow squares go into the left column, and solid squares go into the right column. The vertical order within each column corresponds to the top-to-bottom order of the squares in the input grid.
5.  **Padding:** If one type of square (hollow or solid) has fewer instances than the other, the corresponding column in the output grid is padded with 4x4 blocks of white pixels at the bottom to match the height determined by the maximum count.

## Facts


```yaml
objects:
  - type: grid
    description: Input grid containing scattered patterns.
  - type: grid
    description: Output grid containing rearranged patterns.
  - type: pattern
    subtype: square_4x4
    properties:
      - solid: True if all 16 pixels are the same non-white color.
      - hollow: True if the 12 border pixels are the same non-white color and the 4 inner pixels are white.
      - color: The non-white color used in the pattern.
      - position: The top-left (row, column) coordinates in the input grid.

actions:
  - identify: Find all non-overlapping 4x4 patterns in the input grid that are either 'solid' or 'hollow'.
  - classify: Determine if each identified pattern is 'solid' or 'hollow'.
  - sort:
      - Separate patterns into two groups: 'hollow' and 'solid'.
      - Sort each group based on their original top-left row coordinate, then column coordinate.
  - arrange:
      - Create a new output grid with width 8 and height determined by `max(count(hollow), count(solid)) * 4`.
      - Place sorted 'hollow' patterns sequentially down the left column (columns 0-3) of the output grid.
      - Place sorted 'solid' patterns sequentially down the right column (columns 4-7) of the output grid.
  - pad: Fill any remaining space in the output grid (due to unequal numbers of hollow and solid patterns) with white pixels.

relationships:
  - The output grid's content is derived solely from the 'solid' and 'hollow' 4x4 patterns found in the input grid.
  - The relative vertical order of patterns of the same type (solid/hollow) is preserved from the input to the output.
  - Hollow patterns are always placed to the left of solid patterns in the output.
```


## Natural Language Program

1.  **Scan** the input grid to locate all distinct 4x4 blocks that are not entirely composed of white pixels.
2.  **Identify** each located 4x4 block as either a "solid square" (all 16 pixels have the same non-white color) or a "hollow square" (the 12 border pixels have the same non-white color, and the 4 central pixels are white). Record the pattern, its type (solid or hollow), and its top-left coordinates from the input grid. Ignore any 4x4 blocks that don't fit these definitions.
3.  **Separate** the identified squares into two lists: one for hollow squares and one for solid squares.
4.  **Sort** the list of hollow squares based first on their original top-row index, and then by their original left-column index as a tiebreaker.
5.  **Sort** the list of solid squares using the same criteria (original top-row index, then original left-column index).
6.  **Determine** the number of rows needed in the output grid by taking the maximum count between the number of hollow squares and the number of solid squares. The output grid height will be this maximum count multiplied by 4. The output grid width is fixed at 8.
7.  **Construct** the output grid, initializing it with white pixels.
8.  **Place** the sorted hollow squares into the output grid. Starting from the top row (row 0), place each 4x4 hollow square pattern into the left columns (columns 0-3) sequentially downwards.
9.  **Place** the sorted solid squares into the output grid. Starting from the top row (row 0), place each 4x4 solid square pattern into the right columns (columns 4-7) sequentially downwards.
10. **Ensure** any grid space remaining below the placed squares (if the counts of hollow and solid squares were unequal) remains filled with white pixels.