
## train_1

**input:**
```
0 0 0 0 0 0
0 4 6 0 0 0
0 2 1 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
1 0 0 2 2 0
0 4 6 0 0 0
0 2 1 0 0 0
6 0 0 4 4 0
6 0 0 4 4 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 9 3 0 0
0 0 7 8 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
8 8 0 0 7 7
8 8 0 0 7 7
0 0 9 3 0 0
0 0 7 8 0 0
3 3 0 0 9 9
3 3 0 0 9 9
```


## train_3

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 3 6 0 0
0 0 5 2 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
2 2 0 0 5 5
2 2 0 0 5 5
0 0 3 6 0 0
0 0 5 2 0 0
6 6 0 0 3 3
6 6 0 0 3 3
```

**Perception of Task Elements:**

1.  **Input Structure:** Each input is a grid (appears to be 6x6 in examples) containing mostly white pixels (0) and a single contiguous 2x2 block of four different non-white pixels.
2.  **Output Structure:** The output grid has the same dimensions as the input. It retains the original 2x2 block in its original position. Additionally, four new rectangular blocks of solid color appear in the four corners of the output grid.
3.  **Color Mapping:** The colors of the four corner blocks in the output are determined by the colors in the original 2x2 input block. Specifically, if the input block is `[[A, B], [C, D]]`, the top-left (TL) corner block has color D, the top-right (TR) corner block has color C, the bottom-left (BL) corner block has color B, and the bottom-right (BR) corner block has color A. This corresponds to a reflection or mapping of colors across the center of the 2x2 block to the corners of the grid.
4.  **Size and Position Mapping:** The size and exact position of the corner blocks depend on the coordinates of the top-left corner of the original 2x2 block in the input grid. Let the input block's top-left corner be at `(r0, c0)`.
    *   The TL output block (color D) occupies the rectangle from `(0, 0)` to `(r0-1, c0-1)`. Its size is `r0 x c0`.
    *   The TR output block (color C) occupies the rectangle from `(0, c0+2)` to `(r0-1, c0+3)`. Its size is `r0 x 2`.
    *   The BL output block (color B) occupies the rectangle from `(r0+2, 0)` to `(r0+3, c0-1)`. Its size is `2 x c0`.
    *   The BR output block (color A) occupies the rectangle from `(r0+2, c0+2)` to `(r0+3, c0+3)`. Its size is `2 x 2`.
5.  **Background:** The rest of the output grid remains white (0), except for the original input block and the four new corner blocks.

**YAML Facts:**


```yaml
task_description: Generate four corner blocks based on a central 2x2 block.
grid_properties:
  - dimensions: Constant across input/output pairs (e.g., 6x6 in examples).
  - background_color: white (0)

input_elements:
  - element: central_block
    description: A 2x2 block of non-white pixels.
    properties:
      - colors: Four distinct colors [A, B] in the first row, [C, D] in the second row.
      - location: Defined by the top-left coordinate (r0, c0).
      - uniqueness: There is only one such block in the input.

output_elements:
  - element: preserved_block
    description: The original 2x2 central_block copied to the output.
    properties:
      - colors: Same as central_block [A, B], [C, D].
      - location: Same as central_block (r0, c0).
  - element: corner_blocks
    description: Four rectangular blocks added to the corners of the grid.
    count: 4
    properties:
      - relationship: Each corner block's color and size/position is determined by one color and the position (r0, c0) of the input central_block.
      - block_TL:
          color: D (from input central_block[1, 1])
          location_top_left: (0, 0)
          location_bottom_right: (r0 - 1, c0 - 1)
          size: r0 rows x c0 columns
      - block_TR:
          color: C (from input central_block[1, 0])
          location_top_left: (0, c0 + 2)
          location_bottom_right: (r0 - 1, c0 + 3)
          size: r0 rows x 2 columns
      - block_BL:
          color: B (from input central_block[0, 1])
          location_top_left: (r0 + 2, 0)
          location_bottom_right: (r0 + 3, c0 - 1)
          size: 2 rows x c0 columns
      - block_BR:
          color: A (from input central_block[0, 0])
          location_top_left: (r0 + 2, c0 + 2)
          location_bottom_right: (r0 + 3, c0 + 3)
          size: 2 rows x 2 columns

relationships:
  - type: preservation
    source: input.central_block
    target: output.preserved_block
  - type: generation
    source: input.central_block
    target: output.corner_blocks
    details: The properties (color, size, location) of the four output corner blocks are derived from the colors and location of the input central block as specified above.
```


**Natural Language Program:**

1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify the unique 2x2 block of non-white pixels in the input grid.
3.  Record the colors of this block as `A` (top-left), `B` (top-right), `C` (bottom-left), `D` (bottom-right).
4.  Record the row `r0` and column `c0` of the top-left pixel of this 2x2 block.
5.  Copy the original 2x2 block (`[[A, B], [C, D]]`) onto the output grid, starting at position `(r0, c0)`.
6.  Create the top-left corner block: Fill the rectangular region from grid coordinate `(0, 0)` to `(r0 - 1, c0 - 1)` with color `D`.
7.  Create the top-right corner block: Fill the rectangular region from grid coordinate `(0, c0 + 2)` to `(r0 - 1, c0 + 3)` with color `C`.
8.  Create the bottom-left corner block: Fill the rectangular region from grid coordinate `(r0 + 2, 0)` to `(r0 + 3, c0 - 1)` with color `B`.
9.  Create the bottom-right corner block: Fill the rectangular region from grid coordinate `(r0 + 2, c0 + 2)` to `(r0 + 3, c0 + 3)` with color `A`.
