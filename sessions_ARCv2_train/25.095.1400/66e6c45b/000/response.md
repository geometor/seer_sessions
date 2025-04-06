**Perception:**

The task involves transforming a 4x4 grid of numbers. The input grid features a central 2x2 block containing non-zero numbers, surrounded by zeros. The output grid rearranges these non-zero numbers, placing them at the four corners of the 4x4 grid, while the rest of the grid is filled with zeros. Specifically, the top-left element of the input's central block moves to the top-left corner of the output, the top-right element moves to the top-right corner, the bottom-left element moves to the bottom-left corner, and the bottom-right element moves to the bottom-right corner.

**YAML Facts:**


```yaml
objects:
  - name: Input Grid
    type: grid
    properties:
      size: 4x4
      elements: integers
      structure: contains a central 2x2 block of non-zero numbers surrounded by zeros.
  - name: Output Grid
    type: grid
    properties:
      size: 4x4
      elements: integers
      structure: contains non-zero numbers only at the four corners, rest are zeros.
  - name: Central 2x2 Block (Input)
    type: subgrid
    properties:
      location: rows 1-2, columns 1-2 (0-indexed)
      elements: non-zero integers from input
      cells:
        - top_left_input: Input[1][1]
        - top_right_input: Input[1][2]
        - bottom_left_input: Input[2][1]
        - bottom_right_input: Input[2][2]
  - name: Corner Cells (Output)
    type: specific cells
    properties:
      location: [0,0], [0,3], [3,0], [3,3] (0-indexed)
      elements: non-zero integers derived from input

actions:
  - name: Extract
    input: Input Grid
    output: Central 2x2 Block values
  - name: Relocate
    description: Map elements from the Central 2x2 Block to the Corner Cells of the Output Grid.
  - name: Fill Zeros
    target: Output Grid
    description: Set all non-corner cells in the Output Grid to 0.

relationships:
  - type: mapping
    from: Central 2x2 Block (Input)
    to: Corner Cells (Output)
    details:
      - Input[1][1] maps to Output[0][0]
      - Input[1][2] maps to Output[0][3]
      - Input[2][1] maps to Output[3][0]
      - Input[2][2] maps to Output[3][3]
```


**Natural Language Program:**

1.  Initialize an empty 4x4 output grid, filled with zeros.
2.  Identify the four values within the central 2x2 block of the input grid (at indices [1,1], [1,2], [2,1], and [2,2]).
3.  Place the value from input grid cell [1,1] into the output grid cell [0,0].
4.  Place the value from input grid cell [1,2] into the output grid cell [0,3].
5.  Place the value from input grid cell [2,1] into the output grid cell [3,0].
6.  Place the value from input grid cell [2,2] into the output grid cell [3,3].
7.  Return the resulting output grid.