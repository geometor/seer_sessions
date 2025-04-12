**Perception**

The input and output grids are both 3x11.
The input grid consistently features a 3x3 colored block on the far left (columns 0-2), followed by a vertical gray separator (column 3), a 3x3 white block (columns 4-6), another vertical gray separator (column 7), and a final 3x3 white block (columns 8-10).
The output grid retains the structure of the input grid, including the left 3x3 colored block and the gray separators in their original positions.
The key transformation occurs in the areas that were white in the input. The first white block (columns 4-6) is replaced by a 3x3 colored block which is a 90-degree clockwise rotation of the leftmost 3x3 input block. The second white block (columns 8-10) is replaced by a 3x3 colored block which is a 180-degree rotation of the leftmost 3x3 input block.

**Facts**


```yaml
task_context:
  grid_size:
    input: [3, 11]
    output: [3, 11]
  components:
    - object: left_block
      location: input grid, rows 0-2, columns 0-2
      size: [3, 3]
      content: variable colors (non-white, non-gray)
    - object: separator_1
      location: input grid, rows 0-2, column 3
      size: [3, 1]
      content: all gray (5)
    - object: middle_block_placeholder
      location: input grid, rows 0-2, columns 4-6
      size: [3, 3]
      content: all white (0)
    - object: separator_2
      location: input grid, rows 0-2, column 7
      size: [3, 1]
      content: all gray (5)
    - object: right_block_placeholder
      location: input grid, rows 0-2, columns 8-10
      size: [3, 3]
      content: all white (0)
transformation:
  - action: copy
    source: input grid, columns 0-3 and column 7
    destination: output grid, same locations
  - action: rotate
    source_object: left_block
    angle: 90 degrees clockwise
    result: middle_block_content
  - action: place
    source: middle_block_content
    destination: output grid, rows 0-2, columns 4-6 (replaces middle_block_placeholder)
  - action: rotate
    source_object: left_block
    angle: 180 degrees
    result: right_block_content
  - action: place
    source: right_block_content
    destination: output grid, rows 0-2, columns 8-10 (replaces right_block_placeholder)
relationships:
  - The content of the middle block in the output grid is determined by a 90-degree clockwise rotation of the left_block from the input grid.
  - The content of the right block in the output grid is determined by a 180-degree rotation of the left_block from the input grid.
  - The left_block and the gray separators from the input grid are preserved in the output grid.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the 3x3 subgrid located at the top-left corner of the input grid (rows 0-2, columns 0-2). Call this the `source_block`.
3.  Rotate the `source_block` 90 degrees clockwise. Call this `rotated_block_90`.
4.  Rotate the `source_block` 180 degrees. Call this `rotated_block_180`.
5.  Place the `rotated_block_90` into the output grid at rows 0-2, columns 4-6, overwriting the existing white pixels.
6.  Place the `rotated_block_180` into the output grid at rows 0-2, columns 8-10, overwriting the existing white pixels.
7.  Return the modified output grid.