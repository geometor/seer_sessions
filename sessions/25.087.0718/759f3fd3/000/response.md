**Perception:**

The input grid consists of a large `white` (0) background with a `green` (3) cross shape formed by a single horizontal line and a single vertical line. The size of the grid and the exact position of the green cross vary between examples.

The output grid retains the original `green` (3) cross. The key transformation occurs on the `white` (0) background pixels. Some of these pixels are changed to `yellow` (4), while others remain `white` (0). The pattern of `yellow` pixels forms a checkerboard across the entire grid, excluding the green lines.

There are two possible checkerboard patterns: one where cells `(r, c)` with `(r + c) % 2 == 0` are colored yellow, and one where cells with `(r + c) % 2 == 1` are colored yellow. The specific checkerboard pattern used in the output seems to depend on the row index of the horizontal green line. If the row index of the horizontal green line is even, the checkerboard pattern where `(r + c) % 2 == 0` is yellow is used. If the row index is odd, the checkerboard pattern where `(r + c) % 2 == 1` is yellow is used.

**Facts:**


```yaml
task_elements:
  - description: Input grid properties
    attributes:
      - grid_size: variable (e.g., 20x20, 10x10)
      - background_color: white (0)
      - foreground_object: green (3) cross
        properties:
          - shape: cross (one horizontal line, one vertical line)
          - thickness: 1 pixel
          - lines:
            - type: horizontal
              location: variable row index (e.g., row 5, row 4)
            - type: vertical
              location: variable column index (e.g., col 7, col 6)

  - description: Output grid properties
    attributes:
      - grid_size: same as input
      - preserved_object: green (3) cross from input
      - modified_background: contains white (0) and yellow (4) pixels
        properties:
          - pattern: checkerboard
          - colors_involved: white (0), yellow (4)
          - rule: replaces some original white pixels with yellow

transformation_logic:
  - description: Core transformation rule
    details:
      - step: Identify the row index (`green_row_idx`) of the horizontal green line in the input.
      - step: Determine the target checkerboard parity (`target_parity`) based on the row index:
          - if `green_row_idx` is even, `target_parity = 0`.
          - if `green_row_idx` is odd, `target_parity = 1`.
      - step: Iterate through each cell `(r, c)` of the input grid.
      - step: Apply rules based on input cell color and position:
          - if input color is green (3), output color is green (3).
          - if input color is white (0):
            - calculate cell parity: `cell_parity = (r + c) % 2`.
            - if `cell_parity == target_parity`, output color is yellow (4).
            - if `cell_parity != target_parity`, output color is white (0).

derived_properties:
  - description: Checkerboard pattern selection
    based_on: parity of the row index of the horizontal green line
    example_1:
      input_green_row_idx: 5 (odd)
      target_parity: 1
      output_pattern: yellow (4) where (r + c) % 2 == 1
    example_2:
      input_green_row_idx: 4 (even)
      target_parity: 0
      output_pattern: yellow (4) where (r + c) % 2 == 0
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Locate the horizontal line of `green` (3) pixels in the input grid and determine its row index, `green_row_idx`.
3.  Determine the target checkerboard parity `p`: if `green_row_idx` is even, set `p = 0`; otherwise, set `p = 1`.
4.  Iterate through each cell of the input grid using its row index `r` and column index `c`.
5.  For each cell `(r, c)`:
    a.  Check if the color of the input cell at `(r, c)` is `white` (0).
    b.  If it is `white`, calculate the cell's parity: `cell_parity = (r + c) % 2`.
    c.  If `cell_parity` is equal to the target parity `p`, change the color of the corresponding cell `(r, c)` in the output grid to `yellow` (4).
    d.  If the color of the input cell is not `white` (i.e., it's `green`), leave the corresponding cell in the output grid unchanged (it remains `green`).
6.  Return the modified output grid.