**Perception**

1.  **Input Grid Structure:** All input examples are 1x14 grids (single rows).
2.  **Key Objects:**
    *   A contiguous horizontal block of a single color (green or orange). Let's call this the "main block".
    *   A single magenta pixel (color 6), acting as a marker or boundary.
    *   White pixels (color 0) filling the remaining space.
3.  **Relationships:** The main block and the magenta pixel are separated by zero or more white pixels in the input.
4.  **Output Grid Structure:** The output grids are also 1x14, containing the same colors and objects as the input.
5.  **Transformation:** The primary transformation is the horizontal shift (translation) of the "main block". Its final position appears to be determined by the position of the magenta pixel. Specifically, the main block moves rightwards until its rightmost pixel is immediately to the left of the magenta pixel. The magenta pixel itself does not move. The relative order of pixels within the main block remains unchanged. White pixels fill the space not occupied by the shifted main block or the magenta pixel.

**Facts**


```yaml
task_type: object_manipulation
grid_dimensions:
  input: 1x14
  output: 1x14
objects:
  - id: main_block
    description: A contiguous horizontal sequence of identical non-white, non-magenta pixels.
    properties:
      color: Varies (green '3' or orange '7' in examples).
      shape: Horizontal line segment.
      length: Varies.
      position: Varies in the input.
  - id: marker
    description: A single magenta pixel.
    properties:
      color: magenta '6'
      shape: Single pixel.
      position: Varies in the input, but remains fixed relative to the grid boundaries during transformation.
  - id: background
    description: Pixels filling the rest of the grid.
    properties:
      color: white '0'
actions:
  - action: shift
    target: main_block
    constraints:
      - type: relative_positioning
        reference_object: marker
        details: The main_block is moved horizontally such that its rightmost pixel becomes adjacent to the left side of the marker pixel.
relationships:
  - type: adjacency
    object1: main_block (right end)
    object2: marker (left side)
    state: established in output
  - type: immutability
    object: marker
    property: position
    state: maintained between input and output
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid, filled entirely with white pixels (color 0).
2.  Identify the single magenta pixel (color 6) in the input grid and record its column index. Place this magenta pixel at the same column index in the output grid.
3.  Identify the contiguous horizontal block of non-white (color > 0), non-magenta (color != 6) pixels in the input grid. Record its color and its length (number of pixels).
4.  Determine the target starting column index for this block in the output grid. This index is calculated as: `(magenta_pixel_column_index - block_length)`.
5.  Place the identified block (using its recorded color and length) into the output grid, starting at the calculated target starting column index and extending to the right until the column index `(magenta_pixel_column_index - 1)`.