Okay, let's analyze the provided examples.

## Perception

1.  **Grid Dimensions:** Both input and output grids in the examples are 10 rows by 4 columns.
2.  **Content Distribution:** In both examples, the non-white pixels are concentrated in the bottom half of the input grid (specifically, rows 5 through 9). The top half (rows 0 through 4) is entirely white.
3.  **Input vs. Output Structure:**
    *   The bottom half of the output grid (rows 5-9) appears to be an exact copy of the bottom half of the input grid (rows 5-9).
    *   The top half of the output grid (rows 0-4) seems related to the bottom half of the input grid. Comparing input row 9 with output row 0, input row 8 with output row 1, and so on, reveals that the top half of the output grid is a vertically flipped version of the bottom half of the input grid.
4.  **Symmetry:** The output grid exhibits vertical symmetry around the horizontal line between row 4 and row 5. The top half is a mirror image (flipped vertically) of the bottom half.
5.  **Transformation Rule:** The transformation seems to involve isolating the bottom half of the input grid, copying it to the bottom half of the output grid, and copying a vertically flipped version of it to the top half of the output grid.

## Facts


```yaml
task_context:
  grid_properties:
    - dimensions: Both input and output grids have the same dimensions.
    - height: The height of the input grid is even (10 in the examples).
    - width: The width is consistent between input and output (4 in the examples).
  relevant_input_region:
    - name: bottom_half
    - definition: The rows from index `height / 2` to `height - 1`.
    - content: Contains all non-background pixels in the input.
  output_structure:
    - top_half: Rows from index 0 to `height / 2 - 1`.
    - bottom_half: Rows from index `height / 2` to `height - 1`.
transformation:
  actions:
    - action: select_region
      source: input_grid
      region: bottom_half
      result: selected_region
    - action: copy
      source: selected_region
      target: output_grid
      target_region: bottom_half
    - action: flip_vertical
      source: selected_region
      result: flipped_region
    - action: copy
      source: flipped_region
      target: output_grid
      target_region: top_half
  relationships:
    - output_grid.bottom_half is identical to input_grid.bottom_half.
    - output_grid.top_half is a vertically flipped version of input_grid.bottom_half.
    - output_grid exhibits vertical symmetry across its horizontal midpoint.
```


## Natural Language Program

1.  Determine the height (`H`) and width (`W`) of the input grid.
2.  Calculate the midpoint row index `M = H / 2`.
3.  Create a new output grid with the same dimensions (`H` x `W`).
4.  Identify the subgrid corresponding to the bottom half of the input grid (rows `M` to `H-1`).
5.  Copy this bottom-half subgrid directly to the bottom half of the output grid (rows `M` to `H-1`).
6.  Create a vertically flipped version of the bottom-half subgrid from the input.
7.  Copy this flipped subgrid to the top half of the output grid (rows `0` to `M-1`).
8.  Return the completed output grid.