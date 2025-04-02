**Perception:**
The task operates on single-row grids (1D arrays). Each input grid contains a single contiguous block of a non-white color (yellow, orange, or gray in the examples) surrounded by white pixels. The output grid is the same size as the input grid. The transformation involves moving the colored block horizontally to the right by a fixed amount. In all three examples, the colored block is shifted exactly 3 positions to the right. The color and length of the block remain unchanged. The surrounding pixels remain white.

**YAML Facts:**

```yaml
task_description: Shift a horizontal colored block right by 3 positions.
grid_properties:
  dimensionality: 1D (single row)
  background_color: white (0)
objects:
  - name: colored_block
    description: A contiguous sequence of non-white pixels.
    properties:
      color: Any color except white (e.g., yellow, orange, gray)
      length: Variable (e.g., 10, 14, 7)
      count_per_input: 1
  - name: background
    description: White pixels surrounding the colored block.
    properties:
      color: white (0)
transformation:
  action: horizontal_shift
  target: colored_block
  parameters:
    direction: right
    distance: 3 pixels
  constraints:
    - Preserve the color of the colored_block.
    - Preserve the length of the colored_block.
    - Preserve the grid dimensions.
    - Fill empty spaces created by the shift with the background color (white).
```


**Natural Language Program:**
1.  Identify the contiguous block of non-white pixels in the input row. Note its color, length, and starting position (index).
2.  Create an output row of the same length as the input row, initially filled with white pixels.
3.  Calculate the new starting position for the block by adding 3 to its original starting position.
4.  Place the identified colored block (with its original color and length) into the output row starting at the calculated new position.