
## train_1

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
```


## train_3

**input:**
```
0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input and output are both 1-dimensional grids (or can be treated as such since they are single rows). Each input grid contains a single contiguous block of a non-white color (yellow, azure, magenta in the examples) surrounded by white pixels (color 0). The output grid shows that this non-white block has been shifted two positions to the right. The surrounding pixels remain white. The size of the grid and the color and size of the non-white block are preserved, only its position changes.

**Facts:**


```yaml
task_type: grid_transformation
dimensionality: 1D (represented as a single row)
grid_properties:
  size_preservation: true
objects:
  - type: contiguous_block
    color: non-white (variable: 4, 8, 6 in examples)
    properties:
      - color_preservation: true
      - size_preservation: true
      - shape_preservation: true (it's a 1D block)
  - type: background
    color: white (0)
actions:
  - name: identify_object
    target: non-white contiguous_block
    attributes:
      - start_index
      - length
      - color
  - name: shift_object
    target: non-white contiguous_block
    parameters:
      direction: right
      distance: 2 positions
  - name: create_output_grid
    properties:
      - same_dimensions_as_input
      - initial_fill: white (0)
  - name: place_object
    target: non-white contiguous_block
    destination: output_grid
    position: original_start_index + 2
relationships:
  - input_block_start_index -> output_block_start_index (output = input + 2)
  - input_grid_size == output_grid_size
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the white color (0).
2.  Scan the input grid to find the first pixel that is not white (0). Record its index (start index), its color, and determine the length of the contiguous block of this color starting from this index.
3.  Calculate the new starting index for this block in the output grid by adding 2 to the recorded start index from the input grid.
4.  Copy the identified contiguous block (with its original color and length) into the output grid, starting at the calculated new index.
5.  The output grid is now complete.
