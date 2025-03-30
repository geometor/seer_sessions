**Perception:**

The input grids contain multiple instances of "framed squares" - square objects composed of an outer frame of one color and an inner "center" of a different color. These squares are separated by a background color (white). The background color is always white (0). The frame colors (red=2, green=3, blue=1) and center colors (yellow=4, green=3, blue=1, red=2, azure=8) vary between examples but seem consistent within an example for defining the squares.

The transformation involves identifying specific pairs of these framed squares and using their shared center color to fill in areas of the white background in the output grid. The key conditions for a pair to trigger a change are:
1.  **Horizontal Adjacency:** The two squares must be on the same horizontal level (occupy the same rows) and be separated only by columns of the white background color.
2.  **Identical Center Color:** The center pixels (or 2x2 area in example 2) of both squares must have the same color.

When such a pair is found, two distinct areas of the white background are filled with the shared center color:
1.  **Between Squares:** The white pixels located in the columns *between* the two squares, and on the same row(s) as the center pixels, are filled.
2.  **Below First Square:** A rectangular block of white pixels located below the *first* square (the one on the left) is filled. The specific location is two rows below the center row(s) of the first square, aligned vertically with the center column(s) of the first square. The height of this block depends on the width of the gap between the squares (height 3 if gap is 3 columns wide, height 2 otherwise).

Squares that do not form such pairs, or pairs that don't meet both conditions (e.g., adjacent but different center colors, or same center color but not adjacent), do not cause any changes. The original squares themselves remain unchanged in the output.

**Facts:**


```yaml
Task: Fill background based on adjacent identical squares

Objects:
  - type: FramedSquare
    properties:
      - frame_color: (integer) color of the square's border
      - center_color: (integer) color of the pixel(s) at the center
      - center_location: (tuple/list) coordinates (row, col) or range of center pixels
      - position: (tuple) top-left corner coordinates (row, col)
      - size: (tuple) height and width (e.g., 3x3, 4x4)
      - bounding_box: (tuple) (min_row, min_col, max_row, max_col)
  - type: Background
    properties:
      - color: (integer) typically 0 (white)

Relationships:
  - type: HorizontallyAdjacent
    arguments: [FramedSquare, FramedSquare]
    condition: Share same row range, separated only by background color columns.
  - type: SameCenterColor
    arguments: [FramedSquare, FramedSquare]
    condition: The center_color property is identical for both squares.

Actions:
  - name: IdentifyFramedSquares
    input: input_grid
    output: list of FramedSquare objects
  - name: FindQualifyingPairs
    input: list of FramedSquare objects
    output: list of pairs (Square1, Square2) meeting HorizontallyAdjacent and SameCenterColor conditions
    constraints: Square1 is to the left of Square2.
  - name: CalculateGap
    input: (Square1, Square2) pair
    output:
      - gap_cols: (list) column indices between Square1 and Square2
      - gap_width: (integer) number of columns in gap_cols
  - name: FillBetween
    input: output_grid, Square1, Square2, gap_cols, fill_color (center_color)
    effect: Modifies output_grid by changing background pixels to fill_color in gap_cols and center rows.
  - name: FillBelow
    input: output_grid, Square1, gap_width, fill_color (center_color)
    effect: Modifies output_grid by changing background pixels to fill_color in a rectangle below Square1's center.
      - location: Starts 2 rows below Square1's center, aligned with Square1's center columns.
      - dimensions: Width matches Square1's center width, height is 3 if gap_width is 3, else 2.

Transformation:
  - Step 1: Initialize output_grid as a copy of input_grid.
  - Step 2: Identify all FramedSquare objects in the input_grid.
  - Step 3: Find all QualifyingPairs (Square1, Square2).
  - Step 4: For each pair:
      - Get fill_color = Square1.center_color.
      - Calculate gap_cols and gap_width.
      - Perform FillBetween action on output_grid.
      - Perform FillBelow action on output_grid.
```


**Natural Language Program:**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Scan the input grid to identify all distinct "framed square" objects. For each square, record its frame color, center color, the row(s) and column(s) of its center pixel(s), and its overall bounding box.
3.  Iterate through all possible pairs of identified framed squares (Square1, Square2).
4.  For each pair, check if they satisfy two conditions:
    a.  They are horizontally adjacent: they occupy the same range of rows, and all columns between the right edge of Square1 and the left edge of Square2 contain only the background color (white, 0).
    b.  They have the same center color.
5.  If a pair (Square1, Square2) satisfies both conditions (where Square1 is the left square):
    a.  Identify the common center color (`fill_color`).
    b.  Identify the column indices strictly between Square1 and Square2 (`gap_cols`).
    c.  Identify the row indices occupied by the center pixels of the squares (`center_rows`).
    d.  For every row `r` in `center_rows` and every column `c` in `gap_cols`: if the pixel at `(r, c)` in the output grid is currently the background color, change it to `fill_color`.
    e.  Calculate the width of the gap: `gap_width = number of columns in gap_cols`.
    f.  Determine the height for the fill area below Square1: `fill_height = 3` if `gap_width == 3`, otherwise `fill_height = 2`.
    g.  Identify the column indices occupied by the center pixel(s) of Square1 (`S1_center_cols`).
    h.  Determine the starting row for the fill area below Square1: `fill_start_row = bottom_row_of_S1_center + 2`.
    i.  For every row `r` from `fill_start_row` to `fill_start_row + fill_height - 1`, and for every column `c` in `S1_center_cols`: if the pixel at `(r, c)` in the output grid is currently the background color, change it to `fill_color`.
6.  After checking all pairs, the final state of the output grid is the result.