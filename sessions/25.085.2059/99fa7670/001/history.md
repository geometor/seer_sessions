
## train_1

**input:**
```
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 5 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 8 8 8 8 8
0 0 0 0 0 8
0 0 0 0 0 8
0 0 0 5 5 5
0 0 0 0 0 5
```


## train_2

**input:**
```
0 0 0
0 6 0
0 0 0
```


**output:**
```
0 0 0
0 6 6
0 0 6
```


## train_3

**input:**
```
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
0 7 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 8 8 8
0 0 0 0 8
0 7 7 7 7
0 0 0 0 7
0 0 6 6 6
0 0 0 0 6
```


## train_4

**input:**
```
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 0 0 0 2
0 3 3 3 3 3
0 0 0 0 0 3
0 0 0 0 0 3
```

**Perception**

1.  **Input/Output Structure:** Both input and output are 2D grids of pixels, represented by integers 0-9 (colors). The background is consistently white (0).
2.  **Key Elements:** The input grids contain one or more isolated, non-white pixels scattered across the white background.
3.  **Transformation:** The output grids show that each non-white pixel from the input has generated an 'L' shape of the same color.
4.  **'L' Shape Formation:**
    *   The 'L' shape originates at the position of the input pixel.
    *   A horizontal line extends from the original pixel's position to the rightmost edge of the grid, filling all cells in that row within this range.
    *   A vertical line extends downwards from the original pixel's row in the rightmost column, filling all cells in the rightmost column from that row down to the bottom edge of the grid.
5.  **Overlap:** When multiple 'L' shapes are generated, they might overlap. The examples show that the color of the overlap is determined by the pixel generating the shape (the specific rules of which color "wins" an overlap aren't explicitly tested with conflicting colors in the same overlap zone in the examples, but the process seems additive or potentially based on processing order, although the final pattern seems independent of order based on the examples provided). A simpler interpretation is that all required cells for all 'L' shapes are painted, overwriting the background and potentially parts of other 'L' shapes.
6.  **Background:** White pixels in the input remain white in the output unless they are overwritten by part of an 'L' shape.

**Facts**


```yaml
task_type: pattern_generation
components:
  - type: grid
    properties:
      - background_color: white (0)
  - type: object
    identifier: colored_pixel
    properties:
      - color: non-white (1-9)
      - location: row, column
actions:
  - name: generate_L_shape
    input: colored_pixel (color C, row R, column C)
    output: painted_region
    steps:
      - step: paint_horizontal_segment
        details: Fill cells in row R from column C to the right edge (width-1) with color C.
      - step: paint_vertical_segment
        details: Fill cells in the rightmost column (width-1) from row R to the bottom edge (height-1) with color C.
grid_transformations:
  - description: Apply 'generate_L_shape' independently for every non-white pixel found in the input grid onto an initially white output grid of the same dimensions.
relationships:
  - Each non-white input pixel maps directly to one L-shaped pattern in the output.
  - The position and color of the input pixel determine the position and color of the generated L-shape.
  - The grid boundaries (right edge, bottom edge) define the extent of the L-shape segments.
```


**Natural Language Program**

1.  Initialize a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Scan the input grid to find all non-white pixels. For each non-white pixel found:
    a.  Record its color (`C`), row index (`R`), and column index (`Col`).
3.  For each recorded non-white pixel (with color `C`, row `R`, column `Col`):
    a.  **Draw Horizontal Line:** Iterate from the pixel's column `Col` to the last column of the grid (`grid_width - 1`). For each column index `j` in this range, set the color of the cell at `(R, j)` in the output grid to `C`.
    b.  **Draw Vertical Line:** Iterate from the pixel's row `R` to the last row of the grid (`grid_height - 1`). For each row index `i` in this range, set the color of the cell at `(i, grid_width - 1)` (the rightmost column) in the output grid to `C`.
4.  Return the completed output grid.
