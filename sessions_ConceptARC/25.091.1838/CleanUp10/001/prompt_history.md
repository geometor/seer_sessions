
## train_1

**input:**
```
2 2 0 2 0 0
0 0 2 2 2 0
2 2 2 2 2 2
2 2 0 2 0 2
2 0 0 2 2 0
0 0 0 2 0 0
```


**output:**
```
0 0 0 2 0 0
0 0 0 2 0 0
2 2 2 2 2 2
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


## train_2

**input:**
```
0 0 2 0 2 0
0 2 0 0 2 0
0 0 2 2 2 2
2 2 0 0 2 2
2 2 2 2 2 2
0 2 0 0 2 0
```


**output:**
```
0 0 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
2 2 2 2 2 2
0 0 0 0 2 0
```

Okay, let's analyze the provided task examples.

**Perception:**

1.  **Grid Size:** Both input and output grids in both examples are 6x6. The grid size remains constant.
2.  **Colors:** The primary colors involved are red (2) and white (0). White appears to be the background color.
3.  **Key Features:**
    *   Both input grids contain scattered red pixels and at least one solid horizontal line composed entirely of red pixels.
    *   Both input grids also contain at least one solid vertical line composed entirely of red pixels.
    *   The output grids seem to retain *only* these solid red lines (both horizontal and vertical) from the input.
4.  **Transformation Pattern:**
    *   In `train_1`, the input has a solid red horizontal line at row 2 and a solid red vertical line at column 3. The output consists *only* of these two lines superimposed. All other red pixels from the input are changed to white (0) in the output.
    *   In `train_2`, the input has a solid red horizontal line at row 4 and a solid red vertical line at column 4. Again, the output consists *only* of these two lines superimposed. All other input red pixels are changed to white (0).
5.  **Inference:** The transformation appears to identify all rows and columns in the input grid that are composed entirely of red (2) pixels. The output grid is constructed by drawing these identified full rows and full columns onto a white background. Pixels retain their red color only if they belong to at least one such complete line (either horizontal or vertical) in the input.

**Facts:**


```yaml
task_context:
  grid_size_preservation: True
  colors_used:
    - red (2)
    - white (0)
  background_color: white (0)

objects:
  - type: line
    subtype: horizontal
    color: red (2)
    property: complete_fill # spans the entire width of the grid
    location_train_1: row 2
    location_train_2: row 4
  - type: line
    subtype: vertical
    color: red (2)
    property: complete_fill # spans the entire height of the grid
    location_train_1: column 3
    location_train_2: column 4
  - type: pixel
    color: red (2)
    property: scattered # not part of a complete horizontal or vertical line
    location_train_1: multiple locations excluding row 2 and column 3
    location_train_2: multiple locations excluding row 4 and column 4

actions:
  - identify: rows composed entirely of red pixels in the input.
  - identify: columns composed entirely of red pixels in the input.
  - create: a new output grid of the same dimensions as the input, initialized with the background color (white).
  - transfer: copy the identified complete red rows from the input to the corresponding rows in the output grid.
  - transfer: copy the identified complete red columns from the input to the corresponding columns in the output grid.
  - result: Pixels in the output grid are red (2) if their position corresponds to a pixel within a complete red row OR a complete red column in the input grid. Otherwise, pixels are white (0).

relationships:
  - superposition: The complete horizontal and vertical red lines identified in the input are superimposed onto the output grid.
  - filtering: Red pixels in the input that are *not* part of a complete row or column are filtered out (set to white) in the output.
```


**Natural Language Program:**

1.  Initialize the output grid with the same dimensions as the input grid, filling it entirely with the background color (white, 0).
2.  Create a boolean mask grid of the same dimensions, initially all False. This mask will mark the locations of pixels that should be red in the final output.
3.  Iterate through each row of the input grid.
4.  If a row consists entirely of red (2) pixels, mark all corresponding positions in that row of the boolean mask grid as True.
5.  Iterate through each column of the input grid.
6.  If a column consists entirely of red (2) pixels, mark all corresponding positions in that column of the boolean mask grid as True.
7.  Iterate through the boolean mask grid. For every position `(row, col)` where the mask value is True, set the corresponding pixel `(row, col)` in the output grid to red (2).
8.  Return the final output grid.
