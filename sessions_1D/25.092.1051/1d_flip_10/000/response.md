## Perception of Task Elements

The task operates on 1-dimensional grids (rows). Each input grid contains a single contiguous block of non-white pixels surrounded by white (0) pixels. The transformation modifies only the non-white block, leaving the surrounding white pixels untouched. The core operation is reversing the order of the colors within the identified non-white block.

## YAML Facts


```yaml
task_type: array_manipulation
grid_dimensionality: 1D # All examples are 1xN grids
background_color: 0 # white
objects:
  - type: contiguous_block
    color: non-white # Any color other than white (0)
    count: 1 # Exactly one block per input
    properties:
      - location: embedded within white pixels
      - content: sequence of colors
actions:
  - name: identify_block
    input: input_grid
    output: coordinates and color sequence of the non-white block
  - name: reverse_sequence
    input: color sequence of the non-white block
    output: reversed color sequence
  - name: replace_block
    input:
      - input_grid
      - coordinates of the block
      - reversed color sequence
    output: output_grid
relationship: The output grid is identical to the input grid except for the segment corresponding to the non-white block, where the sequence of colors is reversed.
```


## Natural Language Program

1.  **Identify** the contiguous sequence of non-white pixels within the input row. Note the starting and ending positions of this sequence.
2.  **Extract** the colors of the pixels forming this sequence.
3.  **Reverse** the order of the extracted colors.
4.  **Create** the output row by copying the input row.
5.  **Replace** the pixels in the output row at the identified positions (from step 1) with the reversed sequence of colors (from step 3).