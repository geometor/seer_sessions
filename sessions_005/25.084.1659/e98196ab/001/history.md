
## train_1

**input:**
```
0 3 0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 7 0 0
0 0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 7 0 0 0 7
```


**output:**
```
0 3 0 0 0 3 0 0 0 3 7
7 0 0 0 0 0 0 0 7 0 0
0 0 7 3 7 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
7 3 0 0 0 0 7 0 0 0 7
```


## train_2

**input:**
```
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 8 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0
1 0 0 0 0 0 0 0 0 0 1
```


**output:**
```
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 1 0 1 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 1 0 0 0 0 0 1 0 0
1 8 0 0 0 0 0 0 0 8 1
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 1 0 1 0 0 1 0
0 0 0 0 0 0 1 0 0 0 0
0 0 1 0 1 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 1
5 5 5 5 5 5 5 5 5 5 5
2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 2 0 0
```


**output:**
```
2 0 0 0 0 2 0 0 0 0 2
0 1 0 1 1 0 1 0 0 1 0
0 0 0 0 0 0 1 0 0 0 0
0 0 1 0 1 0 0 1 0 0 0
2 0 0 0 2 0 0 0 2 0 1
```

**Perception**

1.  **Input Structure:** Each input grid is divided into three horizontal sections: a top section, a single row of gray pixels (color 5) acting as a separator, and a bottom section.
2.  **Symmetry:** The top and bottom sections have the same height. The gray separator line is exactly in the middle vertically.
3.  **Output Structure:** The output grid has the same width as the input grid and the same height as the top (or bottom) section of the input grid.
4.  **Transformation:** The output grid appears to be a composite of the top and bottom sections of the input grid. Specifically, it looks like the bottom section is overlaid onto the top section. Where pixels exist in the bottom section (i.e., are non-white/non-zero), they appear in the output grid at the corresponding position. Where pixels in the bottom section are white (zero), the original pixel from the top section is retained in the output. The gray separator line is discarded.

**Facts**


```yaml
task_description: Overlay the non-white pixels from the bottom half of the input grid onto the top half, discarding the central gray separator line.

definitions:
  - name: Input Grid
    type: 2D array of integers (colors)
    properties:
      - Contains a single horizontal line composed entirely of gray pixels (color 5).
      - This gray line divides the grid into a top region and a bottom region of equal height.
  - name: Gray Separator Line
    type: Object (horizontal line)
    properties:
      - Color: Gray (5)
      - Location: Central horizontal row.
      - Role: Separates the Top Region and Bottom Region.
  - name: Top Region
    type: Subgrid
    properties:
      - Location: Rows above the Gray Separator Line.
      - Content: Pixels of various colors, including white (0).
      - Dimensions: Defines the height and width of the Output Grid.
  - name: Bottom Region
    type: Subgrid
    properties:
      - Location: Rows below the Gray Separator Line.
      - Content: Pixels of various colors, including white (0).
      - Dimensions: Same height as the Top Region, same width as the Input Grid.
  - name: Output Grid
    type: 2D array of integers (colors)
    properties:
      - Dimensions: Same height and width as the Top Region.
      - Content: Result of overlaying the Bottom Region onto the Top Region.

transformation:
  - action: Identify the Gray Separator Line row index.
  - action: Extract the Top Region (rows above the separator).
  - action: Extract the Bottom Region (rows below the separator).
  - action: Create an Output Grid initialized as a copy of the Top Region.
  - action: Iterate through each cell (row `r`, column `c`) in the Bottom Region.
  - condition: If the pixel value `P_bottom` at `(r, c)` in the Bottom Region is not white (0).
  - consequence: Update the pixel value at the corresponding cell `(r, c)` in the Output Grid to `P_bottom`.
  - relation: The correspondence between Bottom Region cells and Output Grid cells is direct (same row index `r` relative to the start of the region, same column index `c`).
```


**Natural Language Program**

1.  Locate the horizontal row in the input grid that consists entirely of gray pixels (color 5). Let the row index of this separator line be `sep_idx`.
2.  Determine the height of the top region, which is `H = sep_idx`. The top region consists of rows 0 to `H-1`.
3.  Determine the bottom region, which consists of rows `sep_idx + 1` to `sep_idx + H`.
4.  Create a new output grid with height `H` and the same width as the input grid.
5.  Initialize the output grid by copying the pixels from the top region (rows 0 to `H-1`) of the input grid.
6.  Iterate through each cell of the output grid, using row index `r` (from 0 to `H-1`) and column index `c` (from 0 to width-1).
7.  For each cell `(r, c)` in the output grid, check the color of the corresponding pixel in the *bottom* region of the input grid. The corresponding input grid coordinates are `(r + sep_idx + 1, c)`.
8.  If the color of the pixel in the bottom region at `(r + sep_idx + 1, c)` is not white (i.e., not 0), update the color of the pixel at `(r, c)` in the output grid to this color.
9.  If the color of the pixel in the bottom region is white (0), the pixel at `(r, c)` in the output grid retains its value copied from the top region.
10. Return the final output grid.
