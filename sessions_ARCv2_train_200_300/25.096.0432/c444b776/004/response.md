**General Assessment:**

The initial code (`code_00.py`) failed because it incorrectly interpreted the transformation rule. The results show that:
1.  For a single horizontal axis, the region *above* the axis is preserved and also copied to the region *below* the axis. The original content below the axis is discarded.
2.  For both horizontal and vertical axes, the Top-Left (TL) quadrant is preserved, the Bottom-Left (BL) quadrant is preserved and *also* copied to the Top-Right (TR) quadrant. The Bottom-Right (BR) quadrant is filled with zeros. The original TR and BR content is discarded.

The previous code assumed swaps or simple reflections/moves based on a single source region, which was incorrect. The strategy is to correctly identify the source region(s) based on the number of axes and copy them to the specified target locations in the output grid, preserving axes and zeroing out discarded regions.

**Metrics:**

*   **Example 1:**
    *   Input dimensions: 19x9
    *   Horizontal axis: row 9
    *   Vertical axis: None
    *   Source region (Input rows 0-8): Shape (9, 9)
    *   Output comparison:
        *   Output rows 0-8 match Input rows 0-8: True
        *   Output rows 10-18 match Input rows 0-8: True
        *   Output row 9 matches Input row 9: True
*   **Example 2:**
    *   Input dimensions: 19x19
    *   Horizontal axis: row 9
    *   Vertical axis: column 9
    *   Source Quadrants (Input): TL (0-8, 0-8), BL (10-18, 0-8). Shapes (9, 9).
    *   Output comparison:
        *   Output TL matches Input TL: True
        *   Output TR matches Input BL: True
        *   Output BL matches Input BL: True
        *   Output BR is all zeros: True
        *   Output row 9 matches Input row 9: True
        *   Output col 9 matches Input col 9: True

**YAML Facts:**


```yaml
task_elements:
  - element: grid
    description: A 2D array of integers representing the input and output state.
    properties:
      - dimensions: [rows, columns]
      - values: integers, with 0 as background, 4 as axis identifier.
  - element: axis
    description: A line (row or column) within the grid composed entirely of the integer 4.
    properties:
      - type: 'horizontal' or 'vertical'
      - index: The row or column index.
      - identifier_value: 4
    relationships:
      - divides: the grid into regions or quadrants.
  - element: region
    description: A section of the grid defined relative to an axis (e.g., above/below, left/right).
    properties:
      - location_relative_to_axis: 'above', 'below', 'left', 'right'
      - grid_slice: The row/column indices defining the region.
    relationships:
      - defined_by: axis
  - element: quadrant
    description: A section of the grid defined by the intersection of horizontal and vertical axes.
    properties:
      - location: 'top_left', 'top_right', 'bottom_left', 'bottom_right'
      - grid_slice: The row/column indices defining the quadrant.
    relationships:
      - defined_by: horizontal_axis, vertical_axis

actions:
  - action: identify_axes
    description: Scan the input grid to find the indices of rows and columns composed entirely of 4.
    inputs: input_grid
    outputs: horizontal_axis_index (Optional), vertical_axis_index (Optional)
  - action: copy_block
    description: Copy cell values from a source block (region/quadrant) in the input grid to a target block in the output grid.
    inputs: input_grid, source_slice, target_slice, output_grid
    outputs: modified_output_grid
  - action: copy_axis
    description: Copy an axis line (row or column) from the input grid to the output grid.
    inputs: input_grid, axis_index, axis_type ('horizontal' or 'vertical'), output_grid
    outputs: modified_output_grid
  - action: fill_block_with_zeros
    description: Set all cells within a specified block (region/quadrant) of the output grid to 0.
    inputs: target_slice, output_grid
    outputs: modified_output_grid

transformation_scenarios:
  - scenario: no_axes
    condition: No horizontal or vertical axis found.
    steps:
      - Create output grid identical to input grid.
  - scenario: horizontal_axis_only
    condition: Only horizontal axis `h` found.
    steps:
      - Initialize output grid with zeros, same dimensions as input.
      - Define source region: input rows < h (slice_src).
      - Define target region 1: output rows < h (slice_tgt1).
      - Define target region 2: output rows > h (slice_tgt2).
      - Perform: copy_block(input, slice_src, slice_tgt1, output)
      - Perform: copy_block(input, slice_src, slice_tgt2, output)
      - Perform: copy_axis(input, h, 'horizontal', output)
  - scenario: vertical_axis_only
    condition: Only vertical axis `v` found.
    steps:
      - Initialize output grid with zeros, same dimensions as input.
      - Define source region: input cols < v (slice_src).
      - Define target region 1: output cols < v (slice_tgt1).
      - Define target region 2: output cols > v (slice_tgt2).
      - Perform: copy_block(input, slice_src, slice_tgt1, output)
      - Perform: copy_block(input, slice_src, slice_tgt2, output)
      - Perform: copy_axis(input, v, 'vertical', output)
  - scenario: both_axes
    condition: Both horizontal axis `h` and vertical axis `v` found.
    steps:
      - Initialize output grid with zeros, same dimensions as input.
      - Define input quadrants slices: TL_in (rows<h, cols<v), BL_in (rows>h, cols<v).
      - Define output quadrants slices: TL_out (rows<h, cols<v), TR_out (rows<h, cols>v), BL_out (rows>h, cols<v), BR_out (rows>h, cols>v).
      - Perform: copy_block(input, TL_in, TL_out, output)
      - Perform: copy_block(input, BL_in, TR_out, output)
      - Perform: copy_block(input, BL_in, BL_out, output)
      - Perform: fill_block_with_zeros(BR_out, output) # Implicitly done by starting with zeros, but good to be explicit if needed.
      - Perform: copy_axis(input, h, 'horizontal', output)
      - Perform: copy_axis(input, v, 'vertical', output)
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Determine the dimensions (rows, columns) of the input grid.
3.  Scan the input grid to find the row index (`h`) of a horizontal axis (row of all 4s), if any.
4.  Scan the input grid to find the column index (`v`) of a vertical axis (column of all 4s), if any.
5.  Create an output grid of the same dimensions as the input, initially filled with zeros.
6.  **If only a horizontal axis `h` is found:**
    a.  Define the source block as the region in the input grid *above* the axis (`rows < h`).
    b.  Copy the source block to the region *above* the axis (`rows < h`) in the output grid.
    c.  Copy the source block to the region *below* the axis (`rows > h`) in the output grid.
    d.  Copy the axis row `h` from the input to the output grid at row `h`.
7.  **If only a vertical axis `v` is found:** (Inferred logic)
    a.  Define the source block as the region in the input grid *left* of the axis (`cols < v`).
    b.  Copy the source block to the region *left* of the axis (`cols < v`) in the output grid.
    c.  Copy the source block to the region *right* of the axis (`cols > v`) in the output grid.
    d.  Copy the axis column `v` from the input to the output grid at column `v`.
8.  **If both horizontal axis `h` and vertical axis `v` are found:**
    a.  Define the Top-Left (TL) input block (`rows < h`, `cols < v`).
    b.  Define the Bottom-Left (BL) input block (`rows > h`, `cols < v`).
    c.  Copy the TL input block to the TL output block (`rows < h`, `cols < v`).
    d.  Copy the BL input block to the Top-Right (TR) output block (`rows < h`, `cols > v`).
    e.  Copy the BL input block to the BL output block (`rows > h`, `cols < v`).
    f.  (The Bottom-Right output block `rows > h`, `cols > v` remains zeros from initialization).
    g.  Copy the horizontal axis row `h` from the input to the output grid at row `h`.
    h.  Copy the vertical axis column `v` from the input to the output grid at column `v`.
9.  **If no axes are found:**
    a.  Copy the entire input grid directly to the output grid (overwriting the initial zeros).
10. Return the completed output grid.