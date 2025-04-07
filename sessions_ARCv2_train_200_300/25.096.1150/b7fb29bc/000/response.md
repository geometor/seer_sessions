## Perception

The input and output are both 15x15 grids containing integer values.
The core structure in the input is a rectangular frame defined by the value 3, located consistently across examples (rows 2-10, columns 3-11).
Inside this frame, the input grid contains 0s and potentially some additional 3s which act as internal "obstacles" or "walls". The positions of these internal 3s vary between examples.
The output grid preserves the external 0s, the outer frame of 3s, and the internal obstacles (3s).
The transformation focuses on the cells within the outer frame that originally contained 0 in the input.
These internal 0s are replaced by either 2 or 4 in the output.
The value 4 is assigned to cells that were originally 0 but are orthogonally adjacent (sharing an edge) to any cell containing a 3 (either the outer frame or an internal obstacle).
The value 2 is assigned to cells that were originally 0 and are *not* orthogonally adjacent to any cell containing a 3.

## Facts


```yaml
objects:
  - id: grid
    description: A 2D array of integers representing the input and output state.
  - id: frame
    description: A rectangular boundary within the grid defined by cells with value 3.
    properties:
      - value: 3
      - location: Consistent across examples (rows 2-10, columns 3-11).
  - id: obstacle
    description: Cells with value 3 located inside the boundary defined by the frame.
    properties:
      - value: 3
      - location: Varies between examples, always within the frame boundary.
  - id: background
    description: Cells with value 0 located outside the frame boundary.
    properties:
      - value: 0
  - id: internal_empty_cell
    description: Cells with value 0 located inside the frame boundary in the input grid.
    properties:
      - value: 0
  - id: fill_cell_type_4
    description: Cells in the output grid corresponding to internal_empty_cells that are adjacent to a frame or obstacle cell.
    properties:
      - value: 4
  - id: fill_cell_type_2
    description: Cells in the output grid corresponding to internal_empty_cells that are not adjacent to any frame or obstacle cell.
    properties:
      - value: 2

relationships:
  - type: containment
    description: Obstacles and internal_empty_cells are contained within the frame.
  - type: adjacency
    description: Orthogonal adjacency (up, down, left, right) between cells. Key for determining fill value.
  - type: transformation
    description: internal_empty_cells are transformed into fill_cell_type_4 or fill_cell_type_2 based on adjacency to frame or obstacle cells.

actions:
  - id: identify_frame_region
    description: Determine the area enclosed by the outer frame of 3s.
  - id: check_adjacency
    description: For each internal_empty_cell, check its orthogonal neighbors in the input grid.
  - id: assign_value
    description: Assign 4 if adjacent to any 3, assign 2 otherwise.
  - id: copy_unmodified
    description: Copy background cells, frame cells, and obstacle cells directly from input to output.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each cell (`R`, `C`) of the input grid within the boundaries defined by the outer frame (specifically, for rows `r` from 3 to 9 and columns `c` from 4 to 10, check cells `input[r][c]`).
3.  For each cell `(r, c)` within this inner region:
    a.  Check if the value of the cell in the *input* grid `input[r][c]` is 0.
    b.  If it is 0, check its four orthogonal neighbors in the *input* grid: `input[r-1][c]`, `input[r+1][c]`, `input[r][c-1]`, `input[r][c+1]`.
    c.  If *any* of these neighbors has the value 3, set the corresponding cell in the *output* grid `output[r][c]` to 4.
    d.  If *none* of these neighbors has the value 3, set the corresponding cell in the *output* grid `output[r][c]` to 2.
4.  Cells outside this inner region, and cells within the region that were not originally 0 (i.e., the frame cells and internal obstacles), remain unchanged from their input values (already handled by initializing the output as a copy).
5.  Return the modified output grid.