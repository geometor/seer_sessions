
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 0 0
0 0 4 4 0 0
4 4 4 4 0 0
4 4 4 4 0 0
0 0 0 0 4 4
0 0 0 0 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 0 0
0 0 4 4 4 4 0 0
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
0 0 4 4 4 4 0 0
0 0 4 4 4 4 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 0 0
0 0 4 4 0 0
4 4 4 4 0 0
4 4 4 4 0 0
0 0 4 4 0 0
0 0 4 4 0 0
0 0 4 4 4 4
0 0 4 4 4 4
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Grids:** Both inputs and outputs are 2D grids composed of integer values, specifically 0 and 4.
2.  **Objects:** The primary object within the input grid is the shape formed by the non-zero cells (value 4). The background is represented by zeros (0).
3.  **Transformation:** The core transformation appears to be a scaling operation applied to the shape identified in the input, followed by cropping to the bounds of the scaled shape.
4.  **Scaling Factor:** Each cell containing a '4' in the input seems to expand into a 2x2 block of '4's in the output. This suggests a scaling factor of 2.
5.  **Cropping/Framing:** The output grid's dimensions are not fixed but depend on the size and position of the scaled shape. The output grid tightly frames the resulting 2x scaled pattern. Zeros are used as the background filler within this frame.

**YAML Facts:**


```yaml
task_description: Scale a shape defined by non-zero elements within a grid and crop the output to the scaled shape's bounding box.
elements:
  - element: grid
    properties:
      - type: 2D array
      - content: integers (0 and 4)
      - role: input and output container
  - element: shape
    properties:
      - composed_of: cells with value 4 in the input grid
      - connectivity: typically connected, but not necessarily
      - location: variable within the input grid
  - element: background
    properties:
      - value: 0
      - fills: space not occupied by the shape
actions:
  - action: identify_shape
    input: input grid
    output: coordinates of all cells with value 4
  - action: calculate_bounding_box
    input: coordinates of shape cells
    output: top-left corner (min_row, min_col), height, width
  - action: scale_shape
    input: shape cells relative to bounding box top-left
    parameters:
      - scale_factor: 2
    output: coordinates of 2x2 blocks in the output grid
  - action: create_output_grid
    parameters:
      - dimensions: (bounding_box_height * 2, bounding_box_width * 2)
      - initial_value: 0
    output: initialized output grid
  - action: place_scaled_shape
    input:
      - output grid
      - scaled shape coordinates (as 2x2 blocks)
      - value: 4
    output: output grid with the scaled shape placed
relationships:
  - relation: scaling
    subject: input shape cell (value 4)
    object: 2x2 block of cells (value 4) in the output grid
    details: Each input '4' maps to a 2x2 block of '4's.
  - relation: bounding
    subject: output grid dimensions
    object: scaled shape
    details: Output grid dimensions are determined by twice the height and width of the input shape's bounding box.
  - relation: positioning
    subject: scaled shape in the output grid
    object: input shape within its bounding box
    details: The relative position of a '4' within the input bounding box determines the position of its corresponding 2x2 block in the output grid. (Relative row `r_rel`, relative col `c_rel`) maps to output top-left block position (`r_rel * 2`, `c_rel * 2`).
```


**Natural Language Program:**

1.  Identify all cells in the input grid that contain the value 4. If no such cells exist, output an empty grid or handle as appropriate (based on potential edge cases, though not shown in examples).
2.  Determine the minimum bounding box that encloses all identified '4' cells. Record the row (`min_row`) and column (`min_col`) of the top-left corner, and the height (`bb_height`) and width (`bb_width`) of this box.
3.  Create a new output grid, initialized with zeros, having dimensions (`bb_height` * 2) rows and (`bb_width` * 2) columns.
4.  Iterate through each cell (`r`, `c`) of the input grid within the calculated bounding box (from `min_row` to `min_row + bb_height - 1` and `min_col` to `min_col + bb_width - 1`).
5.  If the input cell `input[r][c]` contains the value 4:
    a. Calculate the corresponding top-left coordinates (`out_r`, `out_c`) in the output grid:
       `out_r = (r - min_row) * 2`
       `out_c = (c - min_col) * 2`
    b. Set the value 4 in the 2x2 block of the output grid starting at (`out_r`, `out_c`). Specifically, set:
       `output[out_r][out_c] = 4`
       `output[out_r + 1][out_c] = 4`
       `output[out_r][out_c + 1] = 4`
       `output[out_r + 1][out_c + 1] = 4`
6.  Return the generated output grid.
