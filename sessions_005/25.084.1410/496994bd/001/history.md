
## train_1

**input:**
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```


## train_2

**input:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```


**output:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```

Okay, let's analyze the provided examples.

## Perception of Task Elements

1.  **Grid Structure:** Both input and output are grids of pixels (represented by numbers 0-9). The examples use grids of size 10x5 and 10x3.
2.  **Colors Used:** The examples use white (0), red (2), green (3), and azure (8).
3.  **Input Pattern:** In both examples, the input grid has a block of one or more non-white, uniformly colored horizontal rows at the very top. The rest of the grid is filled with white pixels.
4.  **Output Pattern:** The output grid retains the original colored rows at the top. Additionally, a vertically flipped version of this top block appears at the very bottom of the grid. The rows between the top block and the bottom (reflected) block remain white.
5.  **Transformation:** The core transformation seems to be identifying the contiguous block of non-white rows at the top of the input grid and reflecting this block vertically across the horizontal midline of the grid, placing the reflected image at the bottom while keeping the original top block intact.

## Facts


```yaml
task_context:
  grid_dimensions:
    - input_height: 10
    - input_width: variable (5 in example 1, 3 in example 2)
    - output_height: same as input_height
    - output_width: same as input_width
  colors_present: [white (0), red (2), green (3), azure (8)] # Based on examples, others might appear

identified_objects:
  - object_type: horizontal_row_block
    location: top of the input grid
    description: A contiguous block of one or more rows starting from the first row (row 0), where each row consists of a single, non-white color.
    properties:
      - height: number of rows in the block
      - rows: list of rows, each containing pixel data (color values)

actions_on_objects:
  - action: identify
    target: the top non-white horizontal_row_block in the input grid
  - action: copy
    source: the identified top block
    destination: same location in the output grid
  - action: reflect
    target: the identified top block
    axis: horizontal (across the grid's vertical center)
    description: The order of rows within the block is reversed.
  - action: place
    source: the reflected block
    destination: the bottom of the output grid, aligned such that the last row of the input corresponds to the first row of the reflected block, the second-to-last row to the second row, and so on.

relationships:
  - type: spatial_reflection
    description: The block of rows appearing at the bottom of the output grid is a vertical reflection of the block of rows at the top of the input grid.
  - type: preservation
    description: The original top block from the input grid is preserved in the same location in the output grid.
  - type: background_fill
    description: All rows in the output grid that are not part of the original top block or the reflected bottom block are filled with white (0).

```


## Natural Language Program

1.  Create the output grid by making an exact copy of the input grid.
2.  Identify the contiguous block of non-white rows starting from the top row (row index 0) of the input grid. Let the height of this block (number of rows) be `H` and the total height of the grid be `GridHeight`.
3.  Iterate through the rows of this identified top block, from row index `i = 0` up to `H - 1`.
4.  For each row `i` in the top block of the input grid, copy the contents of that row to the row at index `(GridHeight - 1 - i)` in the output grid.
