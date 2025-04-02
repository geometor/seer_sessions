
## train_1

**input:**
```
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0
```


## train_2

**input:**
```
0 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
```


## train_3

**input:**
```
3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output are 1D arrays (or potentially flattened 2D grids, but treated as 1D for the transformation) of pixels.
Each input array contains a single contiguous block of a non-white color against a white background.
The transformation involves moving this colored block exactly 3 positions to the right within the array.
The pixels displaced by the moving block become white, and the positions vacated by the block also become white.
The color of the block and its length remain unchanged. The overall size of the array remains constant.

## Facts


```yaml
task_type: transformation
input_domain: 1D_grid
output_domain: 1D_grid
grid_properties:
  size_relation: same_size
objects:
  - object_type: contiguous_block
    color: non_white (variable, e.g., yellow, green)
    background_color: white (0)
    count: 1_per_grid
actions:
  - action_type: spatial_translation
    direction: right
    magnitude: 3_positions
    target: the_non_white_contiguous_block
relationships:
  - The position of the non-white block changes between input and output.
  - All other pixels (white background) remain white, although their positions might effectively change relative to the shifted block.
```


## Natural Language Program

1.  Identify the contiguous block of non-white pixels in the input array. Note its color, starting index, and ending index.
2.  Create a new array of the same size as the input, initialized with the background color (white, 0).
3.  Calculate the new starting index for the block by adding 3 to its original starting index.
4.  Copy the identified non-white block into the new array starting at the calculated new starting index.
5.  The resulting array is the output.
