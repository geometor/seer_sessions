
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 5 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 5 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input grids contain two distinct non-white pixels located on the same horizontal row, positioned at the far left and far right ends of the grid (column 0 and column 10 in the examples). The rest of the grid is white.

The transformation modifies only the row containing these two pixels. The space *between* these two endpoint pixels is filled in. The filling is partitioned:
1.  The segment from the left endpoint (exclusive) up to the horizontal midpoint is filled with the color of the left endpoint pixel.
2.  The segment from the horizontal midpoint (exclusive) up to the right endpoint is filled with the color of the right endpoint pixel.
3.  The single pixel exactly at the horizontal midpoint between the two endpoints is colored gray (5).

The original endpoint pixels retain their positions and colors. All other rows remain unchanged (white).

**Facts:**


```yaml
task_context:
  grid_properties:
    - Input and output grids have the same dimensions.
    - Most pixels are white (0).
  input_elements:
    - Contains exactly two non-white pixels.
    - These two pixels ('endpoints') are located on the same row.
    - In the examples, the endpoints are at the horizontal boundaries (first and last column).
  output_elements:
    - The row containing the original endpoints is modified.
    - All other rows remain unchanged.
    - The space between the endpoints on their row is filled.
  transformation:
    - Finds the two non-white pixels (endpoints).
    - Identifies the row they share.
    - Calculates the horizontal midpoint column between the endpoints.
    - Fills the row segment between the left endpoint and the midpoint with the left endpoint's color.
    - Fills the row segment between the midpoint and the right endpoint with the right endpoint's color.
    - Colors the midpoint pixel gray (5).

objects:
  - object: endpoint_1
    description: The leftmost non-white pixel.
    properties:
      - color: C1 (e.g., green=3, blue=1)
      - row: R
      - column: C_left
  - object: endpoint_2
    description: The rightmost non-white pixel.
    properties:
      - color: C2 (e.g., orange=7, red=2)
      - row: R
      - column: C_right
  - object: fill_segment_1
    description: The horizontal segment filled with color C1.
    properties:
      - row: R
      - columns: from C_left + 1 to midpoint_col - 1
      - color: C1
  - object: fill_segment_2
    description: The horizontal segment filled with color C2.
    properties:
      - row: R
      - columns: from midpoint_col + 1 to C_right - 1
      - color: C2
  - object: midpoint_pixel
    description: The pixel exactly in the middle of the endpoints horizontally.
    properties:
      - row: R
      - column: midpoint_col = floor((C_left + C_right) / 2)
      - color: gray (5)

relationships:
  - Endpoint 1 and Endpoint 2 are on the same row (R).
  - Fill Segment 1 is to the right of Endpoint 1 and to the left of Midpoint Pixel.
  - Fill Segment 2 is to the right of Midpoint Pixel and to the left of Endpoint 2.
  - Midpoint Pixel separates Fill Segment 1 and Fill Segment 2.

actions:
  - Find the row (R) and columns (C_left, C_right) and colors (C1, C2) of the two non-white pixels.
  - Verify they are on the same row.
  - Calculate the midpoint column: midpoint_col = floor((C_left + C_right) / 2).
  - For each column 'col' from C_left + 1 up to (but not including) midpoint_col, set the pixel at (R, col) to color C1.
  - Set the pixel at (R, midpoint_col) to gray (5).
  - For each column 'col' from midpoint_col + 1 up to (but not including) C_right, set the pixel at (R, col) to color C2.
  - Copy the input grid to the output grid initially to preserve unchanged pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to find all non-white pixels.
3.  Identify the two non-white pixels. Let their coordinates and colors be `(R1, C1, Color1)` and `(R2, C2, Color2)`.
4.  Verify that `R1` equals `R2`. If not, the rule may not apply (though based on examples, assume they are always on the same row). Let `R = R1`.
5.  Determine which pixel is the left endpoint and which is the right endpoint based on their column indices. Let the left endpoint be `(R, C_left, Color_left)` and the right endpoint be `(R, C_right, Color_right)`, where `C_left < C_right`.
6.  Calculate the column index of the midpoint pixel: `midpoint_col = floor((C_left + C_right) / 2)`.
7.  Iterate through the columns `col` from `C_left + 1` up to `midpoint_col - 1`. For each `col`, set the pixel in the output grid at `(R, col)` to `Color_left`.
8.  Set the pixel in the output grid at `(R, midpoint_col)` to gray (5).
9.  Iterate through the columns `col` from `midpoint_col + 1` up to `C_right - 1`. For each `col`, set the pixel in the output grid at `(R, col)` to `Color_right`.
10. Return the modified output grid.
