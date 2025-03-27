**Perception**

1.  **Input/Output Size:** The input grids are 3x3. The output grids are consistently 9x9, which is 3 times the height and 3 times the width of the input.
2.  **Tiling Structure:** The output grid appears to be constructed by arranging 3x3 blocks, where each block is the size of the original input grid (3x3).
3.  **Content Replication:** The original input grid pattern is replicated three times within the output grid.
4.  **Placement Pattern:** The three copies of the input grid are always placed adjacent to each other, either horizontally in a single row of the 3x3 block structure or vertically in a single column.
5.  **Background Fill:** The remaining six 3x3 blocks in the 9x9 output grid are filled entirely with the white color (0).
6.  **Determining Placement:** The placement (which row or column gets filled with the input pattern and whether it's horizontal or vertical) seems determined by a specific feature within the input grid. Observing the examples:
    *   In `train_1`, the top row (row 0) of the input is monochromatic (all blue, 1). The output tiles the input horizontally across the top row (row 0) of the 3x3 block structure.
    *   In `train_2`, the left column (column 0) of the input is monochromatic (all red, 2). The output tiles the input vertically down the left column (column 0) of the 3x3 block structure.
    *   In `train_3`, the left column (column 0) of the input is monochromatic (all green, 3). The output tiles the input vertically down the left column (column 0) of the 3x3 block structure.
    *   In `train_4`, the middle row (row 1) of the input is monochromatic (all green, 3). The output tiles the input horizontally across the middle row (row 1) of the 3x3 block structure.
7.  **Rule Inference:** The core rule involves identifying the first monochromatic (single non-white color) line (row or column) in the input grid. This line's orientation (horizontal/row or vertical/column) and index determine where the input pattern is tiled three times in the larger output grid.

**Facts**


```yaml
task_description: Tile the input grid 3 times within a 3x3 super-grid structure based on the location and orientation of a monochromatic line in the input.

definitions:
  - object: InputGrid
    properties:
      - height: H
      - width: W
      - grid_values: 2D array of integers 0-9

  - object: OutputGrid
    properties:
      - height: 3 * H
      - width: 3 * W
      - grid_values: 2D array of integers 0-9, initialized to white (0)

  - object: MonochromaticLine
    properties:
      - type: row or column
      - index: integer (0-based index within InputGrid)
      - color: integer (1-9, the single color making up the line)
    identification:
      - The first row or column found in InputGrid where all cells have the same non-white color.

  - object: TileRegion
    properties:
      - base_grid: InputGrid
      - repeat_count: 3
      - orientation: horizontal or vertical (determined by MonochromaticLine type)
      - position_index: integer (determined by MonochromaticLine index)

actions:
  - action: IdentifyMonochromaticLine
    input: InputGrid
    output: MonochromaticLine properties (type, index, color)
    description: Scan rows, then columns of the InputGrid. Return the type (row/column) and index of the first line found where all cells contain the same color, and that color is not white (0).

  - action: ConstructOutputGrid
    input:
      - InputGrid (H x W)
      - MonochromaticLine (type, index)
    output: OutputGrid (3H x 3W)
    description: >
      Create an OutputGrid of size 3H x 3W, initialized with white (0).
      If MonochromaticLine type is 'row' with index 'i':
        Place copies of InputGrid into OutputGrid at block positions (i, 0), (i, 1), and (i, 2).
        (Block (r, c) corresponds to OutputGrid region from row r*H to (r+1)*H-1 and column c*W to (c+1)*W-1).
      If MonochromaticLine type is 'column' with index 'j':
        Place copies of InputGrid into OutputGrid at block positions (0, j), (1, j), and (2, j).

relationships:
  - OutputGrid dimensions are 3 times the InputGrid dimensions.
  - The placement of the repeated InputGrid tiles within the OutputGrid is determined solely by the identified MonochromaticLine from the InputGrid.
  - All areas of the OutputGrid not covered by the InputGrid tiles are filled with white (0).
```


**Natural Language Program**

1.  Determine the height (H) and width (W) of the input grid.
2.  Create a new output grid with height 3*H and width 3*W, initially filled with the white color (0).
3.  Search the input grid for a monochromatic line (a line where all cells have the same color, and that color is not white).
    a.  Iterate through each row (index `i` from 0 to H-1). Check if all cells in that row have the same non-white color. If found, record the type as 'row', the index as `i`, and stop searching.
    b.  If no monochromatic row is found, iterate through each column (index `j` from 0 to W-1). Check if all cells in that column have the same non-white color. If found, record the type as 'column', the index as `j`, and stop searching.
4.  If a monochromatic line of type 'row' with index `i` was found:
    a.  Copy the input grid into the output grid three times horizontally, placing them in the block row `i`. The specific locations are:
        i.   Top-left corner at (i * H, 0 * W)
        ii.  Top-left corner at (i * H, 1 * W)
        iii. Top-left corner at (i * H, 2 * W)
5.  If a monochromatic line of type 'column' with index `j` was found:
    a.  Copy the input grid into the output grid three times vertically, placing them in the block column `j`. The specific locations are:
        i.   Top-left corner at (0 * H, j * W)
        ii.  Top-left corner at (1 * H, j * W)
        iii. Top-left corner at (2 * H, j * W)
6.  Return the completed output grid.