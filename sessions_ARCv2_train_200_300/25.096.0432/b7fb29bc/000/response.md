## Perception

The input and output are 15x15 grids of integers.
The input grid contains a rectangular frame made of the digit 3, enclosing an area primarily filled with 0s. Sometimes, there are isolated 3s within this enclosed area. The area outside the frame is filled with 0s.
The output grid retains the 0s outside the frame and the frame itself (the 3s).
The transformation occurs within the area enclosed by the 3s frame.
The 0s inside the frame are replaced with either 2s or 4s. The isolated 3s within the frame remain unchanged.
The digit 4 appears in cells that were originally 0 but are adjacent (horizontally or vertically) to any cell containing a 3 (either part of the outer frame or an isolated internal 3).
The digit 2 appears in cells that were originally 0 and are *not* adjacent to any cell containing a 3. They are typically surrounded by 4s or other 2s within the enclosed area.
Essentially, the task involves identifying the region bounded by the outer frame, recognizing internal obstacles (3s), and then performing a conditional fill on the internal 0s based on their adjacency to any 3s.

## Facts


```yaml
objects:
  - name: grid
    type: 2D array of integers
    properties:
      - dimensions: 15x15
      - cell_values: [0, 2, 3, 4] (0, 3 in input; 0, 2, 3, 4 in output)
  - name: frame
    type: structure within the grid
    properties:
      - composed_of: cells with value 3
      - shape: rectangular
      - function: defines a boundary
  - name: internal_area
    type: region within the grid
    properties:
      - location: enclosed by the frame
      - initial_content: cells with value 0 and potentially isolated cells with value 3
      - final_content: cells with values 2, 3, 4
  - name: obstacles
    type: cells within the internal_area
    properties:
      - value: 3 (in both input and output)
      - location: isolated within the internal_area in the input
  - name: fill_cells
    type: cells within the internal_area
    properties:
      - initial_value: 0
      - final_value: 2 or 4

relationships:
  - type: adjacency
    between: grid cells
    definition: Cells sharing a horizontal or vertical edge.
  - type: containment
    subject: internal_area
    object: frame
    definition: The internal_area is spatially located inside the boundary defined by the frame.

actions:
  - name: identify_frame
    input: input_grid
    output: set of coordinates for frame cells (value 3)
  - name: identify_internal_area
    input: input_grid, frame coordinates
    output: set of coordinates for internal cells (initially 0 or 3)
  - name: identify_obstacles
    input: internal_area coordinates, input_grid
    output: set of coordinates for internal obstacle cells (value 3)
  - name: conditional_fill
    input: input_grid, internal_area coordinates, obstacle coordinates, frame coordinates
    output: output_grid
    logic:
      - Iterate through each cell (r, c) in the internal_area.
      - If input_grid[r][c] is 0:
        - Check its neighbors (up, down, left, right).
        - If any neighbor has value 3 (either part of the frame or an obstacle):
          - Set output_grid[r][c] to 4.
        - Else:
          - Set output_grid[r][c] to 2.
      - If input_grid[r][c] is 3 (an obstacle):
        - Set output_grid[r][c] to 3.
      - Copy all other cells (frame and outside area) from input_grid to output_grid.

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all cells in the input grid that belong to the rectangular frame (value 3).
3.  Identify all cells located strictly inside the boundary defined by the frame.
4.  For each cell (row `r`, column `c`) identified as being inside the frame:
    a.  Check the value of the cell at (`r`, `c`) in the *input* grid.
    b.  If the input value is 0:
        i.  Examine the four adjacent neighbors (up, down, left, right) of the cell at (`r`, `c`) in the *input* grid.
        ii. If any of these neighbors has the value 3:
            Assign the value 4 to the cell at (`r`, `c`) in the *output* grid.
        iii. Otherwise (if none of the neighbors has the value 3):
            Assign the value 2 to the cell at (`r`, `c`) in the *output* grid.
    c.  If the input value is 3 (meaning it's an internal obstacle), leave the value as 3 in the *output* grid (already copied in step 1).
5.  Return the modified output grid.