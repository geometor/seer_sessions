
## train_1

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
```

## Perception
The input and output grids are both single rows (1D arrays) of pixels. Each input grid contains a single contiguous block of a non-white color, surrounded by white (0) pixels. The non-white color varies between examples (orange in train_1, yellow in train_2 and train_3). The output grid also contains a single contiguous block of the same non-white color as the input, surrounded by white pixels. The key transformation appears to be a spatial shift of the non-white block. Comparing the start and end positions of the non-white block in the input and output reveals a consistent shift of 3 positions to the right. The length and color of the block remain unchanged.

## Facts

```yaml
task_type: grid_transformation
grid_dimensionality: 1D (represented as 1xN)
input_features:
  - type: background
    color: white (0)
  - type: object
    description: A single contiguous horizontal block of a non-white color.
    properties:
      - color: Varies (orange, yellow)
      - length: Varies
      - position: Varies
output_features:
  - type: background
    color: white (0)
  - type: object
    description: A single contiguous horizontal block of a non-white color.
    properties:
      - color: Same as the input object's color
      - length: Same as the input object's length
      - position: Shifted relative to the input object's position
transformation:
  - action: identify
    target: the contiguous block of non-white color in the input grid
  - action: calculate_shift
    details: The shift amount is constant across examples.
    input_start_index: index of the first pixel of the block in the input
    output_start_index: index of the first pixel of the block in the output
    shift_amount: output_start_index - input_start_index = 3
  - action: apply_shift
    target: the identified block
    direction: right
    amount: 3 positions
  - action: update_grid
    details: Create the output grid by placing the shifted block and filling the remaining positions with white (0).
relationship:
  - The output block's color and length are identical to the input block's.
  - The output block's starting position is exactly 3 positions to the right of the input block's starting position.
```


## Natural Language Program
1.  Identify the single contiguous block of non-white pixels in the input row. Note its color, starting index, and ending index.
2.  Calculate the target starting index for the block in the output row by adding 3 to the starting index found in step 1.
3.  Create a new output row of the same length as the input row, initially filled with white (0) pixels.
4.  Place the identified block (with its original color and length) into the output row, starting at the calculated target starting index.
