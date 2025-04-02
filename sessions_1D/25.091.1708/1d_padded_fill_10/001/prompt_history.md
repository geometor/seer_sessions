
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
```


## train_2

**input:**
```
7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

The input grids are sparsely populated with a single non-white color against a white background. The non-white pixels appear scattered, often forming a rough diagonal pattern. The output grids maintain the same dimensions as the inputs. The transformation involves filling rows with the non-white color. Specifically, for each row, the filling starts from the column where the first non-white pixel occurs in the input row and extends all the way to the right edge of the grid. If a row in the input contains only white pixels, the corresponding row in the output remains entirely white. The color used for filling is the same as the non-white color found in the input grid.

**YAML Facts:**


```yaml
task_description: Fill rows to the right starting from the first non-white pixel.
grid_properties:
  - dimensions: Input and output grids have identical height and width.
  - background_color: White (0) is the predominant background color.
objects:
  - object: Trigger Pixel
    description: The leftmost non-white pixel in each row of the input grid.
    properties:
      - color: Varies across examples (green, orange, red), but is consistent within a single example.
      - role: Determines the fill color and the starting column for the fill operation in its row.
  - object: Fill Area
    description: The region in the output grid that gets filled with the non-white color.
    properties:
      - color: Same as the Trigger Pixel color for that example.
      - location: Starts at the column of the Trigger Pixel and extends to the rightmost column within the same row.
actions:
  - action: Identify Fill Color
    description: Determine the single non-white color present in the input grid.
  - action: Scan Rows
    description: Process the input grid row by row.
  - action: Find Trigger
    description: For each row, locate the column index of the first (leftmost) non-white pixel.
  - action: Fill Right
    description: In the output grid, for each row containing a trigger pixel, color all cells from the trigger pixel's column to the right edge of the grid with the identified fill color.
relationships:
  - relationship: Row Correspondence
    description: Each row in the output grid corresponds directly to the row at the same index in the input grid.
  - relationship: Trigger-Fill Dependency
    description: The presence and column position of a Trigger Pixel in an input row determine if and where the Fill Area starts in the corresponding output row.
    properties:
      - If no Trigger Pixel exists in an input row, the output row remains white.
      - The Fill Area always uses the color of the Trigger Pixel.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify the single non-white color present in the input grid. Let this be the `fill_color`.
3.  Iterate through each row of the input grid, from top to bottom (row index `r`).
4.  For the current row `r`, scan from left to right (column index `c`) to find the first column `start_c` where the pixel color matches the `fill_color`.
5.  If such a `start_c` is found for row `r`:
    a.  Iterate through the columns of the output grid for row `r`, starting from `start_c` up to the last column.
    b.  Set the color of each pixel in this range (`output_grid[r][c]` where `c >= start_c`) to the `fill_color`.
6.  If no pixel matching the `fill_color` is found in the input row `r`, the corresponding output row `r` remains unchanged (all white).
7.  After processing all rows, return the completed output grid.
