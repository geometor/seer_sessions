
## train_1

**input:**
```
3 3 3 0 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 9 0 3 3 3 0 0 0
```


## train_2

**input:**
```
0 5 5 5 0 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 9 0 5 5 5 0 0
```


## train_3

**input:**
```
4 4 4 0 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 9 0 4 4 4 0 0 0
```

## Perception

The input and output are both 1x12 grids (or 1D arrays).
Each input contains:
1.  A single maroon pixel (9).
2.  A contiguous block of three identical pixels of another color (green, gray, or yellow in the examples).
3.  A white pixel (0) immediately preceding the maroon pixel (9).
4.  Other pixels are white (0).

The transformation rule involves rearranging these elements relative to the maroon pixel (9), which acts as an anchor, maintaining its absolute position.
Specifically:
-   The maroon pixel (9) stays in the same location (index).
-   The block of three identical pixels moves from its original position to a new position starting two indices after the maroon pixel.
-   The white pixel (0) that was originally immediately *before* the maroon pixel moves to the position immediately *after* the maroon pixel.
-   All other positions in the grid, including the original positions of the moved block and the original positions of any other pixels (except the anchor), become white (0).

## Facts


```yaml
task_type: grid_manipulation_1d
grid_dimensions:
  input: [1, 12]
  output: [1, 12]
objects:
  - id: anchor_pixel
    description: A single pixel with value 9 (maroon).
    properties:
      color: maroon
      value: 9
      count: 1
  - id: colored_block
    description: A contiguous block of 3 identical pixels.
    properties:
      color: non-white, non-maroon (e.g., green, gray, yellow)
      length: 3
      count: 1
  - id: pre_anchor_pixel
    description: The pixel immediately preceding the anchor_pixel in the input.
    properties:
      color: white
      value: 0
      location: index = anchor_pixel_index - 1
  - id: background_pixel
    description: Pixels with value 0 (white) used for filling space.
    properties:
      color: white
      value: 0
relationships:
  - type: relative_position
    object1: colored_block
    object2: anchor_pixel
    relation: colored_block appears before anchor_pixel in the input.
  - type: adjacency
    object1: pre_anchor_pixel
    object2: anchor_pixel
    relation: pre_anchor_pixel is immediately before anchor_pixel in the input.
actions:
  - action: identify
    target: anchor_pixel
    result: store its index (anchor_idx)
  - action: identify
    target: colored_block
    result: store its pixel values (block_pixels)
  - action: identify
    target: pre_anchor_pixel
    result: store its value (which is 0)
  - action: create_grid
    target: output grid
    properties:
      size: same as input
      initial_value: background_pixel (0)
  - action: place
    target: output grid
    object: anchor_pixel (value 9)
    location: anchor_idx
  - action: place
    target: output grid
    object: pre_anchor_pixel (value 0)
    location: anchor_idx + 1
  - action: place
    target: output grid
    object: colored_block (block_pixels)
    location: starting at anchor_idx + 2
```


## Natural Language Program

1.  Create a new output grid with the same dimensions as the input grid, and fill it entirely with white pixels (0).
2.  Find the index (position) of the single maroon pixel (9) in the input grid. Let this be `anchor_idx`.
3.  Find the contiguous block of three identical non-white, non-maroon pixels in the input grid. Store the sequence of these three pixel values as `colored_block`.
4.  Locate the pixel immediately before the maroon pixel in the input grid (this pixel will have the value 0). Store this value as `pre_anchor_pixel`.
5.  Place the maroon pixel (9) into the output grid at index `anchor_idx`.
6.  Place the `pre_anchor_pixel` (value 0) into the output grid at index `anchor_idx + 1`.
7.  Place the sequence of three pixels stored in `colored_block` into the output grid, starting at index `anchor_idx + 2`.
8.  The output grid is now complete.
