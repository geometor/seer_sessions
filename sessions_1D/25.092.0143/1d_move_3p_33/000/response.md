## Perception

The input and output are both single rows (1D grids) composed of pixels.
Each input row contains a single contiguous block of non-white pixels (e.g., red '2' or magenta '6') surrounded by white pixels ('0').
The output row contains the exact same block of non-white pixels (same color, same length) as the input, but its position is shifted horizontally to the right.
The surrounding pixels remain white.
By comparing the starting positions of the non-white block in the input and output across all examples, the shift amount is consistently 3 positions to the right.

## Facts


```yaml
task_type: grid_transformation
grid_dimensionality: 1D (single row)

components:
  - type: background
    color: white (0)
    role: static_canvas
  - type: object
    description: A single contiguous block of non-white pixels.
    properties:
      color: variable (e.g., red, magenta)
      length: variable
      position: defined by start and end indices

transformation:
  action: horizontal_shift
  target: the non-white object block
  direction: right
  magnitude: 3 positions
  effect: The start and end indices of the block increase by 3. The color and length remain unchanged. The background remains white.

examples_summary:
  - example: train_1
    object_color: red (2)
    input_start_index: 4
    output_start_index: 7
    shift: 3
  - example: train_2
    object_color: magenta (6)
    input_start_index: 3
    output_start_index: 6
    shift: 3
  - example: train_3
    object_color: magenta (6)
    input_start_index: 7
    output_start_index: 10
    shift: 3
```


## Natural Language Program

1.  Identify the single contiguous block of non-white pixels in the input row. Note its color, length, and starting position.
2.  Create an output row of the same length as the input row, initially filled with white pixels (0).
3.  Place the identified block of non-white pixels into the output row, starting 3 positions to the right of its original starting position in the input row. Ensure the color and length of the block are preserved.