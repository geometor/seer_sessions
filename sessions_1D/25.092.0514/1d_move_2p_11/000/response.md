**Perception:**

The input and output are both single-row grids (1-dimensional arrays). Each input grid contains a single contiguous block of a non-white color (azure, green, orange in the examples) surrounded by white pixels. The output grid is identical to the input grid, except that the non-white colored block has been shifted exactly two positions to the right. The size and color of the block remain unchanged. The pixels shifted "off" the right end by the block's movement are replaced by white pixels at the beginning of the row, and the pixels vacated by the block's leftward movement are also filled with white pixels.

**Facts:**


```yaml
task_type: grid_manipulation
grid_dimensionality: 1D # Input and output are single rows
background_color: white (0)
objects:
  - object_type: contiguous_block
    properties:
      color: non-white (any color except 0)
      count: exactly one per grid
      shape: horizontal line segment
      size: variable
      position: variable
actions:
  - action_type: horizontal_shift
    target: contiguous_block
    properties:
      direction: right
      distance: 2 pixels
      boundary_handling: wrap-around is not observed; shifted pixels are replaced by background color (white). The space left behind is also filled with the background color.
relationships:
  - The non-white block is always surrounded by the background color (white).
```


**Natural Language Program:**

1.  Identify the single contiguous block of non-white pixels within the input row.
2.  Determine the starting and ending column indices of this block.
3.  Create a new output row of the same size as the input row, initially filled with the background color (white).
4.  Calculate the new starting column index by adding 2 to the original starting column index.
5.  Copy the identified non-white block into the output row starting at the new calculated index. Ensure the copied block fits within the grid boundaries.